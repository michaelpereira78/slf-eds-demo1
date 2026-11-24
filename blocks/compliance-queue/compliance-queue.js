import {
  STATUS, statusKey, getQueue, saveDecision, resetDemo, siteInfo, normalizePath,
} from '../../scripts/compliance-data.js';

const SNAPSHOT_ADMIN = 'https://tools.aem.live/tools/snapshot-admin/index.html';
const FILTERS = [['all', 'All'], ['pending', 'Pending review'], ['changes', 'Changes requested'], ['approved', 'Approved']];

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

function fmt(date) {
  return new Date(date).toLocaleString('en-CA', {
    month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit',
  });
}

/** Real preview/publish times from the AEM Admin API (best effort, read-only). */
async function addLiveStatus(item, path) {
  const { org, site, ref } = siteInfo();
  try {
    const resp = await fetch(`https://admin.hlx.page/status/${org}/${site}/${ref}${normalizePath(path)}`);
    if (!resp.ok) return;
    const json = await resp.json();
    const parts = [];
    if (json.preview && json.preview.lastModified) parts.push(`Previewed ${fmt(json.preview.lastModified)}`);
    parts.push(json.live && json.live.status === 200 && json.live.lastModified
      ? `Published ${fmt(json.live.lastModified)}` : 'Not published yet');
    item.querySelector('.cq-live').textContent = parts.join(' \u00b7 ');
  } catch (e) {
    // offline or not allowed: leave the field empty
  }
}

function renderItem(row, rerender) {
  const key = statusKey(row.Status);
  const s = STATUS[key];
  const path = row.Page;
  const item = el('li', { class: `cq-item status-${s.tone}` });
  const head = el(
    'div',
    { class: 'cq-head' },
    el('span', { class: 'cq-pill', text: s.label }),
    row.Local ? el('span', { class: 'cq-local', text: 'demo action in this browser' }) : null,
  );
  const title = el('h3', {}, el('a', { href: path, text: row.Title || path }));
  const meta = el(
    'p',
    { class: 'cq-meta' },
    `${row.Site || ''}${row.Site ? ' \u00b7 ' : ''}${path}`,
    el('br'),
    `Submitted by ${row['Submitted By'] || 'unknown'} on ${row.Submitted || '-'}`,
    row.Reviewer ? ` \u00b7 Reviewer: ${row.Reviewer}` : '',
    row['Decision Date'] ? ` \u00b7 Decision: ${row['Decision Date']}` : '',
    row.Snapshot ? el('span', {}, el('br'), `Review snapshot: ${row.Snapshot}`) : null,
  );
  const notes = row.Notes ? el('p', { class: 'cq-notes', text: row.Notes }) : null;
  const live = el('p', { class: 'cq-live' });

  const actions = el(
    'div',
    { class: 'cq-actions' },
    el('a', { class: 'button secondary', href: path, text: 'Open preview' }),
  );
  if (key === 'pending') {
    const approve = el('button', { type: 'button', class: 'button primary', text: 'Approve' });
    const changes = el('button', { type: 'button', class: 'button secondary', text: 'Request changes' });
    const reasonWrap = el(
      'div',
      { class: 'cq-reason', hidden: '' },
      el('label', { for: `r-${path}`, text: 'What needs to change?' }),
      el('textarea', { id: `r-${path}`, rows: '2' }),
      el('button', { type: 'button', class: 'button primary', text: 'Send back to advisor' }),
    );
    approve.addEventListener('click', () => {
      saveDecision(path, { Status: 'Approved', Reviewer: 'R. Castillo (you)', Notes: 'Approved in the demo.' });
      rerender(`Approved "${row.Title}". In production this publishes the locked review version.`);
    });
    changes.addEventListener('click', () => {
      reasonWrap.hidden = false;
      reasonWrap.querySelector('textarea').focus();
    });
    reasonWrap.querySelector('button').addEventListener('click', () => {
      const note = reasonWrap.querySelector('textarea').value.trim() || 'Please revise and resubmit.';
      saveDecision(path, { Status: 'Changes requested', Reviewer: 'R. Castillo (you)', Notes: note });
      rerender(`Sent "${row.Title}" back to ${row['Submitted By'] || 'the advisor'}.`);
    });
    actions.append(approve, changes);
    item.append(...[head, title, meta, notes, live, actions, reasonWrap].filter(Boolean));
  } else {
    if (key === 'approved') actions.append(el('span', { class: 'cq-ready', text: 'Ready to publish' }));
    item.append(...[head, title, meta, notes, live, actions].filter(Boolean));
  }
  addLiveStatus(item, path);
  return item;
}

export default async function decorate(block) {
  block.textContent = '';
  const status = el('p', { class: 'cq-toast', role: 'status' });
  const summary = el('div', { class: 'cq-summary' });
  const filters = el('div', { class: 'cq-filters', role: 'group', 'aria-label': 'Filter by status' });
  const list = el('ul', { class: 'cq-list' });
  const footer = el('p', { class: 'cq-source' });
  const reset = el('button', { type: 'button', class: 'button secondary cq-reset', text: 'Reset demo' });
  let filter = 'all';

  const render = async (message) => {
    const { rows, source } = await getQueue();
    const counts = { pending: 0, changes: 0, approved: 0 };
    rows.forEach((r) => { const k = statusKey(r.Status); if (k in counts) counts[k] += 1; });
    summary.replaceChildren(...Object.entries(counts).map(([k, n]) => el(
      'div',
      { class: `cq-count status-${k}` },
      el('strong', { text: `${n}` }),
      el('span', { text: STATUS[k].label }),
    )));
    filters.replaceChildren(...FILTERS.map(([k, label]) => {
      const b = el('button', {
        type: 'button', class: 'cq-filter', 'aria-pressed': `${filter === k}`, text: label,
      });
      b.addEventListener('click', () => { filter = k; render(); });
      return b;
    }));
    const visible = rows.filter((r) => filter === 'all' || statusKey(r.Status) === filter);
    list.replaceChildren(...visible.map((r) => renderItem(r, render)));
    if (!visible.length) list.append(el('li', { class: 'cq-empty', text: 'Nothing here.' }));
    footer.replaceChildren(
      source === 'sheet' ? 'Queue source: the compliance-queue sheet in the content folder. ' : 'Queue source: built-in demo data. ',
      'Snapshots and approvals in production: ',
      el('a', { href: SNAPSHOT_ADMIN, text: 'AEM snapshot admin' }),
      '.',
    );
    status.textContent = message || '';
    status.hidden = !message;
  };

  reset.addEventListener('click', () => { resetDemo(); filter = 'all'; render('Demo reset.'); });
  block.append(summary, el('div', { class: 'cq-toolbar' }, filters, reset), status, list, footer);
  await render();
}
