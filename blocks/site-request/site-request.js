/**
 * Site Request block: the "new advisor site" intake form.
 * Picking a theme re-themes this page live. Submitting produces a request summary and the
 * exact generator command the platform team runs (tools/new-site/new-site.py).
 * No data leaves the page.
 */
const THEMES = [
  ['forest', 'Forest', 'Green and coral', ['#1e4d3b', '#f9a66c']],
  ['harbour', 'Harbour', 'Indigo and teal', ['#1f2a5c', '#5fd3c1']],
  ['slate', 'Slate', 'Charcoal and amber, serif headings', ['#2b2f36', '#f2b134']],
];
const TEMPLATES = [
  ['advisor-team', 'Advisor team', 'Two or more advisors'],
  ['solo-advisor', 'Solo advisor', 'One advisor practice'],
  ['campaign', 'Campaign', 'Single landing page'],
];

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

function field(id, label, attrs = {}) {
  return el(
    'div',
    { class: 'sr-field' },
    el('label', { for: id, text: label }),
    el('input', {
      id, name: id, required: '', ...attrs,
    }),
  );
}

function choice(name, value, title, desc, checked, swatches) {
  const id = `${name}-${value}`;
  const input = el('input', {
    type: 'radio', id, name, value,
  });
  if (checked) input.checked = true;
  return el(
    'div',
    { class: 'sr-choice' },
    input,
    el(
      'label',
      { for: id },
      swatches ? el(
        'span',
        { class: 'sr-swatches', 'aria-hidden': 'true' },
        ...swatches.map((c) => el('span', { style: `background-color:${c}` })),
      ) : null,
      el('strong', { text: title }),
      el('span', { class: 'sr-desc', text: desc }),
    ),
  );
}

const slug = (s) => s.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

export default function decorate(block) {
  const form = el(
    'form',
    { class: 'sr-form', novalidate: '' },
    el(
      'div',
      { class: 'sr-grid' },
      field('firm', '1. Firm or practice name', { placeholder: 'e.g. Prairie Sky Financial', autocomplete: 'organization' }),
      field('city', '2. City and province', { placeholder: 'e.g. Regina, SK' }),
      field('lead', '3. Lead advisor', { placeholder: 'e.g. Sam Rivera, CFP', autocomplete: 'name' }),
    ),
    el(
      'fieldset',
      { class: 'sr-themes' },
      el('legend', { text: '4. Brand theme (this page changes to match)' }),
      ...THEMES.map(([v, t, d, sw], i) => choice('theme', v, t, d, i === 0, sw)),
    ),
    el(
      'fieldset',
      { class: 'sr-templates' },
      el('legend', { text: '5. Approved template' }),
      ...TEMPLATES.map(([v, t, d], i) => choice('template', v, t, d, i === 0)),
    ),
    el('p', { class: 'button-wrapper' }, el('button', { type: 'submit', class: 'button primary', text: 'Create site request' })),
  );

  const result = el('div', {
    class: 'sr-result', hidden: '', tabindex: '-1', 'aria-live': 'polite',
  });

  const applyTheme = (theme) => {
    THEMES.forEach(([v]) => document.body.classList.remove(v));
    document.body.classList.add(theme);
  };
  form.addEventListener('change', (e) => {
    if (e.target.name === 'theme') applyTheme(e.target.value);
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const missing = [...form.querySelectorAll('input[required]')].find((i) => !i.value.trim());
    if (missing) {
      missing.setAttribute('aria-invalid', 'true');
      missing.focus();
      return;
    }
    const data = Object.fromEntries(new FormData(form).entries());
    const site = slug(data.firm).slice(0, 40);
    const id = `REQ-${Date.now().toString().slice(-5)}`;
    const cmd = `python3 tools/new-site/new-site.py --firm "${data.firm}" --city "${data.city}" --lead "${data.lead}" --theme ${data.theme} --template ${data.template}`;
    const copy = el('button', { type: 'button', class: 'button secondary', text: 'Copy command' });
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(cmd);
        copy.textContent = 'Copied';
      } catch (err) {
        copy.textContent = 'Select and copy the text above';
      }
    });
    const theme = THEMES.find(([v]) => v === data.theme)[1];
    const template = TEMPLATES.find(([v]) => v === data.template)[1];
    result.replaceChildren(
      el('h2', { text: `Request ${id} is ready` }),
      el(
        'dl',
        {},
        el('dt', { text: 'Site' }),
        el('dd', { text: `${data.firm}, ${data.city}` }),
        el('dt', { text: 'Lead advisor' }),
        el('dd', { text: data.lead }),
        el('dt', { text: 'Theme and template' }),
        el('dd', { text: `${theme} theme, ${template} template` }),
        el('dt', { text: 'Preview address' }),
        el('dd', { text: `https://main--${site}--<org>.aem.page/` }),
      ),
      el('h3', { text: 'What the platform team runs' }),
      el('pre', {}, el('code', { text: cmd })),
      el('p', { class: 'button-wrapper' }, copy),
      el('p', { text: 'The generator writes the starter documents (home page, navigation, footer) already set to this theme and template, plus the one admin call that creates the site. Creating the site needs a platform administrator; everything after that is done by the advisor in Word or Google Docs.' }),
    );
    result.hidden = false;
    result.focus();
  });

  // deep links from the supervisor console: /new-site?template=solo-advisor&theme=slate
  const params = new URLSearchParams(window.location.search);
  ['template', 'theme'].forEach((name) => {
    const value = params.get(name);
    const input = value && form.querySelector(`input[name="${name}"][value="${CSS.escape(value)}"]`);
    if (input) {
      input.checked = true;
      if (name === 'theme') applyTheme(value);
    }
  });

  block.replaceChildren(form, result);
}
