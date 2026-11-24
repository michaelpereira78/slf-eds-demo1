/**
 * Compliance review data for the demo.
 *
 * Sources, in order of precedence:
 *  1. Decisions and review requests made in THIS browser during a demo (localStorage),
 *     so a presenter can click Approve / Request changes without a backend.
 *  2. The `compliance-queue` Google Sheet in the content folder, served as /compliance-queue.json.
 *     Compliance owns this sheet; authors cannot edit it.
 *  3. Fallback demo data in the code repo (/tools/compliance/demo-queue.json).
 *  4. For a single page: its own `Compliance Status` metadata.
 */
import { getMetadata } from './aem.js';

const KEY = 'advisor-demo-compliance';
const SHEET = '/compliance-queue.json';
const FALLBACK = '/tools/compliance/demo-queue.json';

export const STATUS = {
  approved: { label: 'Approved', tone: 'approved' },
  pending: { label: 'Pending review', tone: 'pending' },
  changes: { label: 'Changes requested', tone: 'changes' },
  draft: { label: 'Not yet submitted', tone: 'draft' },
};

export function statusKey(value = '') {
  const v = value.toLowerCase();
  if (v.startsWith('approved')) return 'approved';
  if (v.includes('pending') || v.includes('review')) return 'pending';
  if (v.includes('change') || v.includes('reject')) return 'changes';
  return 'draft';
}

/** "/harbourview/index" and "/harbourview" both become "/harbourview/" */
export function normalizePath(path = '/') {
  let p = path.split(/[?#]/)[0].replace(/\.plain\.html$|\.html$/, '');
  if (p.endsWith('/index')) p = p.slice(0, -5);
  return p || '/';
}

function samePath(a, b) {
  const strip = (p) => normalizePath(p).replace(/\/$/, '') || '/';
  return strip(a) === strip(b);
}

/**
 * org / site / ref of the current preview host,
 * e.g. main--slf-eds-demo1--michaelpereira78.aem.page
 */
export function siteInfo(host = window.location.hostname) {
  const m = host.match(/^([a-z0-9-]+)--([a-z0-9-]+)--([a-z0-9-]+)\.aem\.(page|live|reviews)$/);
  if (m) {
    const parts = host.split('.')[0].split('--');
    const [ref, site, org] = parts.slice(-3);
    return { ref, site, org };
  }
  return { ref: 'main', site: 'slf-eds-demo1', org: 'michaelpereira78' };
}

export function previewUrl(path) {
  const { ref, site, org } = siteInfo();
  return `https://${ref}--${site}--${org}.aem.page${path}`;
}

function readLocal() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || { requests: [], decisions: {} };
  } catch (e) {
    return { requests: [], decisions: {} };
  }
}

function writeLocal(state) {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch (e) {
    // storage unavailable (private mode): the demo still works for this page view
  }
}

export function today() {
  const d = new Date();
  const pad = (n) => `${n}`.padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

export function saveRequest(request) {
  const state = readLocal();
  state.requests = state.requests.filter((r) => !samePath(r.Page, request.Page));
  state.requests.unshift({
    ...request, Status: 'Pending review', Submitted: today(), Local: true,
  });
  delete state.decisions[normalizePath(request.Page)];
  writeLocal(state);
}

export function saveDecision(path, decision) {
  const state = readLocal();
  state.decisions[normalizePath(path)] = { ...decision, 'Decision Date': today() };
  writeLocal(state);
}

export function resetDemo() {
  try {
    localStorage.removeItem(KEY);
  } catch (e) {
    // ignore
  }
}

function rowsFromJson(json) {
  if (Array.isArray(json.data)) return json.data;
  const names = json[':names'] || Object.keys(json).filter((k) => !k.startsWith(':'));
  const first = names.map((n) => json[n]).find((s) => s && Array.isArray(s.data));
  return first ? first.data : [];
}

let cached;
async function fetchSource() {
  if (!cached) {
    cached = (async () => {
      const local = ['localhost', '127.0.0.1'].includes(window.location.hostname);
      // locally there is no content sheet, so go straight to the demo data
      const sources = local ? [[FALLBACK, 'demo']] : [[SHEET, 'sheet'], [FALLBACK, 'demo']];
      const tryNext = async (i) => {
        if (i >= sources.length) return { rows: [], source: 'none' };
        const [url, source] = sources[i];
        try {
          const resp = await fetch(url, { cache: 'no-store' });
          if (resp.ok) {
            const rows = rowsFromJson(await resp.json());
            if (rows.length) return { rows, source };
          }
        } catch (e) {
          // fall through to the next source
        }
        return tryNext(i + 1);
      };
      return tryNext(0);
    })();
  }
  return cached;
}

/** The full review queue, newest first, with this browser's demo actions applied. */
export async function getQueue() {
  const { rows, source } = await fetchSource();
  const state = readLocal();
  const merged = rows.map((r) => ({ ...r }));
  state.requests.forEach((req) => {
    const i = merged.findIndex((r) => samePath(r.Page, req.Page));
    if (i >= 0) {
      merged[i] = {
        ...merged[i],
        ...req,
        Title: merged[i].Title || req.Title,
        Site: merged[i].Site || req.Site,
        Notes: req.Notes || merged[i].Notes,
        'Decision Date': '',
      };
    } else merged.unshift(req);
  });
  Object.entries(state.decisions).forEach(([path, d]) => {
    const row = merged.find((r) => samePath(r.Page, path));
    if (row) Object.assign(row, d, { Local: true });
  });
  merged.sort((a, b) => `${b.Submitted}`.localeCompare(`${a.Submitted}`));
  return { rows: merged, source };
}

/** Status of one page: queue first, then the page's own metadata. */
export async function getPageStatus(path = window.location.pathname) {
  const { rows } = await getQueue();
  const row = rows.find((r) => samePath(r.Page, path));
  if (row) return { key: statusKey(row.Status), row };
  const meta = getMetadata('compliance-status');
  return {
    key: meta ? statusKey(meta) : 'draft',
    row: {
      Page: normalizePath(path),
      Status: meta,
      Reviewer: getMetadata('approved-by') || getMetadata('reviewer'),
      'Decision Date': getMetadata('approval-date') || getMetadata('review-date'),
    },
  };
}
