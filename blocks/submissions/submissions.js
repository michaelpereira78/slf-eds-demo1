/**
 * Submissions block: the latest requests or audit events made from THIS browser, so a presenter
 * can show what was just sent. The system of record is the Google Sheet in Drive.
 *
 * Authoring (two-column rows):
 *   Form   figma-import | layout-change | compliance-audit
 *   Sheet  optional link to the Google Sheet (shown as "Open the sheet")
 */
import { localSubmissions, clearLocalSubmissions } from '../../scripts/forms.js';

const COLUMNS = {
  'figma-import': [['reference', 'Reference'], ['submittedAt', 'Submitted'], ['siteName', 'Site'], ['requester', 'Requested by'], ['deadline', 'Needed by'], ['status', 'Status']],
  'layout-change': [['reference', 'Reference'], ['submittedAt', 'Submitted'], ['site', 'Site'], ['pagePath', 'Page'], ['change', 'Change'], ['requester', 'Requested by']],
  'compliance-audit': [['timestamp', 'Time'], ['event', 'Event'], ['pagePath', 'Page'], ['advisor', 'Advisor'], ['reviewer', 'Reviewer'], ['status', 'Status']],
};

const SAMPLE = {
  'figma-import': [{
    reference: 'FIG-1118-7QX2', submittedAt: '2026-11-18 10:42', siteName: 'Bayside Wealth (rebrand)', requester: 'R. Castillo', deadline: '2026-12-15', status: 'In build',
  }],
  'layout-change': [{
    reference: 'LAY-1123-K2PD', submittedAt: '2026-11-23 15:10', site: 'Harbourview Financial Group', pagePath: '/harbourview/', change: 'Add a block (testimonials, stats, banner...)', requester: 'Grace MacLeod',
  }],
  'compliance-audit': [
    {
      timestamp: '2026-11-24 09:12', event: 'Submitted', pagePath: '/campaigns/retirement-checkup', advisor: 'Priya Nair', reviewer: '', status: 'Pending review',
    },
    {
      timestamp: '2026-11-22 16:40', event: 'Changes requested', pagePath: '/northstar/', advisor: 'Elena Park', reviewer: 'R. Castillo', status: 'Changes requested',
    },
    {
      timestamp: '2026-11-20 11:05', event: 'Approved', pagePath: '/', advisor: 'Jordan Lee', reviewer: 'R. Castillo', status: 'Approved',
    },
  ],
};

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'class') e.className = v;
    else if (k === 'text') e.textContent = v;
    else e.setAttribute(k, v);
  });
  children.flat().forEach((c) => c && e.append(c));
  return e;
}

export default function decorate(block) {
  const config = {};
  [...block.children].forEach((row) => {
    const [k, v] = row.children;
    if (!k) return;
    const link = v && v.querySelector('a[href]');
    let value = v ? v.textContent.trim() : '';
    if (link) value = link.getAttribute('href');
    config[k.textContent.trim().toLowerCase()] = value;
  });
  const formId = config.form || 'figma-import';
  const cols = COLUMNS[formId] || COLUMNS['figma-import'];
  block.textContent = '';

  const wrap = el('div', {
    class: 'sub-table-wrap', tabindex: '0', role: 'region', 'aria-label': 'Recent submissions',
  });
  const note = el('p', { class: 'sub-note' });
  const tools = el('div', { class: 'sub-tools' });

  const render = () => {
    const mine = localSubmissions(formId).map((s) => ({ ...s.data, mode: s.mode }));
    const rows = [...mine, ...SAMPLE[formId].map((r) => ({ ...r, mode: 'sample' }))];
    const table = el(
      'table',
      {},
      el('thead', {}, el(
        'tr',
        {},
        ...cols.map(([, label]) => el('th', { scope: 'col', text: label })),
        el('th', { scope: 'col', text: 'Recorded in' }),
      )),
      el('tbody', {}, ...rows.slice(0, 12).map((r) => el(
        'tr',
        { class: `sub-${r.mode}` },
        ...cols.map(([key]) => el('td', { text: r[key] || '' })),
        el('td', {}, el('span', {
          class: `sub-pill sub-pill-${r.mode}`,
          text: {
            sheet: 'Google Sheet', webhook: 'Google Sheet', demo: 'This browser', sample: 'Sample row',
          }[r.mode],
        })),
      ))),
    );
    wrap.replaceChildren(table);
    note.textContent = mine.length
      ? `${mine.length} submitted from this browser, newest first. The sheet in Drive is the system of record.`
      : 'Nothing submitted from this browser yet; the row below is sample data. The sheet in Drive is the system of record.';
  };

  if (config.sheet) tools.append(el('a', { class: 'button secondary', href: config.sheet, text: 'Open the sheet in Google Drive' }));
  const clear = el('button', { type: 'button', class: 'button secondary', text: 'Clear this browser' });
  clear.addEventListener('click', () => { clearLocalSubmissions(formId); render(); });
  tools.append(clear);

  document.addEventListener('request-form:submitted', render);
  document.addEventListener('audit:logged', render);
  render();
  block.append(note, wrap, tools);
}
