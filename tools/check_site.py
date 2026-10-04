"""Check static pages and their local navigation before deployment."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.guide_shots = set()
        self.errors = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "img" and values.get("data-guide-shot"):
            self.guide_shots.add(values["data-guide-shot"])
        anchor = values.get("id")
        if anchor:
            if anchor in self.ids:
                self.errors.append(f"duplicate id: {anchor}")
            self.ids.add(anchor)
        for attr in ("href", "src", "content"):
            value = values.get(attr, "")
            if attr == "content" and tag != "meta":
                continue
            if attr == "content" and not values.get("property", "").startswith("og:image"):
                continue
            if value:
                self.links.append(value)


def main():
    pages = {}
    for path in ROOT.glob("*.html"):
        page = Page()
        source = path.read_text(encoding="utf-8")
        if source.count("<script") != source.count("</script>"):
            page.errors.append("unclosed script tag")
        page.feed(source)
        counts = {lang: source.count(f'lang-{lang}"') for lang in ("ru", "en", "pl", "uk")}
        if len(set(counts.values())) != 1:
            page.errors.append(f"incomplete translations: {counts}")
        pages[path.name] = page

    errors = []
    for name, page in pages.items():
        errors.extend(f"{name}: {error}" for error in page.errors)
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith("//"):
                continue
            target_name = unquote(parsed.path)
            if not target_name and not parsed.fragment:
                continue
            target = ROOT / target_name.lstrip("/")
            if target_name in ("", "/"):
                target = ROOT / (name if not target_name else "index.html")
            elif target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"{name}: missing local target {link}")
            elif parsed.fragment and target.suffix == ".html":
                destination = pages.get(target.name)
                if destination and parsed.fragment not in destination.ids:
                    errors.append(f"{name}: missing anchor {link}")
        for shot in page.guide_shots:
            for lang in ("ru", "en", "pl", "uk"):
                image = ROOT / "assets" / "support-guide" / lang / f"{shot}.jpg"
                if not image.is_file():
                    errors.append(f"{name}: missing {lang} guide image {shot}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(pages)} pages: local links, assets and anchors OK")


if __name__ == "__main__":
    main()
