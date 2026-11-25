/**
 * Request Form block: the platform's intake forms.
 *
 * Authoring (two-column rows):
 *   Form          figma-import | layout-change | compliance-review
 *   Submit to     optional: a sheet path (/forms/...) or an https web-app URL;
 *                 defaults per form in scripts/forms.js
 *   Confirmation  optional: the sentence shown after a successful submit
 *
 * Field sets live in FIELDS below so the column names always match the sheet's `incoming` tab
 * (see docs/ADMIN-SETUP.md for the exact header rows).
 */
import {
  FORMS, submitForm, makeReference, nowStamp, logAudit,
} from '../../scripts/forms.js';
import { saveRequest, normalizePath } from '../../scripts/compliance-data.js';

const SITES = ['Maple Ridge Wealth Partners', 'Harbourview Financial Group', 'Northstar Planning'];
const SITE_PATHS = {
  'Maple Ridge Wealth Partners': '/', 'Harbourview Financial Group': '/harbourview/', 'Northstar Planning': '/northstar/',
};

const FIELDS = {
  'figma-import': {
    prefix: 'FIG',
    title: 'Import a custom website design from Figma',
    button: 'Send to MarTech Engineering',
    done: 'Request sent to MarTech Engineering',
    confirmation: 'MarTech Engineering will review the Figma file, confirm the scope and timeline by email, '
      + 'then run their agentic Figma-to-EDS build. The new design is built from approved blocks and goes '
      + 'through code review and Compliance before anything is published.',
    fields: [
      {
        name: 'figmaUrl', label: 'Figma file URL', type: 'url', required: true, placeholder: 'https://www.figma.com/design/...', pattern: 'https://(www\\.)?figma\\.com/.+', hint: 'Share the file with view access for martech-engineering@example.com.',
      },
      {
        name: 'siteName', label: 'Advisor or site name', required: true, placeholder: 'e.g. Prairie Sky Financial',
      },
      {
        name: 'requester', label: 'Requested by', required: true, autocomplete: 'name', placeholder: 'Your name',
      },
      {
        name: 'email', label: 'Contact email', type: 'email', required: true, autocomplete: 'email', placeholder: 'name@example.com',
      },
      {
        name: 'deadline', label: 'Needed by', type: 'date', required: true,
      },
      {
        name: 'theme', label: 'Brand / theme', type: 'select', required: true, options: ['Use the design in the Figma file (new theme)', 'Forest', 'Harbour', 'Slate'],
      },
      {
        name: 'pages', label: 'Pages needed', type: 'checkboxes', options: ['Home', 'Team', 'Advisor profile', 'Services', 'Contact', 'Campaign landing page', 'Other (see notes)'], wide: true,
      },
      {
        name: 'notes', label: 'Notes for MarTech Engineering', type: 'textarea', placeholder: 'Anything the team should know: fonts, imagery, must-keep content, launch event...', wide: true,
      },
    ],
    extra: () => ({ requestType: 'Figma import', status: 'New' }),
  },
  'layout-change': {
    prefix: 'LAY',
    title: 'Request a layout change',
    button: 'Send request',
    done: 'Layout change requested',
    confirmation: 'Your supervisor will look at the request. Simple changes (a section style, a block variant) '
      + 'are usually done the same day; bigger ones go to MarTech Engineering.',
    fields: [
      {
        name: 'site', label: 'Your site', type: 'select', required: true, options: SITES,
      },
      {
        name: 'pagePath', label: 'Page', required: true, placeholder: 'e.g. /harbourview/ or /advisors/jordan-lee',
      },
      {
        name: 'change', label: 'What kind of change?', type: 'select', required: true, options: ['Change a section style (Light, Dark, Centered...)', 'Reorder or remove sections', 'Add a block (testimonials, stats, banner...)', 'Switch template', 'Something else'],
      },
      {
        name: 'requester', label: 'Your name', required: true, autocomplete: 'name',
      },
      {
        name: 'details', label: 'Describe the change', type: 'textarea', required: true, wide: true, placeholder: 'e.g. Move the testimonials above the team and make the contact band dark.',
      },
    ],
    extra: () => ({ status: 'New' }),
  },
  'compliance-review': {
    prefix: 'CR',
    title: 'Submit a change for compliance review',
    button: 'Submit for review',
    done: 'Submitted for compliance review',
    confirmation: 'Compliance can now see the page in the review queue, and the submission is in the audit log. '
      + 'Your supervisor publishes it once it is approved.',
    fields: [
      {
        name: 'advisor', label: 'Advisor', required: true, autocomplete: 'name', placeholder: 'e.g. Grace MacLeod',
      },
      {
        name: 'site', label: 'Site', type: 'select', required: true, options: SITES,
      },
      {
        name: 'pagePath', label: 'Page path', required: true, placeholder: 'e.g. /harbourview/',
      },
      {
        name: 'changeSummary', label: 'What changed?', type: 'textarea', required: true, wide: true, placeholder: 'e.g. New team member and updated bio',
      },
      {
        name: 'checks', label: 'Checklist', type: 'checkboxes', required: true, wide: true, options: ['The regulatory disclosure is on the page', 'Product wording comes from approved content', 'Names, credentials and contact details are correct'],
      },
    ],
  },
};

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (v === false || v == null) return;
    if (k === 'class') e.className = v;
    else if (k === 'text') e.textContent = v;
    else e.setAttribute(k, v === true ? '' : v);
  });
  children.flat().forEach((c) => c && e.append(c));
  return e;
}

