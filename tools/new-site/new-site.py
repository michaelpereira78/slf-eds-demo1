#!/usr/bin/env python3
"""Generate a new advisor site from an approved template and brand theme.

Writes, for one new site:
  <out>/<site>/index.docx, nav.docx, footer.docx   starter documents to upload (Drive converts them to Google Docs)
  <out>/<site>/sidekick.json                       Sidekick config (Library, compliance review, snapshot review)
  <out>/<site>/create-site.sh                      the admin API calls that create the site (needs an admin token)
  <out>/<site>/README.txt                          step-by-step instructions

Two modes:
  --mode repoless   (default) a separate site, e.g. https://main--prairie-sky--<org>.aem.page/, that reuses
                    this repository's code (AEM "repoless" sites). Needs one admin API call.
  --mode folder     a sub-folder of the existing demo site, e.g. /prairie-sky/ (no admin call needed;
                    this is how /harbourview/ and /northstar/ are set up in the demo).

Example:
  python3 tools/new-site/new-site.py --firm "Prairie Sky Financial" --city "Regina, SK" \
      --lead "Sam Rivera, CFP" --theme harbour --template advisor-team

All generated people and contact details are placeholders (example.com, 555 numbers).
Requires: python-docx.
"""
import argparse
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ORG = 'michaelpereira78'
REPO = 'slf-eds-demo1'
THEMES = {'forest': 'Forest', 'harbour': 'Harbour', 'slate': 'Slate'}
TEMPLATES = ('advisor-team', 'solo-advisor', 'campaign')

# reuse the document writer from tools/build-content.py
spec = importlib.util.spec_from_file_location('build_content', os.path.join(ROOT, 'tools', 'build-content.py'))


def load_builder():
    saved = sys.argv
    sys.argv = saved[:1]
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.argv = saved
    return mod


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:40]


def meta_block(rows):
    return ('block', 'Metadata', [[[('p', [k])], [('p', [v])]] for k, v in rows.items()])


def section_style(style):
    return ('block', 'Section Metadata', [[[('p', ['Style'])], [('p', [style])]]])


def pages(a, base):
    """Starter pages. `base` is '' for a repoless site or '/<slug>' for folder mode."""
    first = a.lead.split(',')[0].split(' ')[0]
    email = f"{slugify(a.lead.split(',')[0]).replace('-', '.')}@example.com"
    disclosure = ('p', [('a', f'https://main--{REPO}--{ORG}.aem.page/fragments/disclosure', '/fragments/disclosure')])
    meta = {
        'Title': f'{a.firm} | {a.city}',
        'Description': f'{a.firm} in {a.city}. [Replace with one sentence about the practice.]',
        'Template': a.template,
        'Theme': THEMES[a.theme],
        'Compliance Status': 'Draft',
    }
    if base:
        meta['Nav'] = f'{base}/nav'
        meta['Footer'] = f'{base}/footer'
    home = f'{base}/'
    if a.template == 'solo-advisor':
        sections = [
            [('block', 'Hero', [[[('p', [a.city]), ('h1', a.lead),
                                  ('p', ['[Who you help, in one sentence.]']),
                                  ('p', [('b-a', 'Book a meeting', f'mailto:{email}')])]]])],
            [('h2', 'How I work'), ('p', ['[Your story and approach. Paste your photo into the hero above.]']),
             ('ul', [['[Service one]'], ['[Service two]'], ['[Service three]']]),
             ('block', 'Contact (Card)', [[[('p', ['Phone'])], [('p', ['555-555-0100'])]],
                                          [[('p', ['Email'])], [('p', [email])]]]),
             section_style('Sidebar')],
        ]
    elif a.template == 'campaign':
        sections = [
            [('block', 'Hero (Centered)', [[[('p', [a.firm]), ('h1', '[The offer in one line]'),
                                             ('p', ['[Why it matters, in two sentences.]']),
                                             ('p', [('b-a', 'Book now', f'mailto:{email}')])]]])],
            [('h2', 'What you get'), ('block', 'Columns', [[
                [('h3', '[Benefit one]'), ('p', ['[One sentence.]'])],
                [('h3', '[Benefit two]'), ('p', ['[One sentence.]'])],
                [('h3', '[Benefit three]'), ('p', ['[One sentence.]'])]]]), section_style('Centered')],
        ]
    else:
        sections = [
            [('block', 'Hero', [[[('p', [a.city]), ('h1', f'Meet {a.firm}'),
                                  ('p', ['[Two or three sentences about who you help and how.]']),
                                  ('p', [('b-a', 'Book a meeting', f'{home}#contact-us')])]]])],
            [('h2', 'Our team'), ('p', ['[One sentence about the team. Add a row per person; paste photos in the first column.]']),
             ('block', 'Team Cards', [[[('p', ['[photo]'])], [('p', [a.lead])], [('p', ['[Title]'])],
                                       [('p', [f'[Short bio for {first}.]'])], [('p', [email])], [('p', ['555-555-0100'])]]]),
             section_style('Light')],
            [('h2', 'Contact us'), ('block', 'Contact', [
                [[('p', ['Office'])], [('p', ['[Street address]']), ('p', [a.city])]],
                [[('p', ['Main line'])], [('p', ['555-555-0100'])]],
                [[('p', ['Email'])], [('p', [email])]]])],
        ]
    sections.append([disclosure])
    nav = {'metadata': {}, 'sections': [
        [('p', [('a', a.firm, home)])],
        [('ul', [[('a', 'Home', home)], [('a', 'Contact', f'{home}#contact-us')]])],
        [('p', [('b-a', 'Book a meeting', f'mailto:{email}')])],
    ]}
    footer = {'metadata': {}, 'sections': [
        [('p', [('a', a.firm, home)]), ('p', [f'{a.firm}, {a.city}'])],
        [('ul', [[('a', 'Home', home)]])],
        [('p', ['Demo, not affiliated with Sun Life']), ('p', ['All names and contact details are placeholders.'])],
    ]}
    return {'index': {'metadata': meta, 'sections': sections}, 'nav': nav, 'footer': footer}


