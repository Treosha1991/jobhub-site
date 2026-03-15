(() => {
  const html = document.documentElement;
  const storageKey = "jobhub_lang";
  const supported = ["ru", "en", "pl", "uk"];

  const withLang = (raw, lang) => {
    const safe = normalize(lang);
    const url = new URL(raw, window.location.origin);
    url.searchParams.set("lang", safe);
    if (url.origin === window.location.origin) {
      return `${url.pathname}${url.search}${url.hash}`;
    }
    return url.toString();
  };

  const normalize = (v) => {
    const lang = (v || "").toLowerCase();
    return supported.includes(lang) ? lang : "en";
  };

  const getBrowserLang = () => {
    const candidates = Array.isArray(navigator.languages) && navigator.languages.length
      ? navigator.languages
      : [navigator.language, navigator.userLanguage];
    for (const value of candidates) {
      const code = String(value || "").trim().toLowerCase().split("-")[0];
      if (supported.includes(code)) return code;
    }
    return "en";
  };

  const getLang = () => {
    const qp = new URLSearchParams(window.location.search).get("lang");
    if (qp) return normalize(qp);
    const stored = localStorage.getItem(storageKey);
    if (stored) return normalize(stored);
    return getBrowserLang();
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
    syncLangLinks(safe);
    const localizedCurrent = withLang(window.location.href, safe);
    const current = `${window.location.pathname}${window.location.search}${window.location.hash}`;
    if (localizedCurrent !== current) {
      window.history.replaceState({}, "", localizedCurrent);
    }
  }

  function syncLangLinks(lang) {
    const safe = normalize(lang);
    document.querySelectorAll('a[href]').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
      const localizedHref = withLang(href, safe);
      if (localizedHref !== href) {
        link.setAttribute('href', localizedHref);
      }
    });
  }

  function bindLang() {
    document.querySelectorAll("[data-set-lang]").forEach((btn) => {
      btn.addEventListener("click", () => setLang(btn.getAttribute("data-set-lang")));
    });
  }

  function markActiveLinks() {
    const normalizeRoute = (value) => {
      let route = String(value || "")
        .trim()
        .toLowerCase()
        .split("#")[0]
        .split("?")[0];

      // Skip non-page links.
      if (route.startsWith("mailto:") || route.startsWith("tel:")) return "";

      // Handle absolute URLs.
      route = route.replace(/^https?:\/\/[^/]+/i, "");

      route = route.replace(/^\/+/, "").replace(/\/+$/, "");

      if (!route || route === "index" || route === "index.html") return "index";
      if (route.endsWith(".html")) route = route.slice(0, -5);
      return route;
    };

    const currentRoute = normalizeRoute(window.location.pathname);

    document.querySelectorAll("a[data-nav]").forEach((link) => {
      const href = normalizeRoute(link.getAttribute("href") || "");
      const active = href && href === currentRoute;
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
