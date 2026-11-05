"""Merge the four-language Store addendum into an unpublished site preview only."""
import json
from pathlib import Path

EDITION = 'support-store-2026-11-05-v1'
ROOT = Path(__file__).resolve().parents[1]


def apply(out, commerce):
    assert out.resolve().parent == ROOT and out.name in ('dist-support-store-review', 'dist-support-onboarding-preview')
    data = json.loads((ROOT / 'assets' / 'support-store-terms.json').read_text(encoding='utf-8'))
    assert data['edition'] == EDITION
    section = commerce.section
    languages = commerce.LANGS
    rows = data['languages']
    full = ''.join(section(tuple(rows[lang][index]['title'] for lang in languages),
                           tuple(rows[lang][index]['body'] for lang in languages))
                   for index in range(3))
    privacy = section(tuple(rows[lang][-1]['title'] for lang in languages),
                      tuple(rows[lang][-1]['body'] for lang in languages))
    intro = ('Условия подписки через App Store и Google Play. Ознакомьтесь с ними перед покупкой.',
             'Subscription terms for App Store and Google Play. Read them before you subscribe.',
             'Warunki subskrypcji w App Store i Google Play. Zapoznaj się z nimi przed zakupem.',
             'Умови підписки через App Store і Google Play. Ознайомтеся з ними перед купівлею.')
    commerce.render('support-store-terms.html',
        ('Покупки в магазинах приложений', 'App store purchases', 'Zakupy w sklepach z aplikacjami', 'Покупки в магазинах застосунків'),
        intro, full + privacy)
    renewal = section(tuple(rows[lang][2]['title'] for lang in languages),
                      tuple(rows[lang][2]['body'] for lang in languages))
    for name, addition in (
        ('terms.html', full),
        ('support-subscription-terms.html', full),
        ('support-refunds.html', renewal),
        ('privacy.html', privacy), ('support-privacy.html', privacy)):
        page = out / name
        html = page.read_text(encoding='utf-8')
        if name == 'support-refunds.html':
            html = html.replace('</main>', addition + '</main>', 1)
        else:
            hero_end = html.index('</section>', html.index('<section class="hero">')) + len('</section>')
            html = html[:hero_end] + '\n' + addition + '\n' + html[hero_end:]
        html = html.replace('<main id="main"', f'<main data-support-store-edition="{EDITION}" id="main"')
        page.write_text(html, encoding='utf-8')
