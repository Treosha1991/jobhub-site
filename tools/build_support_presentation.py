"""Build the public video page and its three-step employer invitation."""
from html import escape


def build(out, commerce, onboarding_origin, video):
    tr = commerce.tr
    steps = (
        (('Заполните анкету', 'Fill in your application', 'Wypełnij formularz', 'Заповніть анкету'),
         ('Расскажите о компании. Мы проверим данные и сообщим, когда можно продолжить.',
          'Tell us about your company. We’ll review your details and let you know when you can continue.',
          'Opowiedz o firmie. Sprawdzimy dane i damy znać, kiedy możesz przejść dalej.',
          'Розкажіть про компанію. Ми перевіримо дані й повідомимо, коли можна продовжити.')),
        (('Выберите тариф', 'Choose a plan', 'Wybierz pakiet', 'Оберіть тариф'),
         ('После одобрения выберите Free или пакет, который оплачивает компания.',
          'Once approved, choose Free or a plan your company pays for.',
          'Po zatwierdzeniu wybierz Free albo pakiet opłacany przez firmę.',
          'Після схвалення оберіть Free або пакет, який оплачує компанія.')),
        (('Управляйте компанией', 'Run your company', 'Zarządzaj firmą', 'Керуйте компанією'),
         ('Приглашайте команду и планируйте работу в браузере, приложении для компьютера или на телефоне.',
          'Invite your team and plan work in your browser, desktop app or on your phone.',
          'Zaproś zespół i planuj pracę w przeglądarce, aplikacji komputerowej lub na telefonie.',
          'Запрошуйте команду й плануйте роботу в браузері, застосунку для комп’ютера або на телефоні.')),
    )
    cards = ''.join(
        f'<li><span class="support-step-number" aria-hidden="true">{number:02}</span>'
        f'<h3>{tr(*title)}</h3>{commerce.paragraph(body)}</li>'
        for number, (title, body) in enumerate(steps, 1)
    )
    application = escape(onboarding_origin + '/employer/connect-company/?lang=en', quote=True)
    title = tr('Начните с трёх шагов', 'Get started in three steps', 'Zacznij w trzech krokach', 'Почніть із трьох кроків')
    content = f"""
<section class="section-card support-steps" id="support-presentation" aria-labelledby="support-steps-title">
  <h2 id="support-steps-title">{title}</h2>
  <ol>{cards}</ol>
  <div class="support-step-actions">
    <a class="btn support-step-primary" data-onboarding-link href="{application}">{tr('Заполнить анкету', 'Fill in the application', 'Wypełnij formularz', 'Заповнити анкету')}</a>
    <a class="btn" href="/support-pricing.html">{tr('Посмотреть тарифы', 'See plans', 'Zobacz pakiety', 'Переглянути тарифи')}</a>
  </div>
</section>
"""
    commerce.render('support-presentation.html',
        ('Презентация', 'Presentation', 'Prezentacja', 'Презентація'), None, video + content)
    page = out / 'support-presentation.html'
    html = page.read_text(encoding='utf-8').replace('</head>',
        '<link rel="stylesheet" href="/assets/support-steps.css"></head>')
    page.write_text(html, encoding='utf-8')
    from build_support_updates import add_player_assets
    add_player_assets(page)
    (out / 'assets/support-steps.css').write_text("""
.support-steps { padding: clamp(20px, 4vw, 34px); }
.support-steps h2 { font-size: clamp(24px, 3vw, 36px); margin: 0 0 18px; }
.support-steps ol {
  list-style: none; margin: 0; padding: 0; display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px;
}
.support-steps li {
  padding: 17px; border: 1px solid #426480; border-radius: 14px;
  background: linear-gradient(145deg, #16434f, #132d49);
}
.support-step-number {
  display: inline-grid; place-items: center; min-width: 42px; height: 38px;
  border-radius: 9px; background: #185548; color: #a3ffd0; font-weight: 800;
}
.support-steps h3 { margin: 12px 0 6px; font-size: 1.18rem; }
.support-steps p { margin: 0; color: #c5d9e8; }
.support-step-actions { margin-top: 18px; display: flex; flex-wrap: wrap; gap: 10px; }
.support-step-actions .support-step-primary { background: #26dc8a; border-color: #26dc8a; color: #082e23; }
@media (max-width: 720px) { .support-steps ol { grid-template-columns: 1fr; } }
""", encoding='utf-8')
