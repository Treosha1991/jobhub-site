"""Static presentation shared with the native newcomer screen. No tracking."""
import json
from html import escape
from pathlib import Path


def build(source_root, out, commerce):
    data = json.loads((source_root / 'assets/support-presentation-v2/content.json').read_text(encoding='utf-8'))
    langs = commerce.LANGS
    slides = ''.join(
        f'<article class="presentation-slide" data-slide="{index}"{(" hidden" if index else "")}>'
        f'<p class="eyebrow">JobHub Support · {index + 1} / {len(data["slides"])}</p>'
        '<h2>' + commerce.tr(*(slide[lang]['title'] for lang in langs)) + '</h2>'
        '<p>' + commerce.tr(*(slide[lang]['body'] for lang in langs)) + '</p></article>'
        for index, slide in enumerate(data['slides']))
    content = '<section class="section-card" id="support-presentation" aria-label="JobHub Support">' + slides
    content += '<div class="actions"><button type="button" class="btn" data-slide-back>' + commerce.tr('Назад', 'Back', 'Wstecz', 'Назад') + '</button>'
    content += '<output aria-live="polite" data-slide-count>1 / 6</output><button type="button" class="btn" data-slide-next>' + commerce.tr('Далее', 'Next', 'Dalej', 'Далі') + '</button></div>'
    content += '<p><a class="btn" href="/demo">' + commerce.tr('Попробовать демо', 'Try the demo', 'Wypróbuj demo', 'Спробувати демо') + '</a></p></section>'
    commerce.render('support-presentation.html', ('Презентация', 'Presentation', 'Prezentacja', 'Презентація'), ('JobHub Support',)*4, content)
    page = out / 'support-presentation.html'
    html = page.read_text(encoding='utf-8').replace('</head>', '<link rel="stylesheet" href="/assets/support-presentation.css"><script src="/assets/support-presentation.js" defer></script></head>')
    page.write_text(html, encoding='utf-8')
    (out / 'assets/support-presentation.css').write_text('''
.presentation-slide { min-height: 15rem; padding: clamp(1rem, 4vw, 3rem); }
.presentation-slide h2 { font-size: clamp(1.6rem, 4vw, 3rem); line-height: 1.2; }
.presentation-slide p { max-width: 50rem; font-size: clamp(1rem, 2vw, 1.3rem); line-height: 1.65; }
#support-presentation .actions { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }
#support-presentation button { cursor: pointer; font: inherit; }
#support-presentation button:disabled { opacity: .45; cursor: default; }
[data-slide][hidden] { display: none; }
''', encoding='utf-8')
    (out / 'assets/support-presentation.js').write_text('''
const slides = [...document.querySelectorAll('[data-slide]')];
const back = document.querySelector('[data-slide-back]');
const next = document.querySelector('[data-slide-next]');
let index = 0;
function show(value) {
  index = Math.max(0, Math.min(slides.length - 1, value));
  slides.forEach((slide, i) => { slide.hidden = i !== index; });
  back.disabled = index === 0;
  next.disabled = index === slides.length - 1;
  document.querySelector('[data-slide-count]').textContent = `${index + 1} / ${slides.length}`;
}
back.addEventListener('click', () => show(index - 1));
next.addEventListener('click', () => show(index + 1));
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft') show(index - 1);
  if (e.key === 'ArrowRight') show(index + 1);
});
show(0);
''', encoding='utf-8')
