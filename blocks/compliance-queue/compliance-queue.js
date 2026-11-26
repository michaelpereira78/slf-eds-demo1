import {
  STATUS, statusKey, getQueue, saveDecision, resetDemo, siteInfo, normalizePath,
} from '../../scripts/compliance-data.js';
import { logAudit } from '../../scripts/forms.js';

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

let statusDenied = false;

/**
 * Real preview/publish times from the AEM Admin API (best effort, read-only).
 * Once roles are configured the Admin API needs a signed-in user, so we only ask
 * when the Sidekick is on the page (or ?status=live) and stop after the first 401/403.
 */
function canReadStatus() {
  if (statusDenied) return false;
  const params = new URLSearchParams(window.location.search);
  return params.get('status') === 'live' || !!document.querySelector('aem-sidekick, helix-sidekick');
}

async function addLiveStatus(item, path) {
  if (!canReadStatus()) return;
  const { org, site, ref } = siteInfo();
  try {
    const resp = await fetch(`https://admin.hlx.page/status/${org}/${site}/${ref}${normalizePath(path)}`, { credentials: 'include' });
    if (resp.status === 401 || resp.status === 403) statusDenied = true;
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

function audit(row, event, notes) {
  logAudit({
    event,
    advisor: row['Submitted By'] || '',
    site: row.Site || '',
    pagePath: normalizePath(row.Page),
    changeSummary: row.Notes || '',
    submittedBy: row['Submitted By'] || '',
    status: event,
    reviewer: 'R. Castillo (supervisor)',
    decisionDate: new Date().toISOString().slice(0, 10),
    notes,
  });
}

function renderItem(row, rerender, readOnly) {
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
  if (readOnly) {
    if (key === 'changes') actions.append(el('span', { class: 'cq-ready cq-todo', text: 'Edit the page, Preview, then resubmit' }));
    if (key === 'approved') actions.append(el('span', { class: 'cq-ready', text: 'Approved: your supervisor publishes it' }));
    if (key === 'pending') actions.append(el('span', { class: 'cq-ready cq-wait', text: 'With Compliance' }));
    item.append(...[head, title, meta, notes, live, actions].filter(Boolean));
  } else if (key === 'pending') {
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
      audit(row, 'Approved', 'Approved as submitted.');
      rerender(`Approved "${row.Title}" and logged it in the audit sheet. Next: open the preview and click Publish in Sidekick.`);
    });
    changes.addEventListener('click', () => {
      reasonWrap.hidden = false;
      reasonWrap.querySelector('textarea').focus();
    });
    reasonWrap.querySelector('button').addEventListener('click', () => {
      const note = reasonWrap.querySelector('textarea').value.trim() || 'Please revise and resubmit.';
      saveDecision(path, { Status: 'Changes requested', Reviewer: 'R. Castillo (you)', Notes: note });
      audit(row, 'Changes requested', note);
      rerender(`Sent "${row.Title}" back to ${row['Submitted By'] || 'the advisor'} and logged it in the audit sheet.`);
    });
    actions.append(approve, changes);
    item.append(...[head, title, meta, notes, live, actions, reasonWrap].filter(Boolean));
  } else {
    if (key === 'approved') actions.append(el('span', { class: 'cq-ready', text: 'Ready to publish (Sidekick > Publish)' }));
    item.append(...[head, title, meta, notes, live, actions].filter(Boolean));
  }
  addLiveStatus(item, path);
  return item;
}

function readConfig(block) {
  const config = {};
  [...block.children].forEach((row) => {
    const [k, v] = row.children;
    if (!k) return;
    const link = v && v.querySelector('a[href]');
    let value = v ? v.textContent.trim() : '';
    if (link) value = link.getAttribute('href');
    config[k.textContent.trim().toLowerCase()] = value;
  });
  return config;
}

