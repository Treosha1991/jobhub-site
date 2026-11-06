const appId = 6761860677;
const bundleId = 'today.jobhub.app';

function isSupportRelease(name, version) {
  if (name?.trim().toLowerCase() !== 'jobhub support'
      || !/^\d+\.\d+(\.\d+)?$/.test(version)) return false;
  const [major, minor, patch = 0] = version.split('.').map(Number);
  return major > 1 || (major === 1 && (minor > 0 || patch >= 6));
}

async function checkStorefront(url) {
  const response = await fetch(url, { signal: AbortSignal.timeout(4000) });
  if (!response.ok) throw new Error('storefront_http_' + response.status);
  const html = await response.text();
  const app = html.match(/<script\b[^>]*\bid="?software-application"?\s+[^>]*>([^<]+)<\/script>/i);
  const state = html.match(/<script\b[^>]*\bid="serialized-server-data"[^>]*>([\s\S]*?)<\/script>/i);
  if (!app || !state) throw new Error('storefront_format');
  const { name } = JSON.parse(app[1]);
  const subtitle = JSON.parse(state[1]).data[0]?.data?.shelfMapping?.mostRecentVersion?.items[0]?.primarySubtitle;
  const version = subtitle?.match(/\d+\.\d+(\.\d+)?$/)?.[0];
  return isSupportRelease(name, version);
}

export async function onRequestGet(context) {
  const { request } = context;
  const detectedCountry = request.cf?.country?.toLowerCase();
  const country = /^[a-z]{2}$/.test(detectedCountry) && detectedCountry !== 'xx' ? detectedCountry : 'pl';
  const cacheUrl = new URL('/api/app-store-release', request.url);
  cacheUrl.searchParams.set('country', country);
  const cache = caches.default;
  const cached = await cache.match(cacheUrl.href);
  const headers = { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
  if (cached) return Response.json(await cached.json(), { headers });

  const lookup = new URL('https://itunes.apple.com/lookup');
  lookup.search = new URLSearchParams({ id: appId, country, entity: 'software' });
  const storeUrl = 'https://apps.apple.com/' + country + '/app/id' + appId;
  try {
    const response = await fetch(lookup.href, { signal: AbortSignal.timeout(4000) });
    let available;
    if (response.status === 403) {
      // Some edge addresses cannot reach Lookup; check the same public storefront.
      available = await checkStorefront(storeUrl);
    } else {
      if (!response.ok) throw new Error('store_http_' + response.status);
      const { results } = await response.json();
      available = results.some(app => app.trackId === appId && app.bundleId === bundleId
        && isSupportRelease(app.trackName, app.version));
    }
    const url = available ? storeUrl : null;
    const result = { url };
    context.waitUntil(cache.put(cacheUrl.href, Response.json(result, {
      headers: { 'Cache-Control': url ? 'public, max-age=3600' : 'public, max-age=300' },
    })).catch(() => {}));
    return Response.json(result, { headers });
  } catch (error) {
    const reason = /^(store|storefront)_http_\d{3}$/.test(error.message) ? error.message : 'store_lookup_failed';
    return Response.json({ url: null, reason }, { headers, status: 503 });
  }
}
