"""Check the built site (_site/) for broken local links and anchors. Stdlib only.

    python3 build.py && python3 check_site.py
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent / "_site"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.references, self.errors = set(), [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f"duplicate id: {attrs['id']}")
            self.ids.add(attrs['id'])
        for attr in ('src', 'href'):
            if attrs.get(attr):
                self.references.append(attrs[attr])


def main():
    if not SITE.is_dir():
        raise SystemExit('_site/ not found: run python3 build.py first')
    pages, errors = {}, []
    for path in SITE.rglob('*.html'):
        if path.name == '404.html':  # links from the site root on purpose
            continue
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        pages[path.resolve()] = page
        errors += [f'{path.relative_to(SITE)}: {e}' for e in page.errors]
    for path, page in pages.items():
        for ref in page.references:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith('/'):
                errors.append(f'{path.relative_to(SITE)}: root-relative URL breaks project Pages: {ref}')
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_file():
                errors.append(f'{path.relative_to(SITE)}: missing file: {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(SITE)}: missing anchor: {ref}')
    if not (SITE / 'index.html').is_file():
        errors.append('index.html missing')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Site OK: {len(pages)} pages, {sum(len(p.references) for p in pages.values())} references.')


if __name__ == '__main__':
    main()
