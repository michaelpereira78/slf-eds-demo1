/**
 * Compliance status bar and "Request review" dialog.
 * Loaded only on authoring hosts (local, *.aem.page, *.aem.reviews), never on the live site.
 * Also reacts to the Sidekick custom plugin event `custom:request-compliance-review`.
 */
import { loadCSS } from './aem.js';
import {
  STATUS, getPageStatus, saveRequest, normalizePath,
} from './compliance-data.js';
import { logAudit } from './forms.js';

const COMPLIANCE_EMAIL = 'compliance@example.com';
const SKIP = ['/compliance', '/tools/', '/fragments/', '/nav', '/footer'];

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

function describe(key, row) {
  const who = row.Reviewer ? ` by ${row.Reviewer}` : '';
  const when = row['Decision Date'] ? ` on ${row['Decision Date']}` : '';
  if (key === 'approved') return `Approved${who}${when}. Ready to publish.`;
  if (key === 'pending') return `Submitted${row['Submitted By'] ? ` by ${row['Submitted By']}` : ''}${row.Submitted ? ` on ${row.Submitted}` : ''}. Waiting for Compliance. Do not publish yet.`;
  if (key === 'changes') return `Sent back${who}${when}${row.Notes ? `: ${row.Notes}` : '.'}`;
  return 'This version has not been reviewed. Request a review before publishing.';
}

let dialog;

function siteName() {
  const parts = document.title.split('|').map((t) => t.trim());
  return parts[1] && parts[1] !== 'Advisor Demo' ? parts[1] : parts[0];
}

function buildDialog(onDone) {
  const title = document.title.split('|')[0].trim();
  const path = normalizePath(window.location.pathname);
  const form = el(
    'form',
    { method: 'dialog', class: 'compliance-form' },
    el('h2', { id: 'compliance-dialog-title', text: 'Request compliance review' }),
    el('p', { class: 'compliance-page', text: `${title} (${path})` }),
    el('label', { for: 'cr-name', text: 'Your name' }),
    el('input', {
      id: 'cr-name', name: 'name', required: '', value: 'Demo Advisor', autocomplete: 'name',
    }),
    el('label', { for: 'cr-team', text: 'Review team' }),
    el(
      'select',
      { id: 'cr-team', name: 'team' },
      el('option', { text: 'Advisor marketing compliance' }),
      el('option', { text: 'Insurance compliance' }),
      el('option', { text: 'Investments compliance' }),
    ),
    el('label', { for: 'cr-notes', text: 'What changed?' }),
    el('textarea', {
      id: 'cr-notes', name: 'notes', rows: '3', placeholder: 'For example: new team member and updated bio',
    }),
    el(
      'fieldset',
      {},
      el('legend', { text: 'Checklist' }),
      ...[
        'The regulatory disclosure is on the page',
        'Product wording comes from approved content',
        'Names, credentials and contact details are correct',
      ].map((t, i) => el('label', { class: 'check' }, el('input', { type: 'checkbox', required: '', name: `c${i}` }), ` ${t}`)),
    ),
    el(
      'div',
      { class: 'compliance-actions' },
      el('button', {
        type: 'button', class: 'button secondary', value: 'cancel', text: 'Cancel',
      }),
      el('button', { type: 'submit', class: 'button primary', text: 'Submit for review' }),
    ),
  );

  const done = el('div', { class: 'compliance-done', hidden: '' });
  dialog = el('dialog', { class: 'compliance-dialog', 'aria-labelledby': 'compliance-dialog-title' }, form, done);
  form.querySelector('button[value="cancel"]').addEventListener('click', () => dialog.close());
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(form);
    saveRequest({
      Page: path,
      Title: title,
      Site: siteName(),
      'Submitted By': data.get('name'),
      Reviewer: data.get('team'),
      Notes: data.get('notes'),
    });
    // audit trail: one row per submission in the compliance-audit-log sheet
    const logged = logAudit({
      event: 'Submitted',
      advisor: data.get('name'),
      site: siteName(),
      pagePath: path,
      changeSummary: data.get('notes'),
      submittedBy: data.get('name'),
      status: 'Pending review',
      reviewer: data.get('team'),
      notes: 'Checklist confirmed (3 of 3)',
    });
    const body = encodeURIComponent(`Please review: ${window.location.href}\n\nWhat changed: ${data.get('notes') || '-'}\nSubmitted by: ${data.get('name')}`);
    done.replaceChildren(
      el('h2', { text: 'Review requested' }),
      el('p', { text: `${data.get('team')} can now see this page in the review queue. You will be told when it is approved or if changes are needed.` }),
      el('p', { class: 'compliance-note compliance-audit', text: 'Adding this submission to the compliance audit log\u2026' }),
      el('p', { class: 'compliance-note', text: 'Your supervisor publishes the page once Compliance approves it. Advisors can edit and preview, but cannot publish.' }),
      el(
        'div',
        { class: 'compliance-actions' },
        el('a', { class: 'button secondary', href: `mailto:${COMPLIANCE_EMAIL}?subject=${encodeURIComponent(`Review request: ${title}`)}&body=${body}`, text: 'Also email Compliance' }),
        el('a', { class: 'button primary', href: '/compliance', text: 'Open the review queue' }),
      ),
    );
    form.hidden = true;
    done.hidden = false;
    logged.then((r) => {
      const line = done.querySelector('.compliance-audit');
      if (line) {
        line.textContent = r.mode === 'demo'
          ? `Audit log: saved in ${r.destination}.`
          : `Audit log: recorded in the ${r.destination}.`;
      }
    });
    onDone();
  });
  dialog.addEventListener('close', () => {
    form.hidden = false;
    done.hidden = true;
  });
  document.body.append(dialog);
}

