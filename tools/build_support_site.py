"""Build an allow-listed Support site; legacy source is never copied to dist.

Local preview: python -m http.server 8780 --directory dist-support
Publication must use dist-support, never the repository root.
"""
from html import escape
from pathlib import Path
import json
import shutil
import build_support_commerce as commerce
import build_support_presentation as presentation
import build_support_updates as updates

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist-support'
EDITION = 'support-only-web-2026-10-26-v1'
LANGS = commerce.LANGS
tr, section, paragraph = commerce.tr, commerce.section, commerce.paragraph


def render(name, title, intro, content):
    commerce.render(name, title, intro, content)


def main():
    OUT.mkdir(exist_ok=True)
    # Remove only the verified, dedicated generated directory, never source.
    assert OUT.resolve().parent == ROOT.resolve() and OUT.name == 'dist-support'
    for item in OUT.iterdir():
        if item.is_symlink():
            item.unlink()
            continue
        assert item.resolve().parent == OUT.resolve(), "Refusing a generated path outside dist-support"
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    (OUT / 'assets').mkdir()
    for name in ('styles.css', 'support-commerce.css', 'logo-jobhub.png'):
        shutil.copy2(ROOT / 'assets' / name, OUT / 'assets' / name)
    shutil.copy2(ROOT / 'favicon.ico', OUT / 'favicon.ico')
    # A small language switcher without analytics, advertisements or API calls.
    (OUT / 'assets' / 'support-site.js').write_text('''
const supported = ['ru','en','pl','uk'];
let lang = new URL(location.href).searchParams.get('lang');
try { lang ||= localStorage.getItem('jobhub_lang'); } catch (_) {}
if (!supported.includes(lang)) lang = 'en';
function setLanguage(code) {
  document.documentElement.dataset.lang = code;
  document.documentElement.lang = code;
  try { localStorage.setItem('jobhub_lang', code); } catch (_) {}
  document.querySelectorAll('[data-set-lang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setLang === code)));
  document.querySelectorAll('a[href]').forEach(a => {
    const u = new URL(a.href, location.href);
    if (u.origin === location.origin && !a.hasAttribute('data-no-lang')) { u.searchParams.set('lang', code); a.href = u; }
  });
}
document.querySelectorAll('[data-set-lang]').forEach(b => b.addEventListener('click', () => setLanguage(b.dataset.setLang)));
setLanguage(lang);
''', encoding='utf-8')
    commerce.ROOT = OUT
    commerce.PUBLIC_NAV = [
        ('index.html#download', ('Скачать', 'Download', 'Pobierz', 'Завантажити')),
        ('support-presentation.html', ('Презентация', 'Presentation', 'Prezentacja', 'Презентація')),
        ('news.html', ('Новости', 'News', 'Aktualności', 'Новини')),
    ]
    commerce.pricing(); commerce.terms(); commerce.refunds(); commerce.privacy()
    player = updates.build(ROOT, OUT, commerce)
    presentation.build(ROOT, OUT, commerce, video=player)

    intro = ('Рабочее пространство для команды: проекты, экипажи, смены, часы и рабочая переписка.',
             'A workspace for your team: projects, crews, shifts, working hours and work chats.',
             'Przestrzeń dla zespołu: projekty, brygady, zmiany, godziny pracy i czaty służbowe.',
             'Робочий простір команди: проєкти, екіпажі, зміни, години та робоче листування.')
    actions = '<p><a class="btn" href="/support-presentation.html">'+tr('Посмотреть презентацию', 'Watch the presentation', 'Zobacz prezentację', 'Переглянути презентацію')+'</a> · <a href="/support-pricing.html">'+tr('Тарифы', 'Pricing', 'Cennik', 'Тарифи')+'</a> · <a href="/support-guide.html">'+tr('Как работает Support', 'How Support works', 'Jak działa Support', 'Як працює Support')+'</a></p>'
    downloads = '<section class="section-card support-downloads" id="download"><h2>' + tr(
        'JobHub Support для Windows', 'JobHub Support for Windows',
        'JobHub Support na Windows', 'JobHub Support для Windows') + '</h2>'
    downloads += '<div class="store-badges"><a class="play-store-badge microsoft-store-badge" href="https://apps.microsoft.com/detail/9P0Q581Q363X" target="_blank" rel="noopener noreferrer" data-no-lang>'
    downloads += '<svg width="30" height="30" viewBox="0 0 30 30" aria-hidden="true"><path fill="#f25022" d="M0 0h14v14H0z"/><path fill="#7fba00" d="M16 0h14v14H16z"/><path fill="#00a4ef" d="M0 16h14v14H0z"/><path fill="#ffb900" d="M16 16h14v14H16z"/></svg>'
    downloads += '<span class="play-store-copy"><span class="play-store-kicker">' + tr(
        'Скачать для Windows', 'Download for Windows', 'Pobierz na Windows', 'Завантажити для Windows')
    downloads += '</span><span class="play-store-name">Microsoft Store</span></span></a></div>'
    downloads += paragraph((
        'Установка бесплатна. Доступ к рабочему пространству открывается после приглашения или подключения фирмы.',
        'Installation is free. Workspace access requires an invitation or company activation.',
        'Instalacja jest bezpłatna. Dostęp do przestrzeni roboczej wymaga zaproszenia lub podłączenia firmy.',
        'Встановлення безкоштовне. Доступ до робочого простору відкривається після запрошення або підключення компанії.')) + '</section>'
    capabilities = section(('Работа своей команды', 'Your team’s work', 'Praca własnego zespołu', 'Робота своєї команди'), intro,
        ('Руководитель приглашает менеджеров и работников в их собственные аккаунты, назначает права и ответственных. Работник подтверждает приглашение. Данные ограничены своей организацией и назначенным доступом.',
         'The owner invites managers and workers into their own accounts and assigns permissions and contacts. The worker accepts the invitation. Access is limited to the organisation and assigned scope.',
         'Właściciel zaprasza menedżerów i pracowników na ich własne konta, nadaje uprawnienia i wyznacza osoby odpowiedzialne. Pracownik przyjmuje zaproszenie. Dostęp ogranicza organizacja i nadany zakres.',
         'Керівник запрошує менеджерів і працівників до їхніх акаунтів, призначає права й відповідальних. Працівник підтверджує запрошення. Доступ обмежений організацією та призначеними правами.'))
    hours = section(('От смены до табеля', 'From shift to timesheet', 'Od zmiany do ewidencji', 'Від зміни до табеля'),
        ('Менеджер планирует смены экипажа на объекте. Работник указывает начало, окончание и паузу. Заказчик объекта проверяет часы; его подтверждение окончательное. Подтверждённые часы можно выгрузить в CSV.',
         'The manager plans crew shifts at a project. The worker enters start, end and break. The site customer reviews the hours and gives final approval. Approved hours can be exported as CSV.',
         'Menedżer planuje zmiany brygady na obiekcie. Pracownik wpisuje początek, koniec i przerwę. Klient obiektu sprawdza godziny i zatwierdza je ostatecznie. Zatwierdzone godziny można wyeksportować do CSV.',
         'Менеджер планує зміни екіпажу на об’єкті. Працівник зазначає початок, кінець і перерву. Замовник об’єкта перевіряє години; його підтвердження остаточне. Підтверджені години можна експортувати в CSV.'))
    scope = section(('Что входит в продукт', 'Product scope', 'Zakres produktu', 'Склад продукту'),
        ('JobHub Support — самостоятельное ПО для управления уже существующей командой. На этом сайте не предлагаются поиск работы, доска вакансий, подбор персонала, продажа контактов, реклама или кредиты. Учёт транспорта и жилья означает учёт назначений внутри команды, а не продажу этих услуг.',
         'JobHub Support is independent software for managing an existing team. This site offers no job search, job board, recruitment, contact sales, advertising or credits. Transport and housing features record internal team assignments; they do not sell those services.',
         'JobHub Support to samodzielne oprogramowanie do zarządzania istniejącym zespołem. Ta strona nie oferuje szukania pracy, tablicy ofert, rekrutacji, sprzedaży kontaktów, reklam ani kredytów. Funkcje transportu i zakwaterowania ewidencjonują przydziały zespołu; nie sprzedają tych usług.',
         'JobHub Support — самостійне ПЗ для керування наявною командою. Сайт не пропонує пошук роботи, дошку вакансій, підбір персоналу, продаж контактів, рекламу чи кредити. Функції транспорту й житла обліковують призначення команди, а не продають ці послуги.'))
    render('index.html', ('JobHub Support',)*4, intro, actions+downloads+player+capabilities+hours+scope)
    updates.add_player_assets(OUT / 'index.html')
    render('support-guide.html', ('Как работает Support', 'How Support works', 'Jak działa Support', 'Як працює Support'), intro, capabilities+hours+scope)
    render('help.html', ('Помощь JobHub Support', 'JobHub Support help', 'Pomoc JobHub Support', 'Допомога JobHub Support'), intro, capabilities+hours)
    render('faq.html', ('Вопросы и ответы', 'Questions and answers', 'Pytania i odpowiedzi', 'Запитання й відповіді'), intro, scope+capabilities+hours)
    render('contact.html', ('Поддержка', 'Contact support', 'Kontakt ze wsparciem', 'Підтримка'),
           ('Напишите на admin@jobhub.today. Не отправляйте пароль, код входа или документы личности.',
            'Email admin@jobhub.today. Do not send passwords, login codes or identity documents.',
            'Napisz na admin@jobhub.today. Nie wysyłaj haseł, kodów logowania ani dokumentów tożsamości.',
            'Напишіть на admin@jobhub.today. Не надсилайте пароль, код входу чи документи особи.'), '')
    deletion = section(('Удаление аккаунта', 'Account deletion', 'Usunięcie konta', 'Видалення акаунта'),
        ('В приложении откройте «Мой аккаунт» → «Удалить аккаунт» и подтвердите запрос паролем или кодом. Можно также написать на admin@jobhub.today с адреса аккаунта: попросим безопасно подтвердить владение. Не присылайте пароль.',
         'In the app, open My account → Delete account and confirm with your password or a code. You can also email admin@jobhub.today from your account address; we ask you to verify ownership securely. Do not send a password.',
         'W aplikacji otwórz Moje konto → Usuń konto i potwierdź hasłem lub kodem. Możesz też napisać na admin@jobhub.today z adresu konta; poprosimy o bezpieczne potwierdzenie własności. Nie przesyłaj hasła.',
         'У застосунку відкрийте «Мій акаунт» → «Видалити акаунт» і підтвердьте паролем або кодом. Також можна написати на admin@jobhub.today з адреси акаунта: попросимо безпечно підтвердити володіння. Не надсилайте пароль.'),
        ('Деактивация входа и удаление личного профиля не отменяют законные обязанности организации хранить рабочий табель и историю решений. Часть сведений может сохраняться по закону или для защиты прав; запросы о рабочих данных направляются также вашей организации. Отмена подписки и удаление аккаунта — отдельные действия.',
         'Deactivating sign-in and deleting a personal profile do not override an organisation’s lawful duties to retain timesheets and decision history. Some information may be retained by law or to protect rights; direct work-data requests also to your organisation. Cancelling a subscription and deleting an account are separate actions.',
         'Dezaktywacja logowania i usunięcie profilu nie znoszą zgodnych z prawem obowiązków organizacji dotyczących ewidencji czasu i historii decyzji. Część danych może pozostać z obowiązku prawnego lub dla ochrony praw; wnioski o dane służbowe kieruj także do organizacji. Anulowanie subskrypcji i usunięcie konta to osobne działania.',
         'Деактивація входу й видалення профілю не скасовують законних обов’язків організації зберігати табель та історію рішень. Частину даних можуть зберігати за законом або для захисту прав; запити щодо робочих даних адресуйте також організації. Скасування підписки й видалення акаунта — окремі дії.'))
    render('data-deletion.html', ('Удаление данных', 'Data deletion', 'Usuwanie danych', 'Видалення даних'), ('JobHub Support',)*4, deletion)
    # Canonical general paths are the same independent-product policies, not
    # the old job-board terms. Copies avoid a redirect to an outdated document.
    shutil.copy2(OUT / 'support-privacy.html', OUT / 'privacy.html')
    general = section(('Аккаунт и допустимое использование', 'Account and acceptable use', 'Konto i dozwolone użycie', 'Акаунт і допустиме використання'),
        ('Используйте свой аккаунт, храните данные входа в тайне, указывайте достоверные контакты и не размещайте незаконные материалы. Доступ к данным фирмы появляется только после назначения прав и подтверждения приглашения. Руководитель отвечает за законность обработки данных своей команды. Блокирование злоупотреблений не отменяет обязательных прав пользователя.',
         'Use your own account, keep credentials private, provide accurate contact details and do not upload unlawful material. Company-data access requires assigned permissions and accepted invitations. The organisation is responsible for lawful processing of its team data. Abuse prevention does not remove mandatory user rights.',
         'Korzystaj z własnego konta, chroń dane logowania, podawaj prawdziwe kontakty i nie przesyłaj treści niezgodnych z prawem. Dostęp do danych firmy wymaga uprawnień i przyjęcia zaproszenia. Organizacja odpowiada za zgodne z prawem przetwarzanie danych zespołu. Zapobieganie nadużyciom nie wyłącza obowiązkowych praw użytkownika.',
         'Використовуйте власний акаунт, бережіть дані входу, надавайте правдиві контакти й не завантажуйте незаконні матеріали. Доступ до даних компанії потребує прав і підтвердженого запрошення. Організація відповідає за законність обробки даних команди. Запобігання зловживанням не скасовує обов’язкових прав користувача.'))
    render('terms.html', ('Условия JobHub Support', 'JobHub Support terms', 'Warunki JobHub Support', 'Умови JobHub Support'), ('JobHub Support',)*4,
           general+scope+'<p><a href="/support-subscription-terms.html">'+tr('Условия платной подписки', 'Paid subscription terms', 'Warunki płatnej subskrypcji', 'Умови платної підписки')+'</a></p>')
    render('404.html', ('Страница недоступна', 'Page unavailable', 'Strona niedostępna', 'Сторінка недоступна'),
           ('Здесь доступен только JobHub Support. Перейдите на главную страницу.',
            'This site provides JobHub Support only. Please open the home page.',
            'Ta strona udostępnia wyłącznie JobHub Support. Przejdź na stronę główną.',
            'Тут доступний лише JobHub Support. Перейдіть на головну сторінку.'), '')
    pages = sorted(p.name for p in OUT.glob('*.html') if p.name != '404.html')
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://jobhub.today/{"" if p=="index.html" else p}</loc></url>' for p in pages)+'</urlset>', encoding='utf-8')
    (OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://jobhub.today/sitemap.xml\n', encoding='utf-8')
    (OUT / '_redirects').write_text('/demo https://jobhub-support-demo.onrender.com/?lang=ru 302\n/demo/ https://jobhub-support-demo.onrender.com/?lang=ru 302\n', encoding='utf-8')
    (OUT / '_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Content-Security-Policy: default-src \'self\'; img-src \'self\' data:; style-src \'self\'; script-src \'self\'; media-src \'self\' blob:; worker-src \'self\' blob:; connect-src \'self\'; frame-src \'none\'; object-src \'none\'; base-uri \'self\'; form-action \'none\'\n' + updates.media_headers(), encoding='utf-8')
    manifest = {'edition': EDITION, 'live_payments': False, 'publication_approved': True,
                'files': sorted(str(p.relative_to(OUT)).replace('\\', '/') for p in OUT.rglob('*') if p.is_file())}
    (OUT / 'support-site-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(f'{EDITION}: {len(pages)} pages; only allow-listed assets; no checkout. Output: {OUT}')


if __name__ == '__main__':
    main()