function readConfig(block) {
  const config = {};
  [...block.children].forEach((row) => {
    const [k, v] = row.children;
    if (!k) return;
    const key = k.textContent.trim().toLowerCase().replace(/[^a-z]+/g, '-');
    const link = v && v.querySelector('a[href]');
    let value = v ? v.textContent.trim() : '';
    if (link) value = link.getAttribute('href');
    config[key] = value;
  });
  return config;
}

function fieldEl(formId, f) {
  const id = `${formId}-${f.name}`;
  const wrap = el('div', { class: `rf-field${f.wide ? ' rf-wide' : ''}` });
  if (f.type === 'checkboxes') {
    const fs = el('fieldset', { class: 'rf-checks', 'data-required': f.required || false });
    fs.append(el('legend', { text: f.label }));
    f.options.forEach((o, i) => {
      const cid = `${id}-${i}`;
      fs.append(el(
        'label',
        { for: cid, class: 'rf-check' },
        el('input', {
          type: 'checkbox', id: cid, name: f.name, value: o, required: f.required && formId === 'compliance-review',
        }),
        el('span', { text: o }),
      ));
    });
    wrap.append(fs);
    return wrap;
  }
  wrap.append(el('label', { for: id }, f.label, f.required ? el('span', { class: 'rf-req', 'aria-hidden': 'true', text: ' *' }) : null));
  let input;
  if (f.type === 'select') {
    input = el('select', { id, name: f.name, required: f.required });
    f.options.forEach((o) => input.append(el('option', { value: o, text: o })));
  } else if (f.type === 'textarea') {
    input = el('textarea', {
      id, name: f.name, rows: '4', required: f.required, placeholder: f.placeholder,
    });
  } else {
    input = el('input', {
      id,
      name: f.name,
      type: f.type || 'text',
      required: f.required,
      placeholder: f.placeholder,
      pattern: f.pattern,
      autocomplete: f.autocomplete,
    });
  }
  wrap.append(input);
  if (f.hint) wrap.append(el('p', { class: 'rf-hint', text: f.hint }));
  return wrap;
}

function collect(form, def) {
  const fd = new FormData(form);
  const data = {};
  def.fields.forEach((f) => {
    data[f.name] = f.type === 'checkboxes' ? fd.getAll(f.name).join('; ') : (fd.get(f.name) || '').trim();
  });
  return data;
}

function summaryList(def, data) {
  const dl = el('dl', { class: 'rf-summary' });
  def.fields.forEach((f) => {
    if (!data[f.name]) return;
    dl.append(el('dt', { text: f.label }), el('dd', { text: data[f.name] }));
  });
  return dl;
}

