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
})();
