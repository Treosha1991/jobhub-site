"""Publish the reviewed Free activation terms alongside the unchanged Store terms.

The iOS 185 client uses /terms.html and the pinned Store version. Keep that
contract while publishing the separate Free version returned by its server.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITION = 'support-free-2026-11-05-v1'


def apply(out, commerce):
    assert out.resolve().parent == ROOT and out.name in ('dist-support-store-review', 'dist-support-onboarding-preview')
    data = json.loads((ROOT / 'assets/support-free-terms.json').read_text(encoding='utf-8'))
    assert data['edition'] == EDITION
    rows = data['languages']
    langs = commerce.LANGS
    assert set(rows) == set(langs) and all(len(rows[lang]) == 5 for lang in langs)
    tr, section = commerce.tr, commerce.section
    free = ''.join(section(tuple(rows[lang][i]['title'] for lang in langs),
                           tuple(rows[lang][i]['body'] for lang in langs),
                           anchor='free' if i == 0 else 'free-' + str(i)) for i in range(5))
    commerce.render('support-free-terms.html',
        ('Подключение Free', 'Free activation', 'Aktywacja Free', 'Підключення Free'),
        ('Бесплатно для работодателя. Работники оплачивают личный доступ в магазине приложений.',
         'Free for employers. Workers pay for personal access through their app store.',
         'Bezpłatnie dla pracodawcy. Pracownicy opłacają osobisty dostęp w sklepie z aplikacjami.',
         'Безкоштовно для роботодавця. Працівники оплачують особистий доступ у магазині застосунків.'),
        free)
    policy_pages = (
        ('support-free-terms.html', ('Free: условия подключения', 'Free activation terms', 'Warunki aktywacji Free', 'Умови підключення Free')),
        ('support-store-terms.html', ('Support 20 / 50 / 100',)*4),
        ('support-refunds.html', ('Отмена и возвраты', 'Cancellation and refunds', 'Anulowanie i zwroty', 'Скасування та повернення')),
        ('privacy.html', ('Конфиденциальность', 'Privacy', 'Prywatność', 'Конфіденційність')),
    )
    for name in ('terms.html', 'support-subscription-terms.html',
                 'support-store-terms.html', 'support-free-terms.html', 'support-refunds.html',
                 'privacy.html', 'support-privacy.html'):
        page = out / name
        html = page.read_text(encoding='utf-8')
        current = 'privacy.html' if name == 'support-privacy.html' else name
        tabs = []
        for path, title in policy_pages:
            active = ' aria-current="page"' if path == current else ''
            tabs.append(f'<a href="/{path}"{active}>{tr(*title)}<span aria-hidden="true">→</span></a>')
        label = tr('Условия и правила', 'Terms and policies', 'Warunki i zasady', 'Умови та правила')
        chooser = (f'<nav class="commerce-policies" aria-labelledby="policy-nav-title">'
                   f'<p id="policy-nav-title">{label}</p><div>{"".join(tabs)}</div></nav>')
        addition = chooser
        if name in ('terms.html', 'support-subscription-terms.html'):
            addition += free
        elif name == 'support-refunds.html':
            free_refunds = section(tuple(rows[lang][3]['title'] for lang in langs),
                                   tuple(rows[lang][3]['body'] for lang in langs), anchor='free')
            html = html.replace('</main>', free_refunds + '</main>', 1)
        hero_end = html.index('</section>', html.index('<section class="hero">')) + len('</section>')
        html = html[:hero_end] + '\n' + addition + '\n' + html[hero_end:]
        html = html.replace('<main ', f'<main data-support-free-edition="{EDITION}" ', 1)
        page.write_text(html, encoding='utf-8')
    acceptance = section(('Как фиксируется согласие', 'How acceptance is recorded', 'Jak zapisujemy zgodę', 'Як фіксується згода'),
        ('Для подключения Free сохраняются аккаунт, одобренная анкета и её версия, версия условий, время и язык принятия. Для покупки сохраняются связь аккаунта с фирмой, выбранный магазин и продукт, версия условий и время подтверждения. Это необходимо для исполнения выбранного доступа и разрешения споров; простое чтение страницы не создаёт покупку и не считается согласием.',
         'Free activation records the account, approved application and its revision, terms version, acceptance time and language. Purchases record the account/company binding, selected store and product, terms version and consent time. These records support the selected access and dispute resolution; merely reading a page neither purchases a subscription nor constitutes consent.',
         'Aktywacja Free zapisuje konto, zatwierdzony wniosek i jego wersję, wersję warunków, czas i język akceptacji. Przy zakupie zapisujemy powiązanie konta z firmą, sklep i produkt, wersję warunków i czas potwierdzenia. Służy to realizacji wybranego dostępu i rozpatrywaniu sporów; samo przeczytanie strony nie tworzy zakupu ani nie oznacza zgody.',
         'Для Free зберігаються акаунт, схвалена анкета та її версія, версія умов, час і мова прийняття. Для купівлі зберігаються зв’язок акаунта з фірмою, магазин і продукт, версія умов та час підтвердження. Це потрібно для надання обраного доступу й вирішення спорів; саме читання сторінки не створює купівлі й не є згодою.'))
    for name in ('privacy.html', 'support-privacy.html'):
        page = out / name
        page.write_text(page.read_text(encoding='utf-8').replace('</main>', acceptance + '</main>', 1), encoding='utf-8')
