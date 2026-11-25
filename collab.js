// "Suggest a collaboration" form: the Worker opens the request, the PDF goes straight
// from the browser to Google Drive, and success is shown only after the Worker confirms it.
(() => {
  const btn = document.querySelector(".collab-btn");
  const form = document.getElementById("collab-form");
  if (!btn || !form) return;
  const T = JSON.parse(document.getElementById("collab-text").textContent);
  const API = form.dataset.api.replace(/\/+$/, "");
  const MAX = 5 * 1024 * 1024;
  const $ = name => form.elements.namedItem(name);
  const status = form.querySelector(".collab-status");
  const bar = form.querySelector(".collab-bar");
  const submit = form.querySelector("[type=submit]");
  const submitText = submit.querySelector("span");
  const fileName = form.querySelector(".collab-file-name");
  let busy = false;

  const toggle = open => {
    form.hidden = !open;
    btn.setAttribute("aria-expanded", String(open));
    if (open) $("name").focus();
  };
  btn.addEventListener("click", () => toggle(form.hidden));
  form.querySelector(".collab-cancel").addEventListener("click", () => { toggle(false); btn.focus(); });

  const say = (text, kind = "") => { status.textContent = text; status.className = "collab-status " + kind; };
  const progress = p => { bar.hidden = p === null; if (p !== null) { bar.value = p; } };

  // ---------- validation (the Worker checks everything again) ----------
  const checks = {
    name: () => { const n = [...$("name").value.trim()].length; return n < 2 || n > 80 ? T.e_name : ""; },
    email: () => /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)+$/.test($("email").value.trim()) ? "" : T.e_email,
    idea: () => { const n = [...$("idea").value.trim()].length; return n < 20 || n > 2000 ? T.e_idea : ""; },
    file: () => {
      const f = $("file").files[0];
      if (!f) return T.e_file_missing;
      if (!/\.pdf$/i.test(f.name) || (f.type && f.type !== "application/pdf")) return T.e_file_type;
      if (f.size > MAX) return T.e_file_size;
      return f.size ? "" : T.e_file_type;
    },
  };
  const show = (key, msg) => {
    const err = document.getElementById(`collab-${key}-err`);
    err.textContent = msg; err.hidden = !msg;
    if (msg) $(key).setAttribute("aria-invalid", "true"); else $(key).removeAttribute("aria-invalid");
    return !msg;
  };
  const check = key => show(key, checks[key]());
  for (const key of Object.keys(checks)) {
    $(key).addEventListener(key === "file" ? "change" : "blur", () => { if ($(key).value) check(key); });
    $(key).addEventListener("input", () => { if ($(key).hasAttribute("aria-invalid")) check(key); });
  }
  const showFile = () => { const f = $("file").files[0]; fileName.textContent = f ? f.name : T.no_file; };
  $("file").addEventListener("change", showFile);

  // ---------- network ----------
  class Fail extends Error { constructor(code, data = {}) { super(code); this.code = code; this.data = data; } }
  const pause = ms => new Promise(r => setTimeout(r, ms));

  async function api(path, body) {
    for (let n = 0; ; n++) {
      let r = null;
      try {
        r = await fetch(API + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      } catch { /* offline, or the Worker is unreachable */ }
      const data = r ? await r.json().catch(() => ({})) : {};
      if (r && r.ok) return data;
      const temporary = !r || r.status >= 500;
      if (!temporary) throw new Fail(data.error || "server", data);
      if (n >= 2) throw new Fail(r ? "server" : "network");
      await pause(800 * 2 ** n);
    }
  }

  /** PUT straight to Google Drive. Resolves with the HTTP status; 0 = no readable answer (network or CORS). */
  function put(url, file, offset, onProgress) {
    return new Promise(resolve => {
      const x = new XMLHttpRequest();
      x.open("PUT", url);
      x.setRequestHeader("Content-Type", "application/pdf");
      if (offset) x.setRequestHeader("Content-Range", `bytes ${offset}-${file.size - 1}/${file.size}`);
      x.upload.onprogress = e => { if (e.lengthComputable) onProgress((offset + e.loaded) / file.size); };
      x.onload = () => resolve(x.status);
      x.onerror = x.ontimeout = x.onabort = () => resolve(0);
      x.timeout = 180000;
      x.send(offset ? file.slice(offset) : file);
    });
  }

  async function sha256(file) {
    const d = await crypto.subtle.digest("SHA-256", await file.arrayBuffer());
    return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, "0")).join("");
  }

  async function send() {
    const file = $("file").files[0];
    say(T.preparing, "busy");
    const sha = await sha256(file);
    // Sending the same content again returns the same request, so a retry never makes a second folder.
    let state = await api("/v1/requests", {
      name: $("name").value, email: $("email").value, idea: $("idea").value,
      file: { name: file.name, type: "application/pdf", size: file.size, sha256: sha },
    });
    let blocked = 0;
    for (let n = 0; state.status === "upload"; n++) {
      if (n >= 4) throw new Fail(blocked === n ? "direct_upload" : "upload");
      if (n) { say(T.retrying, "busy"); await pause(1000 * 2 ** (n - 1)); }
      say(T.uploading, "busy");
      progress((state.offset || 0) / file.size);
      const code = await put(state.uploadUrl, file, state.offset || 0, p => {
        progress(p); say(`${T.uploading} ${Math.round(p * 100)}%`, "busy");
      });
      if (code === 0) { blocked++; console.warn("[collab] direct PUT to Google Drive gave no readable answer (network or CORS)"); }
      progress(1);
      say(T.verifying, "busy");
      state = await api("/v1/complete", { id: state.id }); // only this call decides success
    }
    if (state.status !== "complete") throw new Fail("server");
    return state.id;
  }

  function explain(err) {
    const { code, data } = err instanceof Fail ? err : { code: "server", data: {} };
    if (code === "rate_limited") {
      const min = Math.max(1, Math.ceil((data.retryAfter || 60) / 60));
      return T.e_rate.replace("{n}", min);
    }
    if (code === "invalid") {
      const map = { name: T.e_name, email: T.e_email, idea: T.e_idea, file: data.fields?.file === "size" ? T.e_file_size : T.e_file_type };
      for (const k of Object.keys(data.fields || {})) if (map[k]) show(k, map[k]);
      return T.e_check;
    }
    return { bad_file: T.e_bad_file, network: T.e_network, direct_upload: T.e_direct, upload: T.e_upload }[code] || T.e_server;
  }

  form.addEventListener("submit", async ev => {
    ev.preventDefault();
    if (busy) return;
    const bad = Object.keys(checks).filter(k => !check(k));
    if (bad.length) { say(T.e_check, "error"); $(bad[0]).focus(); return; }
    if (!API) { say(T.e_off, "error"); return; }

    busy = true;
    submit.disabled = true;
    form.setAttribute("aria-busy", "true");
    submitText.textContent = T.sending;
    const inputs = form.querySelector("fieldset");
    const warn = e => { e.preventDefault(); };
    window.addEventListener("beforeunload", warn);
    try {
      const work = send();
      inputs.disabled = true;
      const id = await work;
      form.reset(); showFile();
      say(T.success.replace("{id}", id.slice(0, 8)), "ok");
    } catch (err) {
      if (!(err instanceof Fail)) console.error(err);
      say(explain(err), "error");
    } finally {
      window.removeEventListener("beforeunload", warn);
      progress(null);
      busy = false;
      inputs.disabled = false;
      submit.disabled = false;
      form.removeAttribute("aria-busy");
      submitText.textContent = T.send;
      status.focus();
    }
  });
})();
