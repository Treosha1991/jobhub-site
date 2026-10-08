// Browser acceptance: state, real playback, seek, captions, mobile, error recovery.
// Set JOBHUB_TEST_URL and JOBHUB_TEST_OUTPUT to repeat against a deployed site.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require = createRequire('C:/Users/treos/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/__runtime__.cjs');
const {chromium} = require('playwright');
const base = process.env.JOBHUB_TEST_URL || 'http://127.0.0.1:9018/';
const output = process.env.JOBHUB_TEST_OUTPUT || 'T:/JobApp/output/site-home-video-check/local';
await fs.mkdir(output, {recursive: true});
const browser = await chromium.launch({executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true});
const context = await browser.newContext({viewport: {width: 1440, height: 1000}, locale: 'en-GB'});
const errors = [], checks = [];
const page = await context.newPage();
page.on('pageerror', e => errors.push(e.message));
let mediaRequests = [];
page.on('request', request => {
  if (/\.(m3u8|m4s|mp4|vtt)(\?|$)/.test(request.url())) mediaRequests.push(request.url());
});
async function state() {
  return page.evaluate(() => ({
    site: document.documentElement.dataset.lang,
    selected: document.querySelector('#support-video-language').value,
    video: document.querySelector('#support-video').dataset.videoLanguage,
    storage: localStorage.getItem('jobhub_lang'),
    poster: document.querySelector('video').poster,
    paused: document.querySelector('video').paused,
    time: document.querySelector('video').currentTime,
  }));
}
async function ready() { await page.waitForFunction(() => document.querySelector('#support-video')?.dataset.videoLanguage); }
for (const site of ['ru', 'en', 'pl', 'uk']) {
  mediaRequests = [];
  await page.goto(`${base}?lang=${site}`);
  await ready();
  let current = await state();
  assert.equal(current.site, site);
  assert.equal(current.selected, site);
  assert.equal(current.video, site);
  assert.equal(current.paused, true);
  assert.equal(current.time, 0);
  assert.equal(mediaRequests.length, 0, 'no media before play');
  assert.match(current.poster, new RegExp(`/${site}/poster.jpg$`));
  for (const choice of ['ru', 'en', 'pl', 'uk', 'nl']) {
    await page.selectOption('#support-video-language', choice);
    current = await state();
    assert.equal(current.video, choice);
    assert.equal(current.site, site);
    assert.equal(current.storage, site);
    assert.equal(current.paused, true);
    assert.equal(current.time, 0);
    assert.match(current.poster, new RegExp(`/${choice}/poster.jpg$`));
  }
  await page.reload(); await ready();
  assert.equal((await state()).video, site);
  checks.push(`${site}: default, all 5 independent selections, reload reset, no autoplay/preload`);
}
// Site-language change resets any video override, including clicking the same site language.
await page.selectOption('#support-video-language', 'nl');
await page.locator('.lang-inline [data-set-lang="pl"]').click();
await page.waitForFunction(() => document.querySelector('#support-video-language').value === 'pl');
assert.equal((await state()).site, 'pl');
await page.selectOption('#support-video-language', 'nl');
await page.locator('.lang-inline [data-set-lang="pl"]').click();
await page.waitForFunction(() => document.querySelector('#support-video-language').value === 'pl');
await page.goto(base); await ready();
assert.equal((await state()).video, 'pl', 'stored site language without query');
checks.push('site language live change, same-language button, stored site language');

// Rapid selection while the lazy library is loading must not start an old film.
await page.selectOption('#support-video-language', 'ru');
await page.route('**/assets/vendor/**/hls.min.js', async route => {
  await new Promise(resolve => setTimeout(resolve, 500)); await route.continue();
});
await page.locator('#support-video-play').click();
await page.selectOption('#support-video-language', 'nl');
await page.waitForTimeout(750);
assert.equal((await state()).video, 'nl');
assert.equal((await state()).paused, true);
assert.equal(await page.locator('#support-video-play').isVisible(), true);
await page.unroute('**/assets/vendor/**/hls.min.js');
checks.push('switch during lazy player loading cancels old language');

const media = {};
for (const language of ['ru', 'en', 'pl', 'uk', 'nl']) {
  await page.selectOption('#support-video-language', language);
  mediaRequests = [];
  await page.locator('#support-video-play').click();
  await page.waitForFunction(() => {
    const v = document.querySelector('video'); return !v.paused && v.currentTime > .4 && v.videoWidth === 1920;
  }, null, {timeout: 45000});
  let result = await page.evaluate(() => {
    const v = document.querySelector('video'); return {duration: v.duration, width: v.videoWidth, height: v.videoHeight, time: v.currentTime, tracks: v.textTracks.length};
  });
  assert.equal(result.height, 1080);
  assert.equal(result.tracks, 1);
  assert(mediaRequests.filter(u => /\.(m3u8|m4s|mp4)(\?|$)/.test(u)).every(u => u.includes(`/${language}/`)));
  // Seek well beyond the initial buffer, then seek close to the end.
  await page.evaluate(() => { document.querySelector('video').currentTime = 170; });
  await page.waitForFunction(() => { const v = document.querySelector('video'); return v.currentTime > 170.2 && v.readyState >= 3; }, null, {timeout: 30000});
  await page.evaluate(() => { const v = document.querySelector('video'); v.textTracks[0].mode = 'showing'; v.currentTime = v.duration - 6; });
  await page.waitForFunction(() => { const v = document.querySelector('video'); return v.currentTime > v.duration - 5.7 && v.readyState >= 3; }, null, {timeout: 30000});
  await page.waitForFunction(() => { const t = document.querySelector('video').textTracks[0]; return t.cues?.length > 0; }, null, {timeout: 10000});
  result.cues = await page.evaluate(() => document.querySelector('video').textTracks[0].cues.length);
  await page.evaluate(() => document.querySelector('video').pause());
  assert.equal((await state()).paused, true);
  media[language] = {...result, mediaRequests: mediaRequests.length};
  checks.push(`${language}: 1080p playback, pause, middle/end seek, own captions`);
  console.log(`Verified playback and captions: ${language}`);
}
await page.locator('#support-video').scrollIntoViewIfNeeded();
await page.screenshot({path: path.join(output, 'desktop-nl.png')});
await page.reload(); await ready();
assert.equal((await state()).video, 'pl');
assert.equal((await state()).paused, true);
await page.locator('#support-video').scrollIntoViewIfNeeded();
await page.screenshot({path: path.join(output, 'desktop-pl.png')});