export async function openRequestDialog(onDone = () => {}) {
  await loadCSS(`${window.hlx.codeBasePath}/styles/compliance.css`);
  if (!dialog) buildDialog(onDone);
  dialog.showModal();
}

async function renderBar(bar, status) {
  const { key, row } = status || await getPageStatus();
  const s = STATUS[key];
  bar.className = `compliance-bar status-${s.tone}`;
  const actions = [];
  if (key !== 'approved' && key !== 'pending') {
    const btn = el('button', { type: 'button', class: 'compliance-request', text: 'Request review' });
    btn.addEventListener('click', () => openRequestDialog(() => renderBar(bar)));
    actions.push(btn);
  }
  actions.push(el('a', { href: '/compliance', class: 'compliance-queue-link', text: 'Review queue' }));
  const close = el('button', {
    type: 'button', class: 'compliance-close', 'aria-label': 'Hide compliance status', text: '\u00d7',
  });
  close.addEventListener('click', () => {
    bar.hidden = true;
    document.body.style.removeProperty('--author-bar-height');
  });
  bar.replaceChildren(
    el('span', { class: 'compliance-dot', 'aria-hidden': 'true' }),
    el('p', {}, el('strong', { text: `Compliance: ${s.label}` }), el('span', { text: describe(key, row) })),
    el('div', { class: 'compliance-bar-actions' }, ...actions, close),
  );
  document.body.style.setProperty('--author-bar-height', `${bar.offsetHeight}px`);
}

let signedInAs = '';

function listenToSidekick() {
  const handler = () => {
    const bar = document.querySelector('.compliance-bar');
    openRequestDialog(() => bar && renderBar(bar));
  };
  const attach = (sk) => {
    sk.addEventListener('custom:request-compliance-review', handler);
    // remember who is signed in to Sidekick (the Admin API status includes the profile)
    sk.addEventListener('status-fetched', ({ detail }) => {
      const p = detail && detail.profile;
      if (p) signedInAs = p.email || p.name || signedInAs;
    });
    sk.addEventListener('logged-in', ({ detail }) => {
      if (detail) signedInAs = detail.email || detail.name || signedInAs;
    });
    // Publish only works for the publish role (enforced by the Admin API);
    // log it for the audit trail
    sk.addEventListener('published', ({ detail }) => {
      const paths = Array.isArray(detail) ? detail : [detail];
      paths.filter(Boolean).forEach((p) => logAudit({
        event: 'Published',
        site: siteName(),
        pagePath: normalizePath(p),
        submittedBy: signedInAs,
        reviewer: signedInAs,
        status: 'Published',
        decisionDate: new Date().toISOString().slice(0, 10),
        notes: 'Published from Sidekick',
      }));
    });
  };
  const sk = document.querySelector('aem-sidekick');
  if (sk) attach(sk);
  else document.addEventListener('sidekick-ready', () => attach(document.querySelector('aem-sidekick')), { once: true });
}

export default async function init() {
  const path = window.location.pathname;
  listenToSidekick();
  if (SKIP.some((p) => path.startsWith(p))) return;
  const status = await getPageStatus();
  // pages outside the review process (e.g. the demo's own guide pages) have no status at all
  if (!status.row.Status) return;
  await loadCSS(`${window.hlx.codeBasePath}/styles/compliance.css`);
  const bar = el('aside', { class: 'compliance-bar', 'aria-label': 'Compliance status (visible on preview only)' });
  document.body.append(bar);
  await renderBar(bar, status);
}
