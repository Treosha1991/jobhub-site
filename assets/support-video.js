(() => {
  "use strict";
  const supported = ["ru", "en", "pl", "uk", "nl"];
  const siteLanguages = ["ru", "en", "pl", "uk"];
  const names = { ru: "Русский", en: "English", pl: "Polski", uk: "Українська", nl: "Nederlands" };
  const durations = { ru: "5:01", en: "4:51", pl: "5:09", uk: "5:12", nl: "5:17" };
  const copy = {
    ru: { play: "Смотреть презентацию", loading: "Загружаем видео…", error: "Видео не загрузилось. Нажмите «Попробовать снова» или выберите другой язык.", retry: "Попробовать снова", unsupported: "Этот браузер не поддерживает видео. Откройте страницу в актуальной версии Safari, Chrome, Edge или Firefox." },
    en: { play: "Watch the presentation", loading: "Loading the video…", error: "The video could not load. Select ‘Try again’ or choose another language.", retry: "Try again", unsupported: "This browser does not support the video. Open this page in a recent version of Safari, Chrome, Edge or Firefox." },
    pl: { play: "Obejrzyj prezentację", loading: "Ładowanie filmu…", error: "Nie udało się załadować filmu. Kliknij „Spróbuj ponownie” lub wybierz inny język.", retry: "Spróbuj ponownie", unsupported: "Ta przeglądarka nie obsługuje filmu. Otwórz stronę w aktualnej wersji Safari, Chrome, Edge lub Firefox." },
    uk: { play: "Дивитися презентацію", loading: "Завантажуємо відео…", error: "Не вдалося завантажити відео. Натисніть «Спробувати ще раз» або виберіть іншу мову.", retry: "Спробувати ще раз", unsupported: "Цей браузер не підтримує відео. Відкрийте сторінку в актуальній версії Safari, Chrome, Edge або Firefox." }
  };
  let library;
  function loadHls() {
    if (window.Hls) return Promise.resolve(window.Hls);
    if (!library) {
      library = new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "/assets/vendor/hls.js-1.7.3/hls.min.js";
        script.onload = () => resolve(window.Hls);
        script.onerror = () => { script.remove(); library = null; reject(new Error("player-library")); };
        document.head.append(script);
      });
    }
    return library;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const section = document.getElementById("support-video");
    if (!section) return;
    const html = document.documentElement;
    const video = document.getElementById("support-video-player");
    const selector = document.getElementById("support-video-language");
    const play = document.getElementById("support-video-play");
    const playLabel = document.getElementById("support-video-play-label");
    const status = document.getElementById("support-video-status");
    let language;
    let generation = 0;
    let hls = null;
    let preparing = false;
    const siteLanguage = () => siteLanguages.includes(html.dataset.lang) ? html.dataset.lang : "en";
    const text = () => copy[siteLanguage()];
    const root = () => `/assets/support-video/20261008/${language}`;

    function resetMedia() {
      generation += 1;
      video.pause();
      if (hls) { hls.destroy(); hls = null; }
      video.removeAttribute("src");
      video.querySelectorAll("track").forEach(track => track.remove());
      video.load();
      video.controls = false;
      preparing = false;
      play.hidden = false;
      play.disabled = false;
    }

    function chooseLanguage(next) {
      resetMedia();
      language = supported.includes(next) ? next : siteLanguage();
      section.dataset.videoLanguage = language;
      selector.value = language;
      video.poster = `${root()}/poster.jpg`;
      video.lang = language;
      video.setAttribute("aria-label", `JobHub Support · ${names[language]}`);
      document.getElementById("support-video-duration").textContent = durations[language];
      document.getElementById("support-video-nl-note").hidden = language !== "nl";
      playLabel.textContent = text().play;
      status.textContent = "";
    }

    function fail(id, message) {
      if (id !== generation) return;
      resetMedia();
      status.textContent = message || text().error;
      playLabel.textContent = text().retry;
    }

    async function start() {
      if (preparing) return;
      preparing = true;
      const id = generation;
      play.disabled = true;
      playLabel.textContent = text().loading;
      status.textContent = text().loading;
      const url = `${root()}/presentation.m3u8`;
      const track = document.createElement("track");
      track.kind = "subtitles";
      track.srclang = language;
      track.label = names[language];
      track.src = `${root()}/subtitles.vtt`;
      video.append(track);
      try {
        if (video.canPlayType("application/vnd.apple.mpegurl")) {
          // Native Safari HLS, including iPhone/iPad. Play stays in the user gesture.
          video.src = url;
        } else {
          const Hls = await loadHls();
          if (id !== generation) return;
          if (!Hls.isSupported()) { fail(id, text().unsupported); return; }
          hls = new Hls({
            maxBufferLength: 20, maxMaxBufferLength: 40,
            maxBufferSize: 12 * 1024 * 1024, backBufferLength: 20,
          });
          hls.on(Hls.Events.ERROR, (_, data) => {
            if (data.fatal) fail(id);
          });
          hls.loadSource(url);
          hls.attachMedia(video);
        }
        if (id !== generation) return;
        video.controls = true;
        await video.play();
        if (id !== generation) return;
        play.hidden = true;
        play.disabled = false;
        preparing = false;
        status.textContent = "";
      } catch (error) {
        if (id !== generation) return;
        if (error.name === "NotAllowedError") {
          // A browser may require a second gesture after asynchronously loading HLS.
          play.hidden = true;
          play.disabled = false;
          preparing = false;
          status.textContent = "";
        } else { fail(id); }
      }
    }

    play.addEventListener("click", start);
    video.addEventListener("error", () => {
      if (video.getAttribute("src")) fail(generation);
    });
    selector.addEventListener("change", () => chooseLanguage(selector.value));
    // The site's canonical language is set by app.js. An override is intentionally
    // kept only in this document: no URL parameter, cookie or localStorage key.
    new MutationObserver(() => chooseLanguage(siteLanguage())).observe(html, {
      attributes: true, attributeFilter: ["data-lang"]
    });
    window.addEventListener("pageshow", event => {
      if (event.persisted) chooseLanguage(siteLanguage());
    });
    chooseLanguage(siteLanguage());
  });
})();
