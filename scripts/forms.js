/**
 * Form submissions: Figma import requests, layout change requests and the compliance audit log.
 *
 * Where a submission goes is set per form in FORMS below (or per page, with the block's
 * "Submit to" row):
 *  - A sheet path such as '/forms/compliance-audit-log': the row is sent to Adobe's Forms
 *    Submission Service (https://forms.adobe.com/adobe/forms/af/submit/...), which appends it to the
 *    `incoming` tab of that Google Sheet in the site's Drive folder. This is the same request the
 *    AEM Forms "form" block makes for document-based forms. Requires the sheet to be set up as in
 *    docs/ADMIN-SETUP.md (incoming tab, shared with forms@adobe.com, previewed and
 *    published) and the repository to be enabled for the service by Adobe.
 *  - A full https URL (for example a Google Apps Script web app, docs/apps-script/):
 *    the row is POSTed
 *    as JSON. Use this if the Forms Submission Service is not available to you.
 *  - '' (empty): demo mode, nothing leaves the browser.
 *
 * Every submission is also kept in this browser (localStorage), so the demo consoles can list it
 * and the presenter always sees a confirmation, even before the sheets exist.
 */
import { siteInfo } from './compliance-data.js';

export const FORMS = {
  'compliance-audit': {
    endpoint: '/forms/compliance-audit-log',
    destination: 'compliance-audit-log sheet (incoming tab)',
  },
  'figma-import': {
    endpoint: '/forms/figma-import-requests',
    destination: 'MarTech Engineering intake sheet (figma-import-requests)',
  },
  'layout-change': {
    endpoint: '/forms/layout-change-requests',
    destination: 'layout-change-requests sheet',
  },
};

/** Column order for the audit log (also the header row of the sheet's incoming tab). */
export const AUDIT_COLUMNS = ['timestamp', 'event', 'advisor', 'site', 'pagePath', 'changeSummary',
  'submittedBy', 'status', 'reviewer', 'decisionDate', 'notes', 'reference', 'source'];

const LOCAL_KEY = 'advisor-demo-submissions';
const SUBMISSION_SERVICE = 'https://forms.adobe.com/adobe/forms/af/submit/';
const TIMEOUT = 10000;

function readLocal() {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function writeLocal(list) {
  try {
    localStorage.setItem(LOCAL_KEY, JSON.stringify(list.slice(0, 100)));
  } catch (e) {
    // storage unavailable: the confirmation still shows
  }
}

/** Submissions made in this browser, newest first (optionally for one form). */
export function localSubmissions(formId) {
  return readLocal().filter((s) => !formId || s.form === formId);
}

export function clearLocalSubmissions(formId) {
  writeLocal(readLocal().filter((s) => formId && s.form !== formId));
}

/** A short human reference such as FIG-1125-4K7Q. */
export function makeReference(prefix) {
  const d = new Date();
  const pad = (n) => `${n}`.padStart(2, '0');
  const rand = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `${prefix}-${pad(d.getMonth() + 1)}${pad(d.getDate())}-${rand}`;
}

export function nowStamp() {
  // ISO-like local time (the sheet sorts and filters on it)
  const d = new Date();
  const pad = (n) => `${n}`.padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

async function postWithTimeout(url, options) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT);
  try {
    return await fetch(url, { ...options, signal: ctrl.signal });
  } finally {
    clearTimeout(t);
  }
}

async function sendToSheet(path, data) {
  const { ref, site, org } = siteInfo();
  const host = window.location.hostname;
  const formHost = host.endsWith('.aem.page') || host.endsWith('.aem.live') ? host : `${ref}--${site}--${org}.aem.page`;
  const resp = await postWithTimeout(`${SUBMISSION_SERVICE}${btoa(`${path}.json`)}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-adobe-routing': `tier=live,bucket=${ref}--${site}--${org}`,
      'x-adobe-form-hostname': formHost,
    },
    body: JSON.stringify({ data }),
  });
  if (!resp.ok) throw new Error(`Forms Submission Service answered ${resp.status}`);
}

async function sendToWebhook(url, data) {
  // text/plain keeps this a "simple" request (no CORS preflight), which Apps Script web apps need
  await postWithTimeout(url, {
    method: 'POST',
    mode: 'no-cors',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(data),
  });
}

/**
 * Sends one row. Never throws: returns how it was recorded.
 * @param {string} formId key of FORMS
 * @param {Object<string,string>} data flat field values (keys = sheet column headers)
 * @param {string} [endpointOverride] sheet path or https URL from the authored block
 * @returns {Promise<{mode: 'sheet'|'webhook'|'demo', destination: string, error?: string}>}
 */
export async function submitForm(formId, data, endpointOverride) {
  const form = FORMS[formId] || { endpoint: '', destination: formId };
  const endpoint = (endpointOverride ?? form.endpoint ?? '').trim();
  const row = Object.fromEntries(Object.entries(data).map(([k, v]) => [k, v == null ? '' : `${v}`]));
  let result = { mode: 'demo', destination: 'this browser only (demo mode)' };
  // local development never sends anything unless asked to (?forms=live)
  const local = ['localhost', '127.0.0.1'].includes(window.location.hostname)
    && !new URLSearchParams(window.location.search).has('forms');
  if (local) {
    result.destination = 'this browser only (local development)';
  } else {
    try {
      if (/^https:\/\//.test(endpoint)) {
        await sendToWebhook(endpoint, row);
        result = { mode: 'webhook', destination: form.destination };
      } else if (endpoint.startsWith('/')) {
        await sendToSheet(endpoint, row);
        result = { mode: 'sheet', destination: form.destination };
      }
    } catch (e) {
      result = { mode: 'demo', destination: 'this browser only (the sheet is not connected yet)', error: e.message };
    }
  }
  const list = readLocal();
  list.unshift({
    form: formId, data: row, mode: result.mode, at: new Date().toISOString(),
  });
  writeLocal(list);
  return result;
}

/**
 * Appends one event to the compliance audit log.
 * Events: Submitted, Approved, Changes requested, Published.
 */
export function logAudit(event) {
  const row = Object.fromEntries(AUDIT_COLUMNS.map((c) => [c, '']));
  Object.assign(row, {
    timestamp: nowStamp(),
    source: window.location.hostname,
    ...event,
  });
  if (!row.reference) row.reference = makeReference('AUD');
  return submitForm('compliance-audit', row).then((result) => {
    document.dispatchEvent(new CustomEvent('audit:logged', { detail: { row, result } }));
    return result;
  });
}
