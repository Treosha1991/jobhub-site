const appId = 6761860677;
const bundleId = 'today.jobhub.app';

function isSupportRelease(app) {
  if (app.trackId !== appId || app.bundleId !== bundleId
      || app.trackName?.trim().toLowerCase() !== 'jobhub support'
      || !/^\d+\.\d+(\.\d+)?$/.test(app.version)) return false;
  const [major, minor, patch = 0] = app.version.split('.').map(Number);
  return major > 1 || (major === 1 && (minor > 0 || patch >= 6));
}

export async function onRequestGet({ request, waitUntil }) {
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
  try {
    const response = await fetch(lookup, { signal: AbortSignal.timeout(4000) });
    if (!response.ok) return Response.json({ url: null }, { headers, status: 503 });
    const { results } = await response.json();
    const url = results.some(isSupportRelease) ? 'https://apps.apple.com/' + country + '/app/id' + appId : null;
    const result = { url };
    waitUntil(cache.put(cacheUrl.href, Response.json(result, {
      headers: { 'Cache-Control': url ? 'public, max-age=3600' : 'public, max-age=300' },
    })));
    return Response.json(result, { headers });
  } catch {
    return Response.json({ url: null }, { headers, status: 503 });
  }
}
