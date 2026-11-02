"""Merge the four-language Store addendum into an unpublished site preview only."""
import json
from pathlib import Path

EDITION = 'support-store-2026-10-31-v1'
ROOT = Path(__file__).resolve().parents[1]


def apply(out, commerce):
    assert out.resolve() == (ROOT / 'dist-support-store-review').resolve()
    data = json.loads((ROOT / 'assets' / 'support-store-terms.json').read_text(encoding='utf-8'))
    assert data['edition'] == EDITION
    tr, section, paragraph = commerce.tr, commerce.section, commerce.paragraph
    languages = commerce.LANGS
    rows = data['languages']
    full = ''.join(section(tuple(rows[lang][index]['title'] for lang in languages),
                           tuple(rows[lang][index]['body'] for lang in languages))
                   for index in range(3))
    privacy = section(tuple(rows[lang][-1]['title'] for lang in languages),
                      tuple(rows[lang][-1]['body'] for lang in languages))
    intro = ('Правила покупок в App Store и Google Play. Применяются после публикации и принятия перед покупкой. Продажи ещё не открыты.',
             'App Store and Google Play purchase rules. Apply after publication and pre-purchase acceptance. Sales have not opened.',
             'Zasady zakupów w App Store i Google Play. Obowiązują po publikacji i akceptacji przed zakupem. Sprzedaż nie została uruchomiona.',
             'Правила покупок в App Store і Google Play. Діють після публікації й прийняття перед купівлею. Продажі ще не відкрито.')
    commerce.render('support-store-terms.html',
        ('Покупки в магазинах приложений', 'App store purchases', 'Zakupy w sklepach z aplikacjami', 'Покупки в магазинах застосунків'),
        intro, full + privacy)
    scope = section(('Какой канал покупки вы выбрали?', 'Which purchase channel did you choose?',
                     'Który kanał zakupu wybierasz?', 'Який канал купівлі ви обрали?'),
        ('Для покупок в App Store и Google Play действуют правила магазинов ниже. Они имеют приоритет над отличающимися условиями веб-оплаты: магазин определяет цену, налоги, пробный период, сроки смены пакета и возврат. Общие условия использования ПО и обязательные права покупателя сохраняются. Веб-оплата через Paddle ещё не включена.',
         'App Store and Google Play purchases use the store rules below. These take precedence over differing web-payment terms: the store determines the price, taxes, trial, package-change timing and refunds. General software-use terms and mandatory buyer rights remain. Paddle web payments are not enabled.',
         'Zakupy w App Store i Google Play podlegają poniższym zasadom sklepów. Mają one pierwszeństwo przed odmiennymi warunkami płatności internetowych: sklep określa cenę, podatki, okres próbny, terminy zmian pakietu i zwroty. Ogólne warunki korzystania z oprogramowania i obowiązkowe prawa kupującego pozostają. Płatności internetowe Paddle nie są włączone.',
         'Для покупок в App Store і Google Play діють наведені нижче правила магазинів. Вони мають пріоритет перед відмінними умовами веб-оплати: магазин визначає ціну, податки, пробний період, строки зміни пакета й повернення. Загальні умови користування ПЗ та обов’язкові права покупця зберігаються. Веб-оплату Paddle ще не ввімкнено.'))
    pricing = '<section class="section-card" id="store-prices"><h2>' + tr(
        'App Store и Google Play', 'App Store and Google Play', 'App Store i Google Play', 'App Store і Google Play') + '</h2>'
    pricing += '<div class="commerce-plans">'
    for n, price in ((20, 249), (50, 449), (100, 749)):
        pricing += '<article class="commerce-plan"><h3>Support ' + str(n) + '</h3><p class="commerce-price">' + str(price) + ' <span>PLN</span></p>'
        pricing += paragraph(('в месяц, с налогами для Польши', 'per month, including Polish tax',
                              'miesięcznie, z podatkami dla Polski', 'на місяць, з податками для Польщі'))
        pricing += paragraph((f'Одна проверенная фирма, до {n} активных работников. Доступ работников включён.',
                              f'One approved company, up to {n} active workers. Worker access is included.',
                              f'Jedna zweryfikowana firma, do {n} aktywnych pracowników. Dostęp pracowników w cenie.',
                              f'Одна перевірена фірма, до {n} активних працівників. Доступ працівників включено.')) + '</article>'
    pricing += '</div>' + paragraph(('График, проверка часов, рабочие чаты, задачи и объявления, учёт транспорта и жилья. Выгрузка CSV доступна в веб-кабинете.',
                                    'Schedules, hours review, work chats, tasks and announcements, transport and housing records. CSV export is available in the web workspace.',
                                    'Grafik, weryfikacja godzin, czaty służbowe, zadania i ogłoszenia, ewidencja transportu i zakwaterowania. Eksport CSV jest dostępny w panelu internetowym.',
                                    'Графік, перевірка годин, робочі чати, завдання й оголошення, облік транспорту та житла. Експорт CSV доступний у вебкабінеті.'))
    pricing += paragraph(('В других странах действует локальная цена магазина. Окончательные валюта, сумма и период показываются до подтверждения покупки.',
                                    'Other countries use the localized store price. Final currency, amount and period are shown before purchase confirmation.',
                                    'W innych krajach obowiązuje lokalna cena sklepu. Waluta, kwota i okres są widoczne przed potwierdzeniem zakupu.',
                                    'В інших країнах діє локальна ціна магазину. Остаточні валюта, сума й період показуються до підтвердження купівлі.')) + '</section>'
    pricing += section(('Личная подписка работника — только в Custom', 'Personal worker subscription — only in Custom', 'Osobista subskrypcja pracownika — tylko w Custom', 'Особиста підписка працівника — лише в Custom'),
                      tuple(rows[lang][1]['body'] for lang in languages))
    web_heading = '<details class="section-card"><summary>' + tr('Отдельные условия веб-оплаты — пока недоступна', 'Separate web-payment terms — not yet available',
                              'Odrębne warunki płatności internetowych — jeszcze niedostępne', 'Окремі умови веб-оплати — поки недоступна') + '</summary>'
    for name, addition in (
        ('terms.html', scope + full),
        ('support-subscription-terms.html', scope + full + web_heading),
        ('support-pricing.html', scope + pricing + web_heading),
        ('support-refunds.html', scope + full + web_heading),
        ('privacy.html', privacy), ('support-privacy.html', privacy)):
        page = out / name
        html = page.read_text(encoding='utf-8')
        hero_end = html.index('</section>', html.index('<section class="hero">')) + len('</section>')
        html = html[:hero_end] + '\n' + addition + '\n' + html[hero_end:]
        if name in ('support-pricing.html', 'support-subscription-terms.html', 'support-refunds.html'):
            html = html.replace('</main>', '</details></main>', 1)
        # The earlier web text predates worker-paid Custom. Keep its blanket
        # worker-coverage assertion explicitly scoped to standard company plans.
        for before, after in (
            ('Для участия в фирме работнику не нужна дополнительная обязательная платная подписка.',
             'В стандартных пакетах 20/50/100 работнику не нужна дополнительная платная подписка.'),
            ('Workers do not need an additional mandatory paid subscription to participate.',
             'Workers covered by standard 20/50/100 company packages do not need an additional paid subscription.'),
            ('Udział pracownika nie wymaga dodatkowej obowiązkowej płatnej subskrypcji.',
             'W standardowych pakietach firmy 20/50/100 pracownik nie potrzebuje dodatkowej płatnej subskrypcji.'),
            ('Працівнику не потрібна додаткова обов’язкова платна підписка для участі.',
             'У стандартних пакетах фірми 20/50/100 працівнику не потрібна додаткова платна підписка.')):
            html = html.replace(before, after)
        html = html.replace('<main id="main"', f'<main data-support-store-edition="{EDITION}" id="main"')
        page.write_text(html, encoding='utf-8')