SCRIPT = """#!/usr/bin/env bash
# Creates the site "{site}" that reuses the code in github.com/{org}/{repo} (AEM "repoless" site).
# Needs an AEM admin token: sign in at https://tools.aem.live, then copy the x-auth-token value
# (or use the Site Admin tool's "Add site" screen instead of this script).
set -euo pipefail
ORG="{org}"
SITE="{site}"
TOKEN="${{AEM_ADMIN_TOKEN:?export AEM_ADMIN_TOKEN=<your admin token> first}}"
DRIVE_FOLDER="${{DRIVE_FOLDER:?export DRIVE_FOLDER=https://drive.google.com/drive/folders/<id> first}}"

# 1. Create the site: code from the existing repo, content from the new Drive folder
curl -fsS -X PUT "https://admin.hlx.page/config/$ORG/sites/$SITE.json" \\
  -H "x-auth-token: $TOKEN" -H 'content-type: application/json' \\
  --data '{{"code":{{"owner":"{org}","repo":"{repo}"}},"content":{{"source":{{"type":"google","url":"'"$DRIVE_FOLDER"'"}}}}}}'

# 2. Sidekick: Library, Request compliance review, Review (snapshots)
curl -fsS -X POST "https://admin.hlx.page/config/$ORG/sites/$SITE/sidekick.json" \\
  -H "x-auth-token: $TOKEN" -H 'content-type: application/json' --data @"$(dirname "$0")/sidekick.json"

# 3. (Production) only Compliance can publish. Uncomment and replace the example addresses.
#    Note: adding roles turns on sign-in for everyone using Sidekick on this site.
# curl -fsS -X POST "https://admin.hlx.page/config/$ORG/sites/$SITE/access/admin.json" \\
#   -H "x-auth-token: $TOKEN" -H 'content-type: application/json' \\
#   --data '{{"role":{{"basic_author":["*@example.com"],"publish":["compliance-team@example.com"]}}}}'

echo "Created. Preview: https://main--$SITE--$ORG.aem.page/ (404 until the first document is previewed)"
"""

README = """New site: {firm} ({city})
Theme: {theme}   Template: {template}   Mode: {mode}

1. In Google Drive, create a folder for the site{folder_note}.
   Share it with helix@adobe.com as Editor.
2. Turn on Drive > Settings > "Convert uploads to Google Docs editor format", then upload
   index.docx, nav.docx and footer.docx into the folder.
{admin_step}
4. Open each document, edit the text in [square brackets], then Sidekick > Preview.
5. Click "Request compliance review" (Sidekick or the status bar on the preview page).
   Compliance approves and publishes.

Preview address: {preview}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--firm', required=True)
    ap.add_argument('--city', required=True)
    ap.add_argument('--lead', required=True, help='lead advisor name, e.g. "Sam Rivera, CFP"')
    ap.add_argument('--theme', choices=sorted(THEMES), default='forest')
    ap.add_argument('--template', choices=TEMPLATES, default='advisor-team')
    ap.add_argument('--mode', choices=('repoless', 'folder'), default='repoless')
    ap.add_argument('--site', help='site name (default: from the firm name)')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(ROOT), 'slf-eds-demo1-content', '_new-sites'))
    a = ap.parse_args()

    site = a.site or slugify(a.firm)
    out = os.path.join(a.out, site)
    os.makedirs(out, exist_ok=True)
    builder = load_builder()
    builder.DOCX_OUT = out
    base = f'/{site}' if a.mode == 'folder' else ''
    for name, page in pages(a, base).items():
        builder.page_docx(page, os.path.join(out, f'{name}.docx'))

    with open(os.path.join(ROOT, 'docs', 'sidekick.json'), encoding='utf-8') as f:
        sidekick = json.load(f)
    sidekick['project'] = a.firm
    with open(os.path.join(out, 'sidekick.json'), 'w', encoding='utf-8') as f:
        json.dump(sidekick, f, indent=2)

    if a.mode == 'repoless':
        with open(os.path.join(out, 'create-site.sh'), 'w', encoding='utf-8') as f:
            f.write(SCRIPT.format(org=ORG, repo=REPO, site=site))
        os.chmod(os.path.join(out, 'create-site.sh'), 0o755)
        admin = ('3. A platform admin runs create-site.sh (needs an AEM admin token), or adds the site in\n'
                 '   https://tools.aem.live Site Admin with the folder URL as the content source.')
        preview = f'https://main--{site}--{ORG}.aem.page/'
        folder_note = ''
    else:
        admin = '3. No admin step: the folder lives inside the existing demo site.'
        preview = f'https://main--{REPO}--{ORG}.aem.page/{site}/'
        folder_note = f' named "{site}" INSIDE the existing demo content folder'
    with open(os.path.join(out, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(README.format(firm=a.firm, city=a.city, theme=THEMES[a.theme], template=a.template,
                              mode=a.mode, admin_step=admin, preview=preview, folder_note=folder_note))
    print(f'Generated {site} in {out}')
    for fn in sorted(os.listdir(out)):
        print('  ', fn)


if __name__ == '__main__':
    main()