// Recoverable media/network failure: retry remains clickable.
await page.route('**/assets/support-video/**/presentation.m3u8', route => route.fulfill({status: 404, body: 'missing'}));
await page.locator('#support-video-play').click();
await page.waitForFunction(() => document.querySelector('#support-video-status').textContent.includes('Nie udało'));
assert.equal(await page.locator('#support-video-play').isEnabled(), true);
await page.unroute('**/assets/support-video/**/presentation.m3u8');
await page.locator('#support-video-play').click();
await page.waitForFunction(() => !document.querySelector('video').paused && document.querySelector('video').currentTime > .2, null, {timeout: 30000});
checks.push('missing media displays localized error; retry succeeds');

// Browser-locale default and narrow screens. Native Safari playback requires a real
// Apple device; this exercises the actual Chromium HLS path with a phone viewport.
const mobileContext = await browser.newContext({viewport: {width: 390, height: 844}, isMobile: true, hasTouch: true, locale: 'uk-UA'});
const mobile = await mobileContext.newPage();
mobile.on('pageerror', e => errors.push(e.message));
await mobile.goto(base);
await mobile.waitForFunction(() => document.querySelector('#support-video')?.dataset.videoLanguage === 'uk');
for (const width of [320, 390, 768]) {
  await mobile.setViewportSize({width, height: 844});
  for (const language of ['ru', 'en', 'pl', 'uk']) {
    await mobile.goto(`${base}?lang=${language}`);
    await mobile.waitForFunction(() => document.querySelector('#support-video')?.dataset.videoLanguage);
    assert.equal(await mobile.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `overflow ${width}/${language}`);
    await mobile.locator('#support-video').scrollIntoViewIfNeeded();
    if (width === 390) await mobile.screenshot({path: path.join(output, `mobile-${language}.png`)});
  }
}
await mobile.setViewportSize({width: 390, height: 844});
await mobile.selectOption('#support-video-language', 'nl');
await mobile.locator('#support-video-play').click();
await mobile.waitForFunction(() => !document.querySelector('video').paused && document.querySelector('video').currentTime > .2, null, {timeout: 30000});
await mobile.evaluate(() => document.querySelector('video').pause());
await mobile.reload();
await mobile.waitForFunction(() => document.querySelector('#support-video')?.dataset.videoLanguage === 'uk');
checks.push('browser locale uk-UA, 320/390/768px all site languages, mobile NL playback and reload reset');
// Exercise the MSE/hls.js path used by browsers without native HLS.
const mseContext = await browser.newContext({viewport: {width: 1440, height: 1000}});
await mseContext.addInitScript(() => {
  const native = HTMLMediaElement.prototype.canPlayType;
  HTMLMediaElement.prototype.canPlayType = function(type) {
    return type.includes('mpegurl') ? '' : native.call(this, type);
  };
});
const mse = await mseContext.newPage();
mse.on('pageerror', e => errors.push(e.message));
await mse.goto(`${base}?lang=en`);
for (const language of ['ru', 'en', 'pl', 'uk', 'nl']) {
  await mse.selectOption('#support-video-language', language);
  await mse.locator('#support-video-play').click();
  await mse.waitForFunction(() => !document.querySelector('video').paused && document.querySelector('video').currentTime > .4, null, {timeout: 30000});
  assert.equal(await mse.evaluate(() => window.Hls.version), '1.7.3');
  await mse.evaluate(() => { document.querySelector('video').currentTime = 120; });
  await mse.waitForFunction(() => document.querySelector('video').currentTime > 120.2, null, {timeout: 30000});
  await mse.evaluate(() => document.querySelector('video').pause());
}
// Fullscreen entry/exit requires a trusted click; use the player's native surface.
await mse.evaluate(() => {
  const button = document.createElement('button'); button.id = 'test-fullscreen';
  button.textContent = 'Fullscreen'; button.onclick = () => document.querySelector('video').requestFullscreen();
  document.body.append(button);
});
await mse.locator('#test-fullscreen').click();
await mse.waitForFunction(() => document.fullscreenElement?.tagName === 'VIDEO');
await mse.evaluate(() => document.exitFullscreen());
await mse.waitForFunction(() => !document.fullscreenElement);
checks.push('all 5 videos play and seek through hls.js/MSE; fullscreen entry/exit');
assert.deepEqual(errors, []);
await fs.writeFile(path.join(output, 'verification.json'), JSON.stringify({base, date: new Date().toISOString(), checks, media, errors}, null, 2));
console.log(JSON.stringify({base, passed: checks.length, media, errors}, null, 2));
await browser.close();
