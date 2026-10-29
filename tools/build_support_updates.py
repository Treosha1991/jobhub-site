"""Restore only the two existing Support articles and their original video.

Never copy the combined news page or its navigation into the public artifact.
The allow-listed articles and versioned films remain the original sources.
"""
import re
import shutil


ARTICLE_IDS = ('microsoft-store-2026-10-09', 'support-video-2026-10-08')
VIDEO_LANGUAGES = ('ru', 'en', 'pl', 'uk', 'nl')


def article(source, identifier):
    matches = re.findall(
        r'<article\b[^>]*\bid="' + re.escape(identifier) + r'"[^>]*>.*?</article>',
        source, re.S)
    assert len(matches) == 1, f'Expected one preserved Support article: {identifier}'
    return matches[0]


def add_player_assets(page):
    source = page.read_text(encoding='utf-8')
    assets = ('<link rel="stylesheet" href="/assets/support-video.css">'
              '<link rel="stylesheet" href="/assets/support-news.css">'
              '<script defer src="/assets/support-video.js"></script>')
    page.write_text(source.replace('</head>', assets + '</head>'), encoding='utf-8')


def build(root, out, commerce):
    source = (root / 'news.html').read_text(encoding='utf-8')
    articles = [article(source, identifier) for identifier in ARTICLE_IDS]
    video_article = articles[1]
    start = video_article.index('<section class="support-video"')
    end = video_article.index('</section>', video_article.index('</noscript>', start))
    player = video_article[start:end + len('</section>')]
    for name in ('support-video.css', 'support-video.js', 'support-news.css'):
        shutil.copy2(root / 'assets' / name, out / 'assets' / name)
    for relative in ('assets/support-video/20261008', 'assets/vendor/hls.js-1.7.3'):
        shutil.copytree(root / relative, out / relative)
    commerce.render('news.html',
                    ('Новости JobHub Support', 'JobHub Support news',
                     'Aktualności JobHub Support', 'Новини JobHub Support'),
                    ('Новости и видеопрезентация рабочего пространства JobHub Support.',
                     'News and video presentation of the JobHub Support workspace.',
                     'Aktualności i prezentacja wideo przestrzeni JobHub Support.',
                     'Новини та відеопрезентація робочого простору JobHub Support.'),
                    '<div class="support-updates">' + ''.join(articles) + '</div>')
    add_player_assets(out / 'news.html')
    return player


def media_headers():
    result = '\n/assets/support-video/20261008/*\n  Cache-Control: public, max-age=31536000, immutable\n'
    for lang in VIDEO_LANGUAGES:
        result += (f'\n/assets/support-video/20261008/{lang}/presentation.m3u8\n'
                   '  Content-Type: application/vnd.apple.mpegurl\n'
                   f'\n/assets/support-video/20261008/{lang}/subtitles.vtt\n'
                   '  Content-Type: text/vtt; charset=utf-8\n')
    return result
