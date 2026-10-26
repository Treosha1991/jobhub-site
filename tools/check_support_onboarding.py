"""Check presentation/localization and immutable demo export across checkouts."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--mobile', type=Path, required=True)
parser.add_argument('--backend', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'assets/support-presentation-v2/content.json').read_text(encoding='utf-8'))
assert len(data['slides']) == 6
checks = 0
for language in ('ru','en','pl','uk'):
    arb = json.loads((args.mobile / f'lib/l10n/app_{language}.arb').read_text(encoding='utf-8'))
    for index, slide in enumerate(data['slides'],1):
        for field in ('title','body'):
            assert slide[language][field] == arb[f'supportPresentationSlide{index}{field.title()}']
            checks += 1
    for name, text in arb.items():
        if name.startswith(('supportDemo','supportNewcomer','supportCatalog','supportPresentation')) and isinstance(text,str):
            assert text.strip() and '\ufffd' not in text and '???' not in text, (language,name)
mobile_csv = args.mobile / 'assets/support_demo_hours.csv'
backend_csv = args.backend / 'jobs/demo_assets/jobhub-demo-hours.csv'
assert hashlib.sha256(mobile_csv.read_bytes()).digest() == hashlib.sha256(backend_csv.read_bytes()).digest()
for page in (root / 'dist-support').glob('*.html'):
    html = page.read_text(encoding='utf-8')
    assert '\ufffd' not in html and '???' not in html, page.name
print(f'{checks} presentation fields match, 4 localized onboarding catalogs valid, immutable CSV identical.')
