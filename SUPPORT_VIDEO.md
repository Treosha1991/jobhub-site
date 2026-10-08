# Home-page video presentation

The `#support-video` section follows the home-page hero. It uses the approved
Russian, English, Polish, Ukrainian and Dutch films, including their original
narration, translated screenshots and language-specific animation timing.

The same player and media are embedded near the beginning of the featured news
article at `/news#support-video-2026-10-08`. The article is localized in the site's
four languages. Its styles are scoped to `.support-news`; older news is preserved.

## Language behavior

- Initial video language comes from `html[data-lang]`, set by `assets/app.js`.
  The site's existing URL, saved preference and browser-language rules still apply.
- The video's own selector changes only the current film, poster and subtitle
  track. It never writes language settings to the URL, cookies or localStorage.
- Changing the site language resets the video to that language. Reloading the
  page also resets it. A restored page from the browser's back/forward cache resets
  it as well.
- Selecting another film stops the current playback and resets its position.
- Subtitles are visible by default after Play in both page embeds. The visible CC
  button toggles them, and stays in sync with the native player's subtitle menu.
  The choice is kept while switching films on that page; a reload enables them
  again. Native text-track rendering keeps subtitles in video fullscreen.
- Dutch is a video option only. The application and site still support RU/EN/PL/UK.
  A localized note appears when Dutch is selected.

## Media and delivery

Versioned media: `assets/support-video/20261008/{ru,en,pl,uk,nl}/`.
Each film is an HLS VOD playlist with fragmented MP4 segments. The approved
1920×1080 H.264 picture and AAC audio are copied, **not re-encoded**. The MP4 masters
and the editable/manual presentations remain in `T:/JobApp/output/jobhub-support-video`.
Master hashes, durations and segment sizes are recorded in `manifest.json`.

The page fetches only a poster before the visitor presses Play. The chosen film
then streams in short segments. Native HLS is preferred when available; other
MSE-capable browsers lazily load the self-hosted `hls.js` 1.7.3 distribution.
Its Apache-2.0 license and package-integrity/source information are included in
`assets/vendor/hls.js-1.7.3/`. No third-party player iframe or CDN is required.

The site is deployed from GitHub `Treosha1991/jobhub-site` `main` by the existing
Cloudflare Pages integration. `_headers` sets playlist/subtitle content types
and immutable caching for the versioned media. All assets are below the Pages
25 MiB per-file limit. If media changes, use a **new versioned directory** and
update the JS and header paths together. Never overwrite immutable
media URLs with different content.

## Rebuilding and checking

```powershell
python tools/prepare_support_video.py --source T:/JobApp/output/jobhub-support-video
python tools/check_site.py
python -m http.server 9018 --bind 127.0.0.1
node tools/check_support_video.mjs
```

The browser check uses the bundled Codex Playwright dependency and the installed
Microsoft Edge. Set `JOBHUB_TEST_URL` and `JOBHUB_TEST_OUTPUT` to repeat against
the public site. The report and screenshots are saved outside the repository at
`T:/JobApp/output/site-home-video-check/`.
Use a URL ending in `/news.html` (local) or `/news` (public) to check the player
inside the news article. Reports for that page live in `site-news-video-check/`.

Coverage: all four site defaults and all five independent video choices; reload
reset; live site-language changes; browser-language default; no media before
Play; full-HD playback; middle/end seeking; visible subtitle cues and CC/native
toggle synchronization; native-HLS and
HLS.js/MSE paths; fullscreen; localized media-error recovery; 320/390/768px layouts.
The phone-layout check runs in Chromium. Physical iPhone/Safari acceptance is
separate and is not implied by these checks.

Original public slides at `/support-presentation-review` are preserved.
