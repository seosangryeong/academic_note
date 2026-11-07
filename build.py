#!/usr/bin/env python3
"""Build one site that holds every project's notes.

    python3 build.py                  # reads ../rbiz_challenge_note, ... (sibling folders)
    python3 build.py --src sources    # reads sources/rbiz_challenge_note, ... (used by GitHub Actions)
    python3 -m http.server -d _site 8080

The notes themselves live in each project's own repository (notes/*.md, assets/).
This site only copies them: the home page is home.md (overview), each project gets
its own folder (rbiz/, ...), the note list stays on the left and the
project list sits on the right.
"""
from html import escape
from pathlib import Path
import argparse
import hashlib
import re
import shutil

import markdown

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '_site'
SITE_TITLE = '학업 프로젝트 노트'
REPO_URL = 'https://github.com/seosangryeong/academic_note'
# 404.html is shown at any depth, so it links from the site root instead of relatively.
SITE_PATH = '/academic_note/'
FONT = ('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/'
        'pretendardvariable-dynamic-subset.min.css')
CSS_VERSION = hashlib.md5((ROOT / 'styles.css').read_bytes()).hexdigest()[:8]
EXTENSIONS = ['tables', 'attr_list', 'admonition', 'fenced_code', 'sane_lists', 'toc']

# Order in the right-hand list (most recent first).
# slug = folder on this site, repo = GitHub repository, period = shown on the home page and the
# project's overview page here (replaces the date written in the project's 00-index.md).
PROJECTS = [
    {'slug': 'rbiz', 'repo': 'rbiz_challenge_note', 'dir': 'rbiz_challenge_note', 'name': 'R-BIZ 챌린지 로버',
     'period': '2023.03 – 2023.10'},
]


# ---------- Markdown (same rules as each project's build.py) ----------

def render(text):
    return markdown.markdown(text, extensions=EXTENSIONS)


def read_note(path):
    text = path.read_text(encoding='utf-8')
    meta = {}
    if text.startswith('---'):
        head, text = text[3:].split('\n---', 1)
        for line in head.strip().splitlines():
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip()
    return meta, text


