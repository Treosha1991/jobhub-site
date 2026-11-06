const appStoreDownload = document.getElementById('app-store-download');

fetch('/api/app-store-release', { credentials: 'omit' })
  .then(response => response.ok ? response.json() : null)
  .then(status => {
    if (!status?.url) return;
    const badge = appStoreDownload.content.firstElementChild;
    badge.href = status.url;
    appStoreDownload.replaceWith(badge);
  })
  .catch(() => {
    // Leave the App Store badge hidden when its public release cannot be verified.
  });
