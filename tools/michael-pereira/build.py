#!/usr/bin/env python3
"""Build the /michael-pereira/ demo replica content.

Outputs:
  drafts/michael-pereira/*.plain.html          local preview (npm start)
  <out>/michael-pereira/*.docx                 Google Docs / Word files to upload to Drive
  <out>/da/michael-pereira/*.html              Document Authoring (da.live) HTML for slf-eds-demo1-da

Usage: python3 tools/michael-pereira/build.py [out_dir]   (default ../slf-eds-demo1-michael-pereira-content)
"""
import html
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))

spec = importlib.util.spec_from_file_location('build_content', os.path.join(ROOT, 'tools', 'build-content.py'))
bc = importlib.util.module_from_spec(spec)
sys.argv, _argv = sys.argv[:1], sys.argv
spec.loader.exec_module(bc)
sys.argv = _argv

from content_mp import BASE, PAGES  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), 'slf-eds-demo1-michael-pereira-content')
DA_ORIGIN = 'https://main--slf-eds-demo1-da--michaelpereira78.aem.page'


def da_page_html(page):
    """Like page_html, but keeps Section Metadata as a block (the format DA authors see)."""
    sections = [list(s) for s in page['sections']]
    if page.get('metadata'):
        sections[-1].append(('block', 'Metadata', [[[('p', [k])], [('p', [v])]] for k, v in page['metadata'].items()]))
    parts = []
    for section in sections:
        parts.append('<div>' + ''.join(bc.item_html(i) for i in section) + '</div>')
    body = '\n'.join(f'    {p}' for p in parts).replace('src="/images/', f'src="{DA_ORIGIN}/images/')
    return '<body>\n  <header></header>\n  <main>\n' + body + '\n  </main>\n  <footer></footer>\n</body>\n'


def main():
    slug = BASE.strip('/')
    for name, page in PAGES.items():
        hp = os.path.join(bc.DRAFTS, slug, f'{name}.plain.html')
        os.makedirs(os.path.dirname(hp), exist_ok=True)
        with open(hp, 'w', encoding='utf-8') as f:
            f.write(bc.page_html(page))
        dp = os.path.join(OUT, slug, f'{name}.docx')
        os.makedirs(os.path.dirname(dp), exist_ok=True)
        bc.page_docx(page, dp)
        ap = os.path.join(OUT, 'da', slug, f'{name}.html')
        os.makedirs(os.path.dirname(ap), exist_ok=True)
        with open(ap, 'w', encoding='utf-8') as f:
            f.write(da_page_html(page))
        print('wrote', os.path.relpath(hp, ROOT), '|', os.path.relpath(dp, OUT), '|', os.path.relpath(ap, OUT))


if __name__ == '__main__':
    main()