def fold_outs(text):
    """'??? title' + indented block -> <details> (inner Markdown rendered)."""
    lines = text.split('\n')
    out, i = [], 0
    while i < len(lines):
        match = re.match(r'^\?\?\?\s+(.*)$', lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        title, block = match.group(1), []
        i += 1
        while i < len(lines) and (lines[i].startswith('    ') or not lines[i].strip()):
            block.append(lines[i][4:])
            i += 1
        inner = render('\n'.join(block)).replace('\n\n', '\n')
        out += ['', f'<details class="explain"><summary>{escape(title)}</summary>'
                    f'<div class="body">{inner}</div></details>', '']
    return '\n'.join(out)


def html_name(stem):
    return 'index.html' if stem.endswith('index') else f'{stem}.html'


def polish(html):
    html = re.sub(r'href="([\w-]+)\.md(#[^"]*)?"',
                  lambda m: f'href="{html_name(m.group(1))}{m.group(2) or ""}"', html)
    html = html.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
    html = re.sub(r'(<div class="admonition issue">.*?</div>)',
                  lambda m: re.sub(r'(<p><strong>[^<]*</strong>)\s+', r'\1', m.group(1)), html, flags=re.S)
    card = r'<div class="admonition issue">.*?</div>'
    return re.sub(rf'(?:{card}\s*)+',
                  lambda m: f'<div class="issues">{m.group(0)}</div>\n', html, flags=re.S)


# ---------- page frame ----------

def project_list(current, up):
    """Right-hand list of projects. `up` is '' on the home page, '../' inside a project."""
    home = ' class="current" aria-current="page"' if current is None else ''
    items = f'<li><a href="{up}index.html"{home}>전체 개요</a></li>'
    for p in PROJECTS:
        cur = ' class="current"' if p['slug'] == current else ''
        items += f'<li><a href="{up}{p["slug"]}/index.html"{cur}>{escape(p["name"])}</a></li>'
    return items


def page(*, title, description, body, left, current, up, when=''):
    full = SITE_TITLE if title == SITE_TITLE else f'{title} | {SITE_TITLE}'
    when = f'<p class="meta">{escape(when)}</p>' if when else ''
    projects = project_list(current, up)
    left_nav = (f'<nav class="sidebar" aria-label="기록 목록"><div class="sticky">'
                f'<details class="side" open><summary>기록 목록</summary><ol>{left}</ol></details>'
                f'</div></nav>') if left else ''
    layout = 'layout' if left else 'layout no-left'
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(description)}">
<title>{escape(full)}</title>
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{FONT}">
<link rel="stylesheet" href="{up}styles.css?v={CSS_VERSION}">
</head>
<body>
<header class="site-header"><div class="inner">
<a class="brand" href="{up}index.html">{SITE_TITLE}</a>
<a class="header-link" href="{REPO_URL}">GitHub</a>
</div>
<nav class="project-strip" aria-label="프로젝트"><ol>{projects}</ol></nav>
</header>
<div class="{layout}">
{left_nav}
<main class="content">
<header class="note-head">{when}<h1>{escape(title)}</h1></header>
{body}
</main>
<nav class="projects" aria-label="프로젝트 목록"><div class="sticky">
<p class="projects-title">프로젝트</p><ol>{projects}</ol>
</div></nav>
</div>
<footer class="site-footer">seosangryeong · {SITE_TITLE}</footer>
</body>
</html>
'''


def left_nav(notes, name):
    nav = ''
    for other, m, _ in notes:
        label = escape(m.get('nav', m['title']))
        current = ' class="current" aria-current="page"' if other == name else ''
        nav += f'<li><a href="{other}"{current}>{label}</a></li>'
    return nav


# ---------- build ----------

def load(project, src):
    folder = src / project['dir']
    if not (folder / 'notes').is_dir():
        raise SystemExit(f'notes not found: {folder}/notes')
    notes = []
    for path in sorted((folder / 'notes').glob('*.md')):
        meta, text = read_note(path)
        notes.append((html_name(path.stem), meta, text))
    return folder, notes


def build_project(project, folder, notes):
    out = OUT / project['slug']
    (out / 'assets').mkdir(parents=True)
    for asset in (folder / 'assets').iterdir():
        if asset.is_file():
            shutil.copy(asset, out / 'assets' / asset.name)
    for name, meta, text in notes:
        body = polish(render(fold_outs(text)))
        title = meta['title']
        # A collection of unrelated projects: its period covers all of them, so don't show it on
        # the first project's page.
        on_index = name == 'index.html' and not project.get('collection')
        when = project['period'] if on_index else meta.get('date', '')
        (out / name).write_text(page(
            title=title, description=meta.get('description', title), body=body,
            left=left_nav(notes, name), current=project['slug'], up='../',
            when=when), encoding='utf-8')


def home():
    """Home page: research overview written in home.md. {{period:slug}} -> the project's period."""
    periods = {p['slug']: p['period'] for p in PROJECTS}
    text = re.sub(r'\{\{period:(\w+)\}\}', lambda m: periods[m.group(1)],
                  (ROOT / 'home.md').read_text(encoding='utf-8'))
    return page(title=SITE_TITLE, description='대학교·대학원 수업과 대회에서 한 프로젝트 기록.',
                body=polish(render(text)), left='', current=None, up='')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default=str(ROOT.parent),
                        help='folder that holds rbiz_challenge_note/, ... (default: parent folder)')
    src = Path(parser.parse_args().src).resolve()

    loaded = [(p, load(p, src)) for p in PROJECTS]
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'assets').mkdir(parents=True)
    shutil.copy(ROOT / 'styles.css', OUT / 'styles.css')
    for asset in (ROOT / 'assets').iterdir():
        shutil.copy(asset, OUT / 'assets' / asset.name)

    for project, (folder, notes) in loaded:
        build_project(project, folder, notes)
    (OUT / 'index.html').write_text(home(), encoding='utf-8')
    (OUT / '404.html').write_text(page(
        title='페이지를 찾을 수 없습니다', description='없는 페이지',
        body=f'<p>주소가 바뀌었거나 없는 페이지입니다. <a href="{SITE_PATH}index.html">처음 화면</a>에서 '
             '프로젝트를 고르세요.</p>',
        left='', current=None, up=SITE_PATH), encoding='utf-8')
    total = sum(len(n) for _, (_, n) in loaded)
    print(f'built {total} notes from {len(loaded)} projects -> {OUT.relative_to(ROOT)}/')


if __name__ == '__main__':
    main()
