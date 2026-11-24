#!/usr/bin/env python3
"""Render tools/content.py into drafts/*.plain.html and Word .docx files.

Usage: python3 tools/build-content.py [docx_out_dir]
Requires: python-docx. PNG avatars for Word are read from <docx_out_dir>/_avatars/<slug>.png.
"""
import html
import os
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

sys.path.insert(0, os.path.dirname(__file__))
from content import PAGES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFTS = os.path.join(ROOT, 'drafts')
DOCX_OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), 'slf-eds-demo1-content')


def to_class(name):
    m = re.match(r'^([^(]+)(?:\(([^)]*)\))?', name)
    base = re.sub(r'[^a-z0-9]+', '-', m.group(1).strip().lower()).strip('-')
    variants = [re.sub(r'[^a-z0-9]+', '-', v.strip().lower()).strip('-') for v in (m.group(2) or '').split(',') if v.strip()]
    return ' '.join([base] + variants)


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


# ---------------------------------------------------------------- HTML
def runs_html(runs):
    out = []
    for r in runs:
        if isinstance(r, str):
            out.append(html.escape(r))
            continue
        kind, text, href = r
        a = f'<a href="{html.escape(href)}">{html.escape(text)}</a>'
        if kind == 'b-a':
            a = f'<strong>{a}</strong>'
        elif kind == 'i-a':
            a = f'<em>{a}</em>'
        out.append(a)
    return ''.join(out)


def item_html(item):
    kind = item[0]
    if kind == 'p':
        return f'<p>{runs_html(item[1])}</p>'
    if kind in ('h1', 'h2', 'h3'):
        return f'<{kind} id="{slugify(item[1])}">{html.escape(item[1])}</{kind}>'
    if kind == 'ul':
        return '<ul>' + ''.join(f'<li>{runs_html(li)}</li>' for li in item[1]) + '</ul>'
    if kind == 'img':
        _, slug, alt = item
        return (f'<picture><img src="/images/avatars/{slug}.svg" alt="{html.escape(alt)}" '
                f'width="480" height="480" loading="lazy"></picture>')
    if kind == 'block':
        _, name, rows = item
        body = ''.join('<div>' + ''.join('<div>' + ''.join(item_html(i) for i in cell) + '</div>' for cell in row) + '</div>' for row in rows)
        return f'<div class="{to_class(name)}">{body}</div>'
    raise ValueError(kind)


def page_html(page):
    sections = [list(s) for s in page['sections']]
    if page.get('metadata'):
        # the AEM pipeline (and `aem up`) moves the metadata block into <head>
        sections[-1].append(('block', 'Metadata', [[[('p', [k])], [('p', [v])]] for k, v in page['metadata'].items()]))
    out = []
    for section in sections:
        classes = []
        items = []
        for i in section:
            if i[0] == 'block' and i[1] == 'Section Metadata':
                # the AEM pipeline turns Section Metadata "Style" into classes on the section div
                for row in i[2]:
                    key = row[0][0][1][0].strip().lower()
                    if key == 'style':
                        classes += [slugify(v) for v in row[1][0][1][0].split(',')]
                continue
            items.append(i)
        attr = f' class="{" ".join(classes)}"' if classes else ''
        out.append(f'<div{attr}>' + ''.join(item_html(i) for i in items) + '</div>')
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- DOCX
def add_hyperlink(paragraph, text, url, bold=False, italic=False):
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    hl = OxmlElement('w:hyperlink')
    hl.set(qn('r:id'), r_id)
    run = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0563C1')
    rpr.append(color)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rpr.append(u)
    if bold:
        rpr.append(OxmlElement('w:b'))
    if italic:
        rpr.append(OxmlElement('w:i'))
    run.append(rpr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    run.append(t)
    hl.append(run)
    paragraph._p.append(hl)


def abs_url(href):
    if href.startswith('/'):
        return 'https://main--slf-eds-demo1--michaelpereira78.aem.page' + href
    return href


def add_runs(par, runs):
    for r in runs:
        if isinstance(r, str):
            par.add_run(r)
        else:
            kind, text, href = r
            add_hyperlink(par, text, abs_url(href), bold=kind == 'b-a', italic=kind == 'i-a')


def first_par(container, state):
    """Reuse the empty first paragraph of a new table cell."""
    if state.get('fresh'):
        state['fresh'] = False
        return container.paragraphs[0]
    return container.add_paragraph()


def add_item(container, item, state):
    kind = item[0]
    if kind == 'p':
        add_runs(first_par(container, state), item[1])
    elif kind in ('h1', 'h2', 'h3'):
        p = first_par(container, state)
        p.style = f'Heading {kind[1]}'
        p.add_run(item[1])
    elif kind == 'ul':
        for li in item[1]:
            p = first_par(container, state)
            p.style = 'List Bullet'
            add_runs(p, li)
    elif kind == 'img':
        _, slug, alt = item
        p = first_par(container, state)
        png = os.path.join(DOCX_OUT, '_avatars', f'{slug}.png')
        run = p.add_run()
        shape = run.add_picture(png, width=Inches(state.get('img_width', 1.1)))
        shape._inline.docPr.set('descr', alt)
        shape._inline.docPr.set('title', alt)
    elif kind == 'block':
        _, name, rows = item
        ncols = max(len(r) for r in rows)
        table = container.add_table(rows=len(rows) + 1, cols=ncols)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells[0]
        if ncols > 1:
            hdr = hdr.merge(table.rows[0].cells[ncols - 1])
        hp = hdr.paragraphs[0]
        hr = hp.add_run(name)
        hr.bold = True
        shade = OxmlElement('w:shd')
        shade.set(qn('w:val'), 'clear')
        shade.set(qn('w:fill'), 'F9A66C')
        hdr._tc.get_or_add_tcPr().append(shade)
        for ri, row in enumerate(rows):
            for ci, cell in enumerate(row):
                c = table.rows[ri + 1].cells[ci]
                cstate = {'fresh': True, 'img_width': 0.7 if 'Team' in name else 1.4}
                for i in cell:
                    add_item(c, i, cstate)
        if name == 'Team Cards':
            table.autofit = False
            widths = [0.85, 1.15, 1.1, 2.3, 1.45, 0.95]
            for row in table.rows[1:]:
                for ci, w in enumerate(widths[:len(row.cells)]):
                    row.cells[ci].width = Inches(w)
        container.add_paragraph()
    else:
        raise ValueError(kind)


def page_docx(page, path):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Inches(0.6)
    for si, section in enumerate(page['sections']):
        if si > 0:
            doc.add_paragraph('---')
        state = {}
        for item in section:
            add_item(doc, item, state)
    if page.get('metadata'):
        add_item(doc, ('block', 'Metadata', [[[('p', [k])], [('p', [v])]] for k, v in page['metadata'].items()]), {})
    doc.save(path)


def main():
    for name, page in PAGES.items():
        hp = os.path.join(DRAFTS, f'{name}.plain.html')
        os.makedirs(os.path.dirname(hp), exist_ok=True)
        with open(hp, 'w', encoding='utf-8') as f:
            f.write(page_html(page))
        dp = os.path.join(DOCX_OUT, f'{name}.docx')
        os.makedirs(os.path.dirname(dp), exist_ok=True)
        page_docx(page, dp)
        print('wrote', os.path.relpath(hp, ROOT), '|', dp)


if __name__ == '__main__':
    main()
