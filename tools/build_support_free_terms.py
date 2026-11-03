"""Publish the reviewed Free activation terms alongside the unchanged Store terms.

The iOS 185 client uses /terms.html and the pinned Store version. Keep that
contract while publishing the separate Free version returned by its server.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITION = 'support-free-2026-11-03-v1'


def apply(out, commerce):
    assert out.resolve() == (ROOT / 'dist-support-store-review').resolve()
    data = json.loads((ROOT / 'assets/support-free-terms.json').read_text(encoding='utf-8'))
    assert data['edition'] == EDITION
    rows = data['languages']
    langs = commerce.LANGS
    assert set(rows) == set(langs) and all(len(rows[lang]) == 6 for lang in langs)
    tr, section, paragraph = commerce.tr, commerce.section, commerce.paragraph
    free = ''.join(section(tuple(rows[lang][i]['title'] for lang in langs),
                           tuple(rows[lang][i]['body'] for lang in langs),
                           anchor='free' if i == 0 else 'free-' + str(i)) for i in range(5))
    testing = section(tuple(rows[lang][5]['title'] for lang in langs),
                      tuple(rows[lang][5]['body'] for lang in langs), anchor='testflight')
    commerce.render('support-free-terms.html',
        ('Подключение Free', 'Free activation', 'Aktywacja Free', 'Підключення Free'),
        ('Для работодателя — 0 PLN. Работники оплачивают личный доступ в магазине.',
         'PLN 0 for the employer. Workers pay for personal access through the store.',
         'Dla pracodawcy 0 PLN. Pracownicy opłacają osobisty dostęp w sklepie.',
         'Для роботодавця — 0 PLN. Працівники оплачують особистий доступ у магазині.'),
        testing + free)
    chooser = '<nav class="commerce-footer" aria-label="' + 'Support' + '">' + ''.join(
        '<a href="' + path + '" data-nav>' + tr(*title) + '</a>' for path, title in (
            ('/support-free-terms.html', ('Free: условия подключения', 'Free activation terms', 'Warunki aktywacji Free', 'Умови підключення Free')),
            ('/support-store-terms.html', ('Support 20 / 50 / 100',)*4),
            ('/support-refunds.html', ('Отмена и возвраты', 'Cancellation and refunds', 'Anulowanie i zwroty', 'Скасування та повернення')),
            ('/privacy.html', ('Конфиденциальность', 'Privacy', 'Prywatność', 'Конфіденційність')))) + '</nav>'
    for name in ('terms.html', 'support-subscription-terms.html', 'support-pricing.html',
                 'support-store-terms.html', 'support-free-terms.html', 'support-refunds.html'):
        page = out / name
        html = page.read_text(encoding='utf-8')
        # On the dedicated Free page the full content already includes this notice.
        addition = chooser + ('' if name == 'support-free-terms.html' else testing)
        if name in ('terms.html', 'support-subscription-terms.html'):
            addition += free
        elif name == 'support-pricing.html':
            html = html.replace(
                tr('Один рабочий кабинет. Выберите лимит своей команды.', 'One workspace. Choose your team limit.',
                   'Jedna przestrzeń robocza. Wybierz limit zespołu.', 'Один робочий кабінет. Виберіть ліміт своєї команди.'),
                tr('Один рабочий кабинет. Выберите, кто оплачивает доступ команды.',
                   'One workspace. Choose who pays for your team’s access.',
                   'Jedna przestrzeń robocza. Wybierz, kto płaci za dostęp zespołu.',
                   'Один робочий кабінет. Виберіть, хто оплачує доступ команди.'),
                1,
            )
            addition += section(('Free — первый вариант для работодателя', 'Free — the first employer option',
                'Free — pierwszy wariant dla pracodawcy', 'Free — перший варіант для роботодавця'),
                tuple(rows[lang][0]['body'] for lang in langs), tuple(rows[lang][1]['body'] for lang in langs), anchor='free')
        elif name == 'support-refunds.html':
            addition += section(tuple(rows[lang][3]['title'] for lang in langs),
                                tuple(rows[lang][3]['body'] for lang in langs), anchor='free')
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
