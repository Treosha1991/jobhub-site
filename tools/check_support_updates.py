"""Check the generated cutover artifact, including HLS media dependencies."""
import hashlib
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist-support'


class Articles(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            self.ids.append(dict(attrs).get('id'))


news = (OUT / 'news.html').read_text(encoding='utf-8')
parsed = Articles()
parsed.feed(news)
assert parsed.ids == ['microsoft-store-2026-10-09', 'support-video-2026-10-08'], parsed.ids
assert all(word not in news.casefold() for word in ('vacanc', 'ваканс', 'credit', 'кредит', 'recruit'))
for page in ('index.html', 'news.html', 'support-presentation.html'):
    source = (OUT / page).read_text(encoding='utf-8')
    assert source.count('id="support-video-player"') == 1, page
    assert '/assets/support-video.js' in source and '/news.html' in source, page

assets = 0
for lang in ('ru', 'en', 'pl', 'uk', 'nl'):
    directory = OUT / 'assets/support-video/20261008' / lang
    playlist = (directory / 'presentation.m3u8').read_text(encoding='utf-8')
    dependencies = re.findall(r'URI="([^"]+)"', playlist)
    dependencies += [line for line in playlist.splitlines() if line and not line.startswith('#')]
    for name in dependencies + ['presentation.m3u8', 'subtitles.vtt', 'poster.jpg']:
        target = directory / name
        original = ROOT / target.relative_to(OUT)
        assert target.is_file() and target.stat().st_size < 25 * 1024 * 1024, target
        assert hashlib.sha256(target.read_bytes()).digest() == hashlib.sha256(original.read_bytes()).digest(), target
        assets += 1
for page in OUT.glob('*.html'):
    source = page.read_text(encoding='utf-8')
    assert not re.search(r'<(?:form|iframe)\b|paddle\.js|/assets/app\.js', source, re.I), page
assert not (OUT / 'vacancies.html').exists()
headers = (OUT / '_headers').read_text(encoding='utf-8')
assert "media-src 'self' blob:" in headers and "worker-src 'self' blob:" in headers
assert headers.count('Content-Type: application/vnd.apple.mpegurl') == 5
assert headers.count('Content-Type: text/vtt; charset=utf-8') == 5
print(f'PASS: 2 Support articles, 3 video pages, 5 languages, {assets} unchanged media files; cutover boundary retained.')