export default function decorate(block) {
  const config = readConfig(block);
  const formId = config.form || 'figma-import';
  const def = FIELDS[formId];
  block.textContent = '';
  if (!def) {
    block.append(el('p', { text: `Unknown form "${formId}".` }));
    return;
  }
  block.dataset.form = formId;

  const form = el('form', { class: 'rf-form', novalidate: true });
  const grid = el('div', { class: 'rf-grid' }, ...def.fields.map((f) => fieldEl(formId, f)));
  const error = el('p', { class: 'rf-error', role: 'alert', hidden: true });
  const submit = el('button', { type: 'submit', class: 'button primary', text: def.button });
  form.append(grid, error, el('div', { class: 'rf-actions' }, submit, el('p', { class: 'rf-dest', text: `Goes to: ${FORMS[formId === 'compliance-review' ? 'compliance-audit' : formId].destination}` })));

  // sensible defaults
  if (formId === 'figma-import') {
    const d = new Date(Date.now() + 21 * 864e5);
    form.querySelector('[name="deadline"]').value = d.toISOString().slice(0, 10);
  }
  const siteSelect = form.querySelector('select[name="site"]');
  const pathInput = form.querySelector('input[name="pagePath"]');
  if (siteSelect && pathInput) {
    pathInput.value = SITE_PATHS[siteSelect.value];
    siteSelect.addEventListener('change', () => { pathInput.value = SITE_PATHS[siteSelect.value]; });
  }

  const done = el('div', { class: 'rf-done', hidden: true, tabindex: '-1' });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    error.hidden = true;
    const checks = form.querySelector('fieldset[data-required]');
    const checksOk = !checks || formId !== 'compliance-review'
      || [...checks.querySelectorAll('input')].every((i) => i.checked);
    if (!form.checkValidity() || !checksOk) {
      error.textContent = checksOk ? 'Please fill in the highlighted fields.' : 'Please confirm all three checklist items.';
      error.hidden = false;
      form.classList.add('rf-validated');
      const first = form.querySelector(':invalid');
      if (first) first.focus();
      return;
    }
    submit.disabled = true;
    submit.textContent = 'Sending...';
    const data = collect(form, def);
    const reference = makeReference(def.prefix);
    let result;
    if (formId === 'compliance-review') {
      const path = normalizePath(data.pagePath);
      saveRequest({
        Page: path, Title: data.site, Site: data.site, 'Submitted By': data.advisor, Reviewer: 'Advisor marketing compliance', Notes: data.changeSummary,
      });
      result = await logAudit({
        event: 'Submitted',
        advisor: data.advisor,
        site: data.site,
        pagePath: path,
        changeSummary: data.changeSummary,
        submittedBy: data.advisor,
        status: 'Pending review',
        notes: `Checklist confirmed: ${data.checks}`,
        reference,
      });
    } else {
      result = await submitForm(formId, {
        submittedAt: nowStamp(),
        reference,
        ...data,
        ...(def.extra ? def.extra() : {}),
        page: window.location.pathname,
      }, config['submit-to'] || undefined);
    }
    const recorded = result.mode === 'demo'
      ? el('p', { class: 'rf-mode rf-mode-demo' }, el('strong', { text: 'Demo mode: ' }), `saved in ${result.destination}. `, 'Connect the sheet (docs/ADMIN-SETUP.md) to record it in Google Drive.')
      : el('p', { class: 'rf-mode rf-mode-live' }, el('strong', { text: 'Recorded: ' }), `added to the ${result.destination}.`);
    done.replaceChildren(
      el('span', { class: 'rf-done-icon', 'aria-hidden': 'true' }),
      el('h3', { text: def.done }),
      el('p', { class: 'rf-ref' }, 'Reference ', el('strong', { text: reference })),
      el('p', { text: config.confirmation || def.confirmation }),
      recorded,
      summaryList(def, data),
      el('p', { class: 'button-wrapper' }, el('button', { type: 'button', class: 'button secondary rf-again', text: 'Submit another request' })),
    );
    done.querySelector('.rf-again').addEventListener('click', () => {
      form.reset();
      if (pathInput && siteSelect) pathInput.value = SITE_PATHS[siteSelect.value];
      form.classList.remove('rf-validated');
      form.hidden = false;
      done.hidden = true;
      form.querySelector('input, select, textarea').focus();
    });
    submit.disabled = false;
    submit.textContent = def.button;
    form.hidden = true;
    done.hidden = false;
    done.focus({ preventScroll: true });
    done.scrollIntoView({ block: 'start', behavior: 'smooth' });
    block.dispatchEvent(new CustomEvent('request-form:submitted', { bubbles: true, detail: { formId, reference } }));
  });

  block.append(form, done);
}
