"""Render the owner's four-language Support publication candidate.

This generates static copy only. It does not publish or create a checkout.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ('ru', 'en', 'pl', 'uk')


def tr(*values):
    assert len(values) == 4
    return ''.join(f'<span class="lang-{lang}">{escape(value)}</span>'
                   for lang, value in zip(LANGS, values))


NAV = [
    ('support-pricing.html', ('Тарифы', 'Pricing', 'Cennik', 'Тарифи')),
    ('support-subscription-terms.html', ('Условия подписки', 'Subscription terms', 'Warunki subskrypcji', 'Умови підписки')),
    ('support-refunds.html', ('Отмена и возвраты', 'Cancellation and refunds', 'Anulowanie i zwroty', 'Скасування та повернення')),
    ('support-privacy.html', ('Данные и конфиденциальность', 'Data and privacy', 'Dane i prywatność', 'Дані та конфіденційність')),
]
PUBLIC_NAV = []
EDITION = 'support-only-web-2026-10-26-v1'
PUBLIC_INDEXABLE = False
IDENTITY = ('Поставщик ПО: Andrei Trakaila, физическое лицо без зарегистрированной фирмы, Польша. Почтовый адрес: Lawendowa 81A/8, 15-642 Bialystok, Poland.',
            'Software supplier: Andrei Trakaila, an individual without a registered company, Poland. Postal address: Lawendowa 81A/8, 15-642 Bialystok, Poland.',
            'Dostawca oprogramowania: Andrei Trakaila, osoba fizyczna bez zarejestrowanej firmy, Polska. Adres pocztowy: Lawendowa 81A/8, 15-642 Bialystok, Poland.',
            'Постачальник ПЗ: Andrei Trakaila, фізична особа без зареєстрованої фірми, Польща. Поштова адреса: Lawendowa 81A/8, 15-642 Bialystok, Poland.')


def paragraph(values):
    return '<p>' + tr(*values) + '</p>'


def section(title, *paragraphs, anchor=None):
    attr = f' id="{escape(anchor)}"' if anchor else ''
    return f'<section class="section-card"{attr}><h2>{tr(*title)}</h2>' + ''.join(paragraph(p) for p in paragraphs) + '</section>'


def render(file, title, intro, content):
    links = []
    for name, label in PUBLIC_NAV + NAV:
        active = ' aria-current="page"' if name == file else ''
        links.append(f'<a href="/{name}"{active} data-nav>{tr(*label)}</a>')
    nav = ''.join(links)
    buttons = ''.join(f'<button type="button" class="lang-btn" data-set-lang="{lang}">{lang.upper()}</button>' for lang in LANGS)
    robots = '' if PUBLIC_INDEXABLE and file != '404.html' else '<meta name="robots" content="noindex,nofollow">'
    source = f'''<!doctype html>
<html lang="ru" data-lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<title>{escape(title[0])} — JobHub Support</title>
<link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/styles.css?v=20260217j">
<link rel="stylesheet" href="/assets/support-commerce.css?v=20261106-contact-copy">
<script defer src="/assets/support-site.js?v=20261106-contact-copy"></script>
</head><body class="commerce-review">
<a class="commerce-skip" href="#main">{tr('К содержанию', 'Skip to content', 'Przejdź do treści', 'До вмісту')}</a>
<header class="site-header"><div class="wrap commerce-header"><a class="brand" href="/" data-nav>JobHub Support</a><div class="lang-inline">{buttons}</div></div>
<nav class="wrap commerce-nav" aria-label="JobHub Support">{nav}</nav></header>
<main id="main" class="wrap">
<section class="hero"><span class="badge">JobHub Support</span><h1>{tr(*title)}</h1>{paragraph(intro) if intro else ''}</section>
{content}
</main><footer class="wrap"><p>{tr(*IDENTITY)}</p><p><a href="mailto:admin@jobhub.today" data-no-lang>admin@jobhub.today</a></p><div class="commerce-footer">{nav}</div>
<p><a href="/terms.html">{tr('Условия Support', 'Support terms', 'Warunki Support', 'Умови Support')}</a> · <a href="/contact.html">{tr('Поддержка', 'Contact support', 'Wsparcie', 'Підтримка')}</a> · <a href="/help.html">{tr('Помощь', 'Help', 'Pomoc', 'Допомога')}</a></p>
<p><a href="/privacy.html">{tr('Политика JobHub Support', 'JobHub Support privacy', 'Prywatność JobHub Support', 'Політика JobHub Support')}</a> · <a href="/data-deletion.html">{tr('Удаление данных', 'Data deletion', 'Usuwanie danych', 'Видалення даних')}</a></p></footer>
</body></html>'''
    (ROOT / file).write_text(source, encoding='utf-8')


def pricing(onboarding_origin):
    def action(path, label, *, primary=False):
        href = escape(f"{onboarding_origin}{path}&lang=ru", quote=True)
        css = 'btn btn-primary' if primary else 'btn btn-secondary'
        return f'<a class="{css}" href="{href}" data-onboarding-link>{label}<span aria-hidden="true">→</span></a>'

    title = ('Тарифы Support', 'Support plans', 'Pakiety Support', 'Тарифи Support')
    free_label = tr('Бесплатно для работодателя', 'Free for employers',
                    'Bezpłatnie dla pracodawcy', 'Безкоштовно для роботодавця')
    free_intro = paragraph((
        'Вы управляете фирмой бесплатно. Каждый работник оплачивает личную подписку, чтобы подключить свой аккаунт к фирме.',
        'Manage your company for free. Each worker pays for a personal subscription to connect their account to your company.',
        'Zarządzaj firmą bez opłat. Każdy pracownik opłaca subskrypcję osobistą, aby połączyć swoje konto z firmą.',
        'Керуйте фірмою безкоштовно. Кожен працівник оплачує особисту підписку, щоб підключити свій акаунт до фірми.'))
    worker_price = paragraph((
        'Ориентир для работника — 8,72 € в месяц без учёта налогов. Итоговую цену магазин покажет перед покупкой. Первый месяц бесплатный, если магазин предложит пробный период. Затем подписка продлевается автоматически до отмены в магазине.',
        'Estimated worker price: €8.72 per month before tax. The store shows the final price before purchase. The first month is free if the store offers a trial. The subscription then renews automatically until cancelled in the store.',
        'Orientacyjna cena dla pracownika to 8,72 € miesięcznie bez podatków. Sklep pokaże ostateczną cenę przed zakupem. Pierwszy miesiąc jest bezpłatny, jeśli sklep oferuje okres próbny. Subskrypcja odnawia się automatycznie do anulowania w sklepie.',
        'Орієнтовна ціна для працівника — 8,72 € на місяць без урахування податків. Магазин покаже остаточну ціну перед купівлею. Перший місяць безкоштовний, якщо магазин запропонує пробний період. Далі підписка поновлюється автоматично до скасування в магазині.'))
    free_button = action('/employer/connect-company/?package=free',
        tr('Подключить Free', 'Get started with Free', 'Wybierz Free', 'Підключити Free'), primary=True)
    free_card = (f'<section id="free" class="section-card catalog-free" aria-labelledby="free-title">'
                 f'<h2 id="free-title">Free</h2><p class="catalog-free-price">{free_label}</p>'
                 f'<div class="catalog-free-copy">{free_intro}{worker_price}</div>{free_button}</section>')

    # Store catalogue estimates excluding Polish VAT, rounded at the 5 Nov 2026 NBP rate.
    cards = []
    for seats, price in ((20, 46), (50, 83), (100, 139)):
        capacity = paragraph((f'До {seats} одновременно активных работников',
            f'Up to {seats} concurrently active workers', f'Do {seats} jednocześnie aktywnych pracowników',
            f'До {seats} одночасно активних працівників'))
        amount = tr(f'{price} € в месяц', f'€{price} per month',
                    f'{price} € miesięcznie', f'{price} € на місяць')
        coverage = paragraph(('Работодатель оплачивает пакет. Личный доступ работников включён.',
            'The employer pays for the plan. Personal access for workers is included.',
            'Pracodawca opłaca pakiet. Osobisty dostęp pracowników jest w cenie.',
            'Роботодавець оплачує пакет. Особистий доступ працівників включено.'))
        choose = tr(f'Выбрать Support {seats}', f'Choose Support {seats}',
                    f'Wybierz Support {seats}', f'Обрати Support {seats}')
        cards.append(f'<article class="commerce-plan"><h3>Support {seats}</h3>{capacity}'
                     f'<p class="commerce-price">{amount}</p>{coverage}'
                     f'{action(f"/employer/plans/?package={seats}", choose)}</article>')

    paid_title = tr('Платные тарифы для компании', 'Paid plans for companies',
                    'Płatne pakiety dla firm', 'Платні тарифи для компанії')
    paid_intro = paragraph((
        'Оформите пакет в App Store или Google Play. Подписка привязана к вашему аккаунту JobHub Support и действует на всех устройствах.',
        'Subscribe through the App Store or Google Play. The plan is linked to your JobHub Support account and works on all your devices.',
        'Kup pakiet w App Store lub Google Play. Subskrypcja jest przypisana do konta JobHub Support i działa na wszystkich Twoich urządzeniach.',
        'Оформіть пакет в App Store або Google Play. Підписка прив’язана до вашого акаунта JobHub Support і діє на всіх пристроях.'))
    price_note = paragraph((
        'Ориентировочные цены в евро без учёта налогов. Итоговую цену в местной валюте с применимыми налогами магазин покажет перед покупкой.',
        'Estimated prices in euros before tax. Your store shows the final price in your local currency, including applicable taxes, before purchase.',
        'Orientacyjne ceny w euro bez podatków. Przed zakupem sklep pokaże ostateczną cenę w lokalnej walucie z uwzględnieniem należnych podatków.',
        'Орієнтовні ціни в євро без урахування податків. Остаточну ціну в місцевій валюті з відповідними податками магазин покаже перед купівлею.'))
    paid = (f'<section id="paid-plans" class="catalog-paid" aria-labelledby="paid-title">'
            f'<h2 id="paid-title">{paid_title}</h2>{paid_intro}'
            f'<div id="store-prices" class="commerce-plans">{"".join(cards)}</div>{price_note}</section>')
    render('support-pricing.html', title, None, free_card + paid)


def terms():
    rows = [
      (('1. Поставщик и предмет', '1. Supplier and scope', '1. Dostawca i zakres', '1. Постачальник і предмет'), IDENTITY,
       ('Платная подписка Support предоставляет доступ к ПО для внутренних операций вашей организации в пределах пакета и назначенных прав. Пакеты описаны на странице тарифов.',
        'A paid Support subscription provides software for your organisation’s internal operations within your plan limits and assigned permissions. See the pricing page for available plans.',
        'Płatna subskrypcja Support zapewnia dostęp do oprogramowania do wewnętrznych działań organizacji w ramach pakietu i nadanych uprawnień. Pakiety opisuje cennik.',
        'Платна підписка Support надає доступ до ПЗ для внутрішніх операцій вашої організації в межах пакета та призначених прав. Пакети описано на сторінці тарифів.')),
      (('2. Анкета и договор', '2. Application and agreement', '2. Zgłoszenie i umowa', '2. Анкета та договір'),
       ('Заявитель предоставляет достоверные контактные сведения и подтверждает полномочия действовать для организации. Ручное одобрение анкеты само по себе не означает оплату или активную подписку. До покупки показываются версия условий, пакет, сумма, налоги и автопродление; согласие фиксируется отдельно.',
        'Applicants provide accurate contact details and confirm authority to act for the organisation. Manual application approval alone is not payment or an active subscription. The terms edition, package, amount, taxes and renewal are shown before purchase; acceptance is recorded separately.',
        'Wnioskodawca podaje prawdziwe dane kontaktowe i potwierdza umocowanie do działania dla organizacji. Ręczna akceptacja zgłoszenia nie oznacza płatności ani aktywnej subskrypcji. Przed zakupem widoczne są wersja warunków, pakiet, kwota, podatki i odnowienie; zgoda jest rejestrowana osobno.',
        'Заявник надає достовірні контакти й підтверджує повноваження діяти для організації. Схвалення анкети саме по собі не означає оплати чи активної підписки. До купівлі показують редакцію умов, пакет, суму, податки й автоподовження; згоду фіксують окремо.')),
      (('3. Платёж и период', '3. Payment and period', '3. Płatność i okres', '3. Платіж і період'),
       ('Платная подписка оформляется в App Store или Google Play. Перед покупкой магазин показывает итоговую цену и период. Доступ открывается после подтверждения покупки.',
        'Subscribe through the App Store or Google Play. The store shows the final price and billing period before purchase. Access starts once the purchase is verified.',
        'Subskrypcję kupisz w App Store lub Google Play. Przed zakupem sklep pokazuje ostateczną cenę i okres rozliczeniowy. Dostęp otwiera się po weryfikacji zakupu.',
        'Платну підписку оформлюють в App Store або Google Play. Перед купівлею магазин показує остаточну ціну та період оплати. Доступ відкривається після підтвердження купівлі.')),
      (('4. Продление и отмена', '4. Renewal and cancellation', '4. Odnowienie i anulowanie', '4. Поновлення та скасування'),
       ('Подписка продлевается автоматически до отмены. Отключить продление можно в магазине, где оформлена подписка.',
        'The subscription renews automatically until cancelled. Turn off renewal in the store where you subscribed.',
        'Subskrypcja odnawia się automatycznie do anulowania. Odnowienie wyłączysz w sklepie, w którym wykupiono subskrypcję.',
        'Підписка поновлюється автоматично до скасування. Вимкнути поновлення можна в магазині, де оформлено підписку.')),
      (('5. Изменение пакета', '5. Changing package', '5. Zmiana pakietu', '5. Зміна пакета'),
       ('Магазин показывает цену и дату вступления изменений в силу до подтверждения смены пакета.',
        'The store shows the price and effective date before you confirm a plan change.',
        'Przed potwierdzeniem zmiany pakietu sklep pokazuje cenę i datę wejścia zmiany w życie.',
        'Магазин показує ціну та дату набрання зміною чинності до підтвердження зміни пакета.')),
      (('6. Неудачная оплата', '6. Failed payment', '6. Nieudana płatność', '6. Невдала оплата'),
       ('Если платёж не прошёл, проверьте подписку и способ оплаты в том же магазине.',
        'If a payment fails, check your subscription and payment method in the same store.',
        'Jeśli płatność się nie powiodła, sprawdź subskrypcję i metodę płatności w tym samym sklepie.',
        'Якщо платіж не пройшов, перевірте підписку та спосіб оплати в тому самому магазині.')),
      (('7. Рабочие данные и допустимое использование', '7. Work data and permitted use', '7. Dane służbowe i dozwolone użycie', '7. Робочі дані та дозволене використання'),
       ('Организация отвечает за законное основание внесения сведений о работниках, свои инструкции, достоверность часов и своевременный отзыв прав. Псевдоним не гарантирует анонимность. Запрещены чужие данные без основания, незаконный контент, обход доступа и передача кадровых документов через обычный чат.',
        'The organisation is responsible for lawful grounds for worker data, its instructions, accurate hours and timely access revocation. A nickname does not guarantee anonymity. Unauthorised third-party data, unlawful content, access bypass and personnel documents sent through ordinary chat are prohibited.',
        'Organizacja odpowiada za podstawę prawną danych pracowników, swoje polecenia, poprawność godzin i terminowe cofanie uprawnień. Pseudonim nie gwarantuje anonimowości. Zakazane są cudze dane bez podstawy, treści nielegalne, obchodzenie dostępu i przesyłanie akt kadrowych zwykłym czatem.',
        'Організація відповідає за законну підставу даних працівників, свої інструкції, точність годин і своєчасне відкликання прав. Псевдонім не гарантує анонімності. Заборонені чужі дані без підстави, незаконний вміст, обхід доступу й кадрові документи у звичайному чаті.')),
      (('8. Обработка данных и окончание доступа', '8. Data processing and access ending', '8. Przetwarzanie danych i koniec dostępu', '8. Обробка даних і завершення доступу'),
       ('До обработки реальных рабочих данных оформляются необходимые договорные условия обработки данных, перечень обработчиков, сроки хранения и порядок возврата/удаления данных. Подписка сама по себе не включает кадровые документы. Окончание оплаты, архивирование работника и удаление данных — разные действия. До окончания доступа выгрузите доступные таблицы; запрос о данных направляется в поддержку.',
        'Before real work data is processed, the required processing terms, subprocessors, retention periods and return/deletion procedure must be agreed. A subscription alone does not enable personnel documents. Payment expiry, archiving workers and deleting data are separate actions. Export available tables before access ends; send data requests to support.',
        'Przed przetwarzaniem rzeczywistych danych służbowych wymagane są uzgodnione warunki powierzenia, podwykonawcy, okresy przechowywania i procedura zwrotu/usunięcia. Sama subskrypcja nie włącza akt kadrowych. Koniec opłaty, archiwizacja pracownika i usunięcie danych są odrębne. Przed końcem dostępu wyeksportuj dostępne tabele; sprawy danych kieruj do wsparcia.',
        'До обробки реальних робочих даних погоджують потрібні договірні умови обробки, обробників, строки зберігання й порядок повернення/видалення. Сама підписка не вмикає кадрові документи. Завершення оплати, архівування працівника й видалення даних — різні дії. До завершення доступу експортуйте доступні таблиці; запити щодо даних надсилайте підтримці.')),
      (('9. Поддержка, изменения и ответственность', '9. Support, changes and responsibility', '9. Wsparcie, zmiany i odpowiedzialność', '9. Підтримка, зміни та відповідальність'),
       ('Вопросы и претензии: admin@jobhub.today. Укажите аккаунт, фирму и описание проблемы; не присылайте пароль или полные реквизиты карты. Гарантии круглосуточной поддержки, безотказности, трудоустройства, зарплаты или юридической правильности кадровых решений не предоставляются. Изменения цены и существенных условий доводятся заранее; уже оплаченный период не пересчитывается задним числом.',
        'Questions and complaints: admin@jobhub.today. Include your account, organisation and issue; do not send passwords or full card details. No round-the-clock support, uninterrupted operation, employment, wage or legally correct HR-decision guarantee is offered. Price and material terms changes are communicated in advance; paid periods are not repriced retrospectively.',
        'Pytania i reklamacje: admin@jobhub.today. Podaj konto, organizację i opis problemu; nie wysyłaj hasła ani pełnych danych karty. Nie oferujemy gwarancji wsparcia całodobowego, nieprzerwanego działania, zatrudnienia, wynagrodzenia ani prawnej poprawności decyzji kadrowych. Zmiany cen i istotnych warunków są komunikowane wcześniej; opłacony okres nie jest przeliczany wstecz.',
        'Питання й претензії: admin@jobhub.today. Укажіть акаунт, фірму та проблему; не надсилайте пароль чи повні реквізити картки. Немає гарантій цілодобової підтримки, безперервності, працевлаштування, зарплати чи юридичної правильності кадрових рішень. Про зміни ціни та істотних умов повідомляють заздалегідь; оплачений період не перераховують заднім числом.')),
      (('10. Возвраты и обязательные права', '10. Refunds and mandatory rights', '10. Zwroty i prawa bezwzględnie obowiązujące', '10. Повернення та обов’язкові права'),
       ('Порядок отмены и обращения за возвратом приведён на отдельной странице. Эти условия не исключают обязательные права покупателя и ответственность, которую нельзя исключить законом.',
        'Cancellation and refund requests are explained on the separate page. These terms do not exclude mandatory buyer rights or liability that law does not allow to be excluded.',
        'Zasady anulowania i wniosków o zwrot opisuje osobna strona. Warunki nie wyłączają bezwzględnie obowiązujących praw kupującego ani odpowiedzialności, której nie można wyłączyć prawem.',
        'Порядок скасування та звернення по повернення описано на окремій сторінці. Умови не виключають обов’язкових прав покупця й відповідальності, яку не можна виключити законом.')),
    ]
    rows += [
      (('11. Право использования и ваши данные', '11. Right of use and your data', '11. Prawo korzystania i Twoje dane', '11. Право використання та ваші дані'),
       ('На оплаченный срок предоставляется ограниченное неисключительное право пользоваться Support для внутренних задач своей организации. Нельзя перепродавать доступ, нарушать чужие права или обходить защиту. Оплата не передаёт права на исходный код. Ваши права на законно внесённые материалы сохраняются; их обработка разрешается только для предоставления услуги и законных обязанностей.',
        'For the paid term you receive a limited, non-exclusive right to use Support for your organisation’s internal tasks. Reselling access, infringing rights and bypassing security are prohibited. Payment does not transfer source-code rights. Your rights in lawfully supplied materials remain yours; processing is limited to service delivery and legal duties.',
        'Na opłacony okres otrzymujesz ograniczone, niewyłączne prawo korzystania z Support do wewnętrznych zadań organizacji. Odsprzedaż dostępu, naruszanie praw i obchodzenie zabezpieczeń są zabronione. Płatność nie przenosi praw do kodu. Zachowujesz prawa do legalnie wprowadzonych materiałów; przetwarzanie ogranicza się do usługi i obowiązków prawnych.',
        'На оплачений строк надається обмежене невиключне право користуватися Support для внутрішніх завдань організації. Заборонені перепродаж доступу, порушення чужих прав і обхід захисту. Оплата не передає прав на код. Ваші права на законно внесені матеріали зберігаються; обробка обмежена наданням послуги й законними обов’язками.')),
      (('12. Прекращение, изменения и применимое право', '12. Termination, changes and applicable law', '12. Zakończenie, zmiany i prawo właściwe', '12. Припинення, зміни та застосовне право'),
       ('Доступ может быть ограничен при существенном нарушении условий, незаконном использовании или угрозе безопасности, в необходимом и соразмерном объёме. Когда допустимо, сообщаем основание и возможность исправления. Это не отменяет прав на законный возврат и получение своих данных. Существенные изменения условий и повышение цены для действующей подписки сообщаются до их применения; покупатель может отменить продление, а требуемое законом согласие запрашивается отдельно.',
        'Access may be restricted to a necessary and proportionate extent for material breach, unlawful use or a security threat. Where permitted, we explain the reason and opportunity to remedy it. Statutory refund and data-retrieval rights remain. Material terms changes and price increases for an existing subscription are communicated before applying; buyers may cancel renewal, and any legally required consent is requested separately.',
        'Dostęp może być ograniczony w niezbędnym i proporcjonalnym zakresie przy istotnym naruszeniu, nielegalnym użyciu lub zagrożeniu bezpieczeństwa. Gdy jest to dopuszczalne, wyjaśniamy powód i możliwość naprawy. Prawa do ustawowego zwrotu i otrzymania danych pozostają. Istotne zmiany warunków i podwyżki są komunikowane przed zastosowaniem; można anulować odnowienie, a zgoda wymagana prawem jest pozyskiwana osobno.',
        'Доступ може бути обмежено в потрібному й пропорційному обсязі за істотного порушення умов, незаконного використання чи загрози безпеці. Коли дозволено, повідомляємо причину й можливість виправлення. Законні права на повернення та отримання даних зберігаються. Про істотні зміни й підвищення ціни повідомляють до застосування; покупець може скасувати подовження, а потрібну законом згоду запитують окремо.'),
       ('К отношениям с поставщиком ПО применяется право Польши с сохранением обязательной защиты, которую предоставляет применимое право покупателя. Обязательные правила о компетентном суде не ограничиваются. Эта редакция применяется только к новым подпискам Support после отдельного принятия до покупки; она не изменяет старые покупки и бесплатный демо-показ.',
        'Polish law governs the software-supplier relationship without removing mandatory protection under the buyer’s applicable law. Mandatory jurisdiction rules are unaffected. This edition applies only to new Support subscriptions after separate pre-purchase acceptance; it does not alter previous purchases or the free demo.',
        'Relację z dostawcą oprogramowania reguluje prawo polskie z zachowaniem obowiązkowej ochrony wynikającej z prawa właściwego kupującego. Bezwzględnie obowiązujące zasady właściwości sądu pozostają. Wersja dotyczy tylko nowych subskrypcji Support po osobnej akceptacji przed zakupem; nie zmienia wcześniejszych zakupów ani bezpłatnego demo.',
        'Відносини з постачальником ПЗ регулює право Польщі зі збереженням обов’язкового захисту за застосовним правом покупця. Обов’язкові правила підсудності не обмежуються. Редакція діє лише для нових підписок Support після окремого прийняття до купівлі; старі покупки та безкоштовне демо не змінюються.')),
    ]
    render(NAV[1][0], NAV[1][1], (
        'Правила подключения, продления и управления доступом JobHub Support.',
        'Rules for activation, renewal and access management in JobHub Support.',
        'Zasady aktywacji, odnawiania i zarządzania dostępem w JobHub Support.',
        'Правила підключення, поновлення й керування доступом JobHub Support.',
    ), ''.join(section(*row) for row in rows))


def refunds():
    intro = ('Управляйте подпиской в магазине, где вы её оформили.',
             'Manage your subscription in the store where you bought it.',
             'Zarządzaj subskrypcją w sklepie, w którym ją kupiono.',
             'Керуйте підпискою в магазині, де ви її оформили.')
    labels = (
        ('Отменить продление', 'Cancel renewal', 'Anuluj odnowienie', 'Скасувати поновлення'),
        ('Запросить возврат', 'Request a refund', 'Poproś o zwrot', 'Запросити повернення'),
    )
    stores = (
        ('App Store', 'https://support.apple.com/118428', 'https://support.apple.com/118223'),
        ('Google Play', 'https://support.google.com/googleplay/answer/7018481',
         'https://support.google.com/googleplay/answer/2479637'),
    )
    cards = []
    for name, cancel, refund in stores:
        actions = ''.join(f'<a class="btn btn-secondary" href="{url}" data-no-lang>{tr(*label)}</a>'
                          for url, label in zip((cancel, refund), labels))
        cards.append(f'<section class="section-card refund-store"><h2>{name}</h2>'
                     f'<div class="actions">{actions}</div></section>')
    rights = section(('Права покупателя', 'Buyer rights', 'Prawa kupującego', 'Права покупця'),
        ('Отмена продления и запрос возврата — отдельные действия. Магазин рассматривает запрос по своим правилам с учётом обязательных прав покупателя.',
         'Cancelling renewal and requesting a refund are separate steps. The store assesses the request under its rules and applicable mandatory buyer rights.',
         'Anulowanie odnowienia i wniosek o zwrot to odrębne działania. Sklep rozpatruje wniosek według swoich zasad z uwzględnieniem bezwzględnie obowiązujących praw kupującego.',
         'Скасування поновлення та запит на повернення — окремі дії. Магазин розглядає запит за своїми правилами з урахуванням обов’язкових прав покупця.'))
    render(NAV[2][0], NAV[2][1], intro, '<div class="refund-stores">' + ''.join(cards) + '</div>' + rights)


def privacy():
    rows = [
      (('1. Кто отвечает за данные', '1. Who is responsible for data', '1. Kto odpowiada za dane', '1. Хто відповідає за дані'),
       ('Andrei Trakaila отвечает за собственные цели JobHub: аккаунты, проверку заявки, поддержку, безопасность и подтверждение доступа. Организация определяет цели обработки сведений о своей команде; JobHub обрабатывает эти рабочие данные по её законным инструкциям и отдельным договорным условиям. Никнейм не делает связанные с человеком часы и сообщения анонимными.',
        'Andrei Trakaila is responsible for JobHub’s own account, application-review, support, security and access-verification purposes. The organisation determines purposes for its workforce data; JobHub processes that work data under lawful instructions and separate processing terms. A nickname does not anonymise hours and messages linked to a person.',
        'Andrei Trakaila odpowiada za własne cele JobHub: konta, weryfikację zgłoszeń, wsparcie, bezpieczeństwo i potwierdzenie dostępu. Organizacja określa cele danych swojego zespołu; JobHub przetwarza je na zgodne z prawem polecenia i na podstawie odrębnych warunków powierzenia. Pseudonim nie anonimizuje godzin i wiadomości powiązanych z osobą.',
        'Andrei Trakaila відповідає за власні цілі JobHub: акаунти, перевірку заявки, підтримку, безпеку й підтвердження доступу. Організація визначає цілі даних команди; JobHub обробляє їх за законними інструкціями й окремими договірними умовами. Псевдонім не робить пов’язані з людиною години й повідомлення анонімними.')),
      (('2. Какие данные нужны', '2. Data used', '2. Wykorzystywane dane', '2. Які дані потрібні'),
       ('Подключение: email, представитель, полномочия, контактные и организационные сведения анкеты, решения проверки, версия и время принятия условий. Работа: идентификаторы участников, отображаемые имена, назначенные проекты/смены, часы, решения проверки, рабочие сообщения и журнал действий. Оплата: пакет, ID покупателя/подписки/транзакции, сумма, валюта, даты и статус.',
        'Activation: email, representative, authority, application contact/organisation details, review decisions, terms edition and acceptance time. Operations: member IDs, display names, project/shift assignments, hours, review decisions, work messages and audit records. Billing: package, customer/subscription/transaction IDs, amount, currency, dates and status.',
        'Aktywacja: e-mail, przedstawiciel, umocowanie, dane kontaktowe/organizacji z formularza, decyzje weryfikacji, wersja warunków i czas akceptacji. Praca: ID uczestników, wyświetlane nazwy, projekty/zmiany, godziny, decyzje, wiadomości służbowe i dziennik działań. Płatności: pakiet, ID klienta/subskrypcji/transakcji, kwota, waluta, daty i status.',
        'Підключення: email, представник, повноваження, контактні й організаційні дані анкети, рішення перевірки, редакція та час прийняття умов. Робота: ID учасників, відображувані імена, проєкти/зміни, години, рішення, робочі повідомлення й журнал дій. Оплата: пакет, ID покупця/підписки/транзакції, сума, валюта, дати й статус.')),
      (('3. Данные подписки', '3. Subscription data', '3. Dane subskrypcji', '3. Дані підписки'),
       ('Для подтверждения покупки и предоставления доступа JobHub обрабатывает сведения о продукте, статусе подписки и идентификаторе покупки. Платёжные реквизиты обрабатывает магазин, в котором оформлена подписка.',
        'To verify purchases and provide access, JobHub processes product information, subscription status and a purchase identifier. The store where you subscribed handles payment details.',
        'Aby zweryfikować zakup i zapewnić dostęp, JobHub przetwarza informacje o produkcie, stanie subskrypcji i identyfikatorze zakupu. Dane płatnicze obsługuje sklep, w którym kupiono subskrypcję.',
        'Для підтвердження купівлі та надання доступу JobHub обробляє відомості про продукт, статус підписки й ідентифікатор купівлі. Платіжні реквізити обробляє магазин, де оформлено підписку.')),
      (('4. Цели и основания', '4. Purposes and bases', '4. Cele i podstawy', '4. Цілі та підстави'),
       ('Для договора с вами и действий по вашему запросу до него используется договорное основание. Для контактов представителя фирмы — законный интерес организовать и обслуживать отношения с фирмой. Безопасность, доказательства принятия условий и защита требований опираются на соответствующие законные интересы; обязательный учёт — на закон. Необязательное согласие запрашивается отдельно, когда требуется. Основание рабочих данных определяет организация, а не факт оплаты.',
        'A contract with you and requested pre-contract steps use the contractual basis. Organisation-representative contacts use the legitimate interest in arranging and servicing that relationship. Security, terms-acceptance evidence and claims use relevant legitimate interests; mandatory records use legal duties. Optional consent is requested separately where required. The organisation determines the basis for work data; payment does not establish it.',
        'Umowa z Tobą i działania na Twoje żądanie przed jej zawarciem opierają się na podstawie umownej. Kontakty przedstawiciela organizacji opierają się na uzasadnionym interesie nawiązania i obsługi tej relacji. Bezpieczeństwo, dowody akceptacji i roszczenia mają odpowiednie uzasadnione interesy; obowiązkowe rejestry — obowiązek prawny. Wymagana zgoda opcjonalna jest pozyskiwana osobno. Podstawę danych służbowych określa organizacja, nie płatność.',
        'Для договору з вами й дій на ваш запит до нього застосовують договірну підставу. Для контактів представника фірми — законний інтерес організувати й обслуговувати відносини з фірмою. Безпека, докази прийняття умов і захист вимог мають відповідні законні інтереси; обов’язковий облік — законну підставу. Необов’язкову згоду запитують окремо, коли потрібно. Підставу робочих даних визначає організація, а не оплата.')),
      (('5. Доступ и поставщики', '5. Access and providers', '5. Dostęp i dostawcy', '5. Доступ і постачальники'),
       ('Доступ сотрудников ограничивается организацией, ролью, назначением и правами. При обслуживании подписки сведения могут получать уполномоченная поддержка и инфраструктурные поставщики по общей политике JobHub. При подключении реальных рабочих данных организация заранее получает применимые условия обработки, список обработчиков, сведения о местах обработки и международных передачах. Доступ к таким данным открывается после необходимых договорных подтверждений; эта страница сама по себе DPA не заключает.',
        'Staff access is limited by organisation, role, assignment and permissions. Subscription data may be received by authorised support and infrastructure providers under the general JobHub policy. Before activating real work data, the organisation receives applicable processing terms, subprocessors and information on processing locations and international transfers. Such access opens after required contractual confirmations; this page alone does not conclude a DPA.',
        'Dostęp współpracowników ograniczają organizacja, rola, przydział i uprawnienia. Dane subskrypcji mogą otrzymywać upoważnione wsparcie i dostawcy infrastruktury według ogólnej polityki JobHub. Przed aktywacją rzeczywistych danych organizacja otrzymuje właściwe warunki powierzenia, listę podwykonawców i informacje o miejscach przetwarzania oraz transferach. Dostęp otwiera się po wymaganych potwierdzeniach umownych; ta strona sama nie zawiera DPA.',
        'Доступ співробітників обмежують організація, роль, призначення й права. Дані підписки можуть отримувати уповноважена підтримка й інфраструктурні постачальники за загальною політикою JobHub. До підключення реальних робочих даних організація отримує потрібні умови обробки, перелік обробників, місця обробки й міжнародні передачі. Доступ відкривають після потрібних договірних підтверджень; ця сторінка сама не укладає DPA.')),
      (('6. Хранение и удаление', '6. Retention and deletion', '6. Przechowywanie i usuwanie', '6. Зберігання й видалення'),
       ('Критерии срока: сведения аккаунта — пока обслуживается аккаунт; анкета — пока рассматривается заявка или обслуживается подключение; договорные и платёжные подтверждения — пока необходимы для договора, обязательного учёта или конкретного требования. После отпадения цели данные удаляются или обезличиваются, кроме необходимых законных исключений. Для рабочих данных срок, начало его отсчёта и порядок возврата/удаления, включая резервные копии, организация получает до их приёма. Отмена подписки не равна удалению данных.',
        'Retention criteria: account details while the account is serviced; applications while reviewed or activation is serviced; contract and payment evidence while needed for the contract, mandatory records or a specific claim. When the purpose ends, data is deleted or anonymised subject to necessary lawful exceptions. Before work data is accepted, the organisation receives its retention period, starting event and return/deletion procedure, including backups. Cancellation is not data deletion.',
        'Kryteria okresu: dane konta podczas jego obsługi; zgłoszenie podczas rozpatrywania lub obsługi aktywacji; dowody umowne i płatnicze, dopóki są potrzebne do umowy, obowiązkowych rejestrów lub konkretnego roszczenia. Po ustaniu celu dane są usuwane lub anonimizowane z niezbędnymi wyjątkami prawnymi. Przed przyjęciem danych służbowych organizacja otrzymuje okres, zdarzenie początkowe i procedurę zwrotu/usunięcia, w tym kopii. Anulowanie nie oznacza usunięcia danych.',
        'Критерії строку: дані акаунта — поки він обслуговується; анкета — поки розглядають заявку чи обслуговують підключення; договірні й платіжні докази — поки потрібні для договору, обов’язкового обліку чи конкретної вимоги. Після припинення мети дані видаляють або знеособлюють із потрібними законними винятками. До прийняття робочих даних організація отримує строк, початок його відліку й порядок повернення/видалення, включно з копіями. Скасування підписки не є видаленням даних.')),
      (('7. Права и обращения', '7. Rights and requests', '7. Prawa i wnioski', '7. Права та звернення'),
       ('По применимому закону можно запросить доступ, исправление, удаление, ограничение, переносимость или возразить против обработки. Контакт: admin@jobhub.today. Вопрос о рабочих данных сначала адресуйте своей организации; JobHub помогает в пределах своих обязанностей. Жалобу можно подать в польский UODO или другой компетентный орган.',
        'Applicable law may provide access, correction, erasure, restriction, portability or objection rights. Contact admin@jobhub.today. First address work-data requests to your organisation; JobHub assists within its duties. Complaints may be made to Poland’s UODO or another competent authority.',
        'Prawo właściwe może zapewniać dostęp, sprostowanie, usunięcie, ograniczenie, przenoszenie lub sprzeciw. Kontakt: admin@jobhub.today. W sprawach danych służbowych najpierw zwróć się do swojej organizacji; JobHub pomaga w granicach obowiązków. Skargę można złożyć do UODO lub innego właściwego organu.',
        'За застосовним законом можна запросити доступ, виправлення, видалення, обмеження, перенесення чи заперечити обробку. Контакт: admin@jobhub.today. Питання про робочі дані спочатку адресуйте своїй організації; JobHub допомагає в межах обов’язків. Скаргу можна подати до польського UODO чи іншого компетентного органу.')),
    ]
    rows.append((('8. Настройки страницы и обращения', '8. Page settings and requests', '8. Ustawienia strony i wnioski', '8. Налаштування сторінки та звернення'),
       ('Эти страницы сохраняют выбранный язык в локальном хранилище браузера. Для запросов о данных используйте admin@jobhub.today или страницу удаления данных; при необходимости попросим подтвердить принадлежность аккаунта безопасным способом. Ответ предоставляется в сроки применимого закона. Сведения о применимых гарантиях передачи данных можно запросить по тому же адресу.',
        'These pages save your chosen language in browser local storage. Send data requests to admin@jobhub.today or use the data-deletion page; if needed, we ask you to verify account ownership securely. Responses follow applicable legal deadlines. Information about applicable transfer safeguards may be requested at the same address.',
        'Te strony zapisują wybrany język w lokalnej pamięci przeglądarki. Wnioski dotyczące danych kieruj na admin@jobhub.today lub przez stronę usuwania danych; w razie potrzeby poprosimy o bezpieczne potwierdzenie własności konta. Odpowiedź następuje w terminie określonym prawem. Informacje o właściwych zabezpieczeniach transferów można uzyskać pod tym samym adresem.',
        'Ці сторінки зберігають вибрану мову в локальному сховищі браузера. Запити щодо даних надсилайте на admin@jobhub.today або через сторінку видалення; за потреби попросимо безпечно підтвердити належність акаунта. Відповідь надають у строки застосовного закону. Відомості про застосовні гарантії передачі можна запросити за тією самою адресою.')))
    content = ''.join(section(*row) for row in rows)
    content += '<section class="section-card"><h2>'+tr('Связанные политики', 'Related policies', 'Powiązane polityki', 'Пов’язані політики')+'</h2><p><a href="/privacy.html">JobHub Privacy Policy</a> · <a href="https://uodo.gov.pl/" data-no-lang>UODO</a></p></section>'
    render(NAV[3][0], NAV[3][1], ('Политика самостоятельного сервиса JobHub Support, редакция от 26 октября 2026 года. Описывает аккаунты, подключение организации и рабочие данные. Договор обработки рабочих данных оформляется отдельно.', 'Privacy policy for the independent JobHub Support service, edition dated 26 October 2026. Covers accounts, organisation activation and work data. Work-data processing agreements are concluded separately.', 'Polityka prywatności samodzielnego serwisu JobHub Support, wersja z 26 października 2026. Obejmuje konta, podłączenie organizacji i dane służbowe. Umowa powierzenia danych służbowych jest zawierana osobno.', 'Політика самостійного сервісу JobHub Support, редакція від 26 жовтня 2026 року. Описує акаунти, підключення організації та робочі дані. Договір обробки робочих даних укладається окремо.'), content)


if __name__ == '__main__':
    pricing("https://jobapp-backend-f2u8.onrender.com")
    terms()
    refunds()
    privacy()
    print(f'Rendered 4 Support publication candidates: {EDITION}; prelaunch notice and no checkout retained.')
