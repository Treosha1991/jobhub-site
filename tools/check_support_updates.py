"""Check the generated cutover artifact, including HLS media dependencies."""
import hashlib
import argparse
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, default=ROOT / 'dist-support')
OUT = parser.parse_args().root.resolve()


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
presentation = (OUT / 'support-presentation.html').read_text(encoding='utf-8')
assert presentation.count('class="support-step-number"') == 3
assert 'data-slide-' not in presentation and 'data-slide=' not in presentation
assert '/employer/connect-company/' in presentation
pricing = (OUT / 'support-pricing.html').read_text(encoding='utf-8')
assert 'commerce-nav' in pricing and 'data-catalog-redirect' not in pricing
assert 'id="free"' in pricing and pricing.count('class="commerce-plan"') == 3
assert all(f'/employer/plans/?package={seats}' in pricing for seats in (20, 50, 100))
assert 'PLN' not in pricing and 'commerce-draft' not in pricing
downloads = (OUT / 'index.html').read_text(encoding='utf-8').split('id="download"', 1)[1].split('</section>', 1)[0]
assert 'apps.microsoft.com/detail/9P0Q581Q363X' in downloads
assert 'apps.apple.com/' not in downloads and 'play.google.com/store/apps' not in downloads
if (OUT / 'support-free-terms.html').exists():
    refunds = (OUT / 'support-refunds.html').read_text(encoding='utf-8')
    assert 'class="commerce-policies"' in refunds
    assert 'href="/support-refunds.html" aria-current="page"' in refunds

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
    assert not re.search(r'<(?:form|iframe)\b|paddle|/assets/app\.js', source, re.I), page
    assert not re.search(r'\b(?:PLN|Custom)\b|(?<!\d)9[,.]99(?!\d)', source, re.I), page
    assert not re.search(
        r'commerce-draft|testflight|sandbox|продажи (ещё )?не открыты|оплата недоступна|'
        r'sales have not opened|payment is unavailable|sprzedaż nie (?:jest|została)|'
        r'продажі (?:ще )?не відкрито',
        source, re.I,
    ), page
assert not (OUT / 'vacancies.html').exists()
headers = (OUT / '_headers').read_text(encoding='utf-8')
assert "media-src 'self' blob:" in headers and "worker-src 'self' blob:" in headers
assert headers.count('Content-Type: application/vnd.apple.mpegurl') == 5
assert headers.count('Content-Type: text/vtt; charset=utf-8') == 5
print(f'PASS: 2 Support articles, 3 video pages, 5 languages, {assets} unchanged media files; cutover boundary retained.')