export default async function decorate(block) {
  // (Mine) variant: the advisor's read-only view of their own submissions
  // (Summary) variant: just the status counts, used on the workspace dashboards
  const readOnly = block.classList.contains('mine');
  const summaryOnly = block.classList.contains('summary');
  const config = readConfig(block);
  const viewAll = config['view all'] || config.link
    || (readOnly ? '/advisor/submissions' : '/admin/approvals');
  block.textContent = '';
  let who = '';
  const picker = readOnly ? el('select', { class: 'cq-who', id: 'cq-who', 'aria-label': 'Show submissions for' }) : null;
  const status = el('p', { class: 'cq-toast', role: 'status' });
  const summary = el('div', { class: 'cq-summary' });
  const filters = el('div', { class: 'cq-filters', role: 'group', 'aria-label': 'Filter by status' });
  const list = el('ul', { class: 'cq-list' });
  const footer = el('p', { class: 'cq-source' });
  const reset = el('button', { type: 'button', class: 'button secondary cq-reset', text: 'Reset demo' });
  let filter = 'all';

  const render = async (message) => {
    const { rows: allRows, source } = await getQueue();
    if (picker) {
      const names = [...new Set(allRows.map((r) => r['Submitted By']).filter(Boolean))];
      if (!who) [who] = names;
      picker.replaceChildren(...names.map((n) => {
        const o = el('option', { value: n, text: n });
        if (n === who) o.selected = true;
        return o;
      }));
    }
    const rows = readOnly ? allRows.filter((r) => r['Submitted By'] === who) : allRows;
    const counts = { pending: 0, changes: 0, approved: 0 };
    rows.forEach((r) => { const k = statusKey(r.Status); if (k in counts) counts[k] += 1; });
    summary.replaceChildren(...Object.entries(counts).map(([k, n]) => el(
      summaryOnly ? 'a' : 'div',
      { class: `cq-count status-${k}`, ...(summaryOnly ? { href: viewAll } : {}) },
      el('strong', { text: `${n}` }),
      el('span', { text: STATUS[k].label }),
    )));
    if (summaryOnly) return;
    filters.replaceChildren(...FILTERS.map(([k, label]) => {
      const b = el('button', {
        type: 'button', class: 'cq-filter', 'aria-pressed': `${filter === k}`, text: label,
      });
      b.addEventListener('click', () => { filter = k; render(); });
      return b;
    }));
    const visible = rows.filter((r) => filter === 'all' || statusKey(r.Status) === filter);
    list.replaceChildren(...visible.map((r) => renderItem(r, render, readOnly)));
    if (!visible.length) list.append(el('li', { class: 'cq-empty', text: 'Nothing here.' }));
    footer.replaceChildren(...(readOnly ? [
      'Your supervisor reviews each submission and publishes it once Compliance approves. ',
      'Every submission and decision is written to the compliance audit log.',
    ] : [
      source === 'sheet' ? 'Queue source: the compliance-queue sheet in the content folder. ' : 'Queue source: built-in demo data. ',
      'Snapshots and approvals in production: ',
      el('a', { href: SNAPSHOT_ADMIN, text: 'AEM snapshot admin' }),
      '.',
    ]));
    status.textContent = message || '';
    status.hidden = !message;
  };

  reset.addEventListener('click', () => { resetDemo(); filter = 'all'; render('Demo reset.'); });
  if (picker) {
    picker.addEventListener('change', () => { who = picker.value; render(); });
    block.append(el('div', { class: 'cq-whobar' }, el('label', { for: 'cq-who', text: 'Signed in as (demo):' }), picker));
  }
  if (summaryOnly) {
    const all = el('p', { class: 'cq-viewall' }, el('a', { href: viewAll, class: 'button secondary', text: readOnly ? 'View my submissions' : 'Open the approval queue' }));
    block.append(summary, all);
  } else {
    block.append(summary, el('div', { class: 'cq-toolbar' }, filters, readOnly ? null : reset), status, list, footer);
  }
  document.addEventListener('request-form:submitted', () => render());
  await render();
}
