(() => {
  const root = document.documentElement;
  const items = document.querySelectorAll(".reveal");

  // "?noanim" shows everything at once (handy for screenshots)
  if (location.search.includes("noanim") || !("IntersectionObserver" in window)) {
    root.classList.add("no-anim");
    items.forEach(el => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(el => io.observe(el));
  }

  // Flip cards: drawing <-> real screenshot
  document.querySelectorAll(".card3d").forEach(card => {
    const set = on => {
      card.classList.toggle("is-flipped", on);
      card.setAttribute("aria-pressed", on ? "true" : "false");
    };
    card.addEventListener("click", () => set(!card.classList.contains("is-flipped")));
    if (location.search.includes("flipped")) set(true);
  });

  // Enlarge a project screenshot
  const box = document.querySelector(".lightbox");
  if (box && box.showModal) {
    const img = box.querySelector("img");
    document.querySelectorAll(".zoom").forEach(btn => {
      btn.addEventListener("click", () => {
        img.src = btn.dataset.src; img.alt = btn.dataset.alt;
        box.showModal();
      });
    });
    box.querySelector(".lb-close").addEventListener("click", () => box.close());
    box.addEventListener("click", ev => { if (ev.target === box) box.close(); });
  } else {
    document.querySelectorAll(".zoom").forEach(b => b.remove());
  }

  // Copy email
  document.querySelectorAll("[data-copy]").forEach(btn => {
    const label = btn.querySelector("span");
    const original = label.textContent;
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.copy);
      } catch {
        const ta = document.createElement("textarea");
        ta.value = btn.dataset.copy; document.body.append(ta); ta.select();
        try { document.execCommand("copy"); } catch {}
        ta.remove();
      }
      label.textContent = btn.dataset.done;
      btn.classList.add("done");
      setTimeout(() => { label.textContent = original; btn.classList.remove("done"); }, 2000);
    });
  });
  // Menu: underline the section currently on screen
  const navLinks = [...document.querySelectorAll(".nav a[href^='#']")];
  const targets = navLinks.map(a => [a, document.querySelector(a.getAttribute("href"))]).filter(x => x[1]);
  if (targets.length) {
    const mark = current => navLinks.forEach(a => {
      a.classList.toggle("on", a === current);
      if (a === current) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
    const onScroll = () => {
      let current = targets[0][0];
      const line = window.innerHeight * 0.35;
      targets.forEach(([a, sec]) => { if (sec.id !== "main" && sec.getBoundingClientRect().top <= line) current = a; });
      mark(current);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
  // Projects: "Read more" shows the problem / solution / role
  document.querySelectorAll(".more-btn").forEach(btn => {
    const box = document.getElementById(btn.getAttribute("aria-controls"));
    const label = btn.querySelector("span");
    if (!box) { btn.remove(); return; }
    btn.addEventListener("click", () => {
      const open = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      box.classList.toggle("open", open);
      label.textContent = open ? btn.dataset.less : btn.dataset.more;
    });
  });
  // Phone menu: the ☰ button opens the list of sections
  const top = document.querySelector(".top");
  const menuBtn = document.querySelector(".menu-btn");
  if (top && menuBtn) {
    const setOpen = open => { top.classList.toggle("open", open); menuBtn.setAttribute("aria-expanded", open ? "true" : "false"); };
    menuBtn.addEventListener("click", () => setOpen(!top.classList.contains("open")));
    document.querySelectorAll(".nav a").forEach(a => a.addEventListener("click", () => setOpen(false)));
    document.addEventListener("keydown", ev => { if (ev.key === "Escape") setOpen(false); });
  }
})();
