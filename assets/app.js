(() => {
  const html = document.documentElement;
  const storageKey = "jobhub_lang";
  const supported = ["ru", "en", "pl", "uk"];

  const normalize = (v) => {
    const lang = (v || "").toLowerCase();
    return supported.includes(lang) ? lang : "ru";
  };

  const getLang = () => {
    const qp = new URLSearchParams(window.location.search).get("lang");
    if (qp) return normalize(qp);
    return normalize(localStorage.getItem(storageKey));
  };

  function setLang(lang) {
    const safe = normalize(lang);
    html.dataset.lang = safe;
    html.lang = safe;
    localStorage.setItem(storageKey, safe);
    document.querySelectorAll("[data-set-lang]").forEach((btn) => {
      const active = btn.getAttribute("data-set-lang") === safe;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function bindLang() {
    document.querySelectorAll("[data-set-lang]").forEach((btn) => {
      btn.addEventListener("click", () => setLang(btn.getAttribute("data-set-lang")));
    });
  }

  function markActiveLinks() {
    const path = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
    document.querySelectorAll("a[data-nav]").forEach((link) => {
      const href = (link.getAttribute("href") || "").replace(/^\//, "").toLowerCase();
      const active = href === path;
      link.classList.toggle("active", active);
      if (active) {
        link.setAttribute("aria-current", "page");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  function bindMenu() {
    const overlay = document.getElementById("menuOverlay");
    const openBtn = document.getElementById("menuToggle");
    const closeBtn = document.getElementById("menuClose");
    if (!overlay || !openBtn) return;

    const open = () => {
      overlay.hidden = false;
      document.body.style.overflow = "hidden";
    };

    const close = () => {
      overlay.hidden = true;
      document.body.style.overflow = "";
    };

    openBtn.addEventListener("click", open);
    closeBtn?.addEventListener("click", close);
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) close();
    });
    document.querySelectorAll(".drawer-link").forEach((link) => {
      link.addEventListener("click", close);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    setLang(getLang());
    bindLang();
    markActiveLinks();
    bindMenu();
  });
})();
