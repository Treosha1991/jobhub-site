(() => {
  const html = document.documentElement;
  const key = "jobhub_lang";

  function setLang(lang) {
    html.dataset.lang = lang;
    html.lang = lang === "ru" ? "ru" : "en";
    localStorage.setItem(key, lang);
  }

  function initLang() {
    const saved = localStorage.getItem(key);
    setLang(saved === "ru" ? "ru" : "en");
  }

  function bindLangToggle() {
    const btn = document.getElementById("langToggle");
    if (!btn) return;
    btn.addEventListener("click", () => {
      setLang(html.dataset.lang === "ru" ? "en" : "ru");
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initLang();
    bindLangToggle();
  });
})();

