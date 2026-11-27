/**
 * Lead Form: the "Let's connect" contact form of a Sun Life advisor site.
 * The block holds only the heading and intro text; the fields are built here.
 * Demo mode: nothing is sent anywhere. Submitting validates the fields and shows a confirmation.
 * @param {Element} block The block element
 */
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'class') node.className = v;
    else if (k === 'text') node.textContent = v;
    else node.setAttribute(k, v);
  });
  children.flat().forEach((c) => c && node.append(c));
  return node;
}

function field(id, label, { type = 'text', optional = false, icon = '' } = {}) {
  const input = type === 'textarea'
    ? el('textarea', {
      id, name: id, placeholder: ' ', maxlength: '500', rows: '6',
    })
    : el('input', {
      id, name: id, type, placeholder: ' ', autocomplete: { email: 'email', tel: 'tel' }[type] || 'on',
    });
  if (!optional) input.required = true;
  const wrap = el(
    'div',
    { class: `lead-form-field${icon ? ` has-icon icon-${icon}` : ''}${type === 'textarea' ? ' is-textarea' : ''}` },
    input,
    el('label', { for: id, text: label }),
  );
  if (type === 'textarea') {
    const count = el('span', { class: 'lead-form-count', text: '0 of 500' });
    input.addEventListener('input', () => { count.textContent = `${input.value.length} of 500`; });
    wrap.append(count);
  }
  const group = el('div', { class: 'lead-form-group' }, wrap);
  if (optional) group.append(el('p', { class: 'lead-form-optional', text: 'Optional' }));
  group.append(el('p', { class: 'lead-form-error', id: `${id}-error`, 'aria-live': 'polite' }));
  return group;
}

export default function decorate(block) {
  const intro = el('div', { class: 'lead-form-intro' });
  block.querySelectorAll(':scope > div > div').forEach((cell) => intro.append(...cell.childNodes));
  const heading = intro.querySelector('h2, h3');
  if (heading) heading.id = 'lets-connect';

  const methods = el(
    'fieldset',
    { class: 'lead-form-radios' },
    el('legend', { text: 'Preferred Contact Method' }),
    ...['Email', 'Phone'].map((m, i) => el(
      'label',
      { class: 'lead-form-radio' },
      el('input', {
        type: 'radio', name: 'method', value: m.toLowerCase(), ...(i === 0 ? { checked: '' } : {}),
      }),
      el('span', { text: m }),
    )),
  );

  const email = field('lf-email', 'Email Address', { type: 'email', icon: 'mail' });
  const phone = field('lf-phone', 'Phone Number', { type: 'tel', optional: true, icon: 'phone' });
  const consent = el(
    'label',
    { class: 'lead-form-check' },
    el('input', { type: 'checkbox', name: 'consent' }),
    el('span', { text: 'Yes I\u2019d like to receive emails from Sunlife and this advisor. I understand I can unsubscribe at any time.' }),
  );
  const privacy = el('a', { href: 'https://www.sunlife.ca/privacy', text: 'privacy' });
  const disclaimer = el(
    'p',
    { class: 'lead-form-disclaimer' },
    'By providing your contact information you agree to send your information to Sunlife Canada who agrees to use it '
      + 'according to their privacy policy and that Sunlife can contact you from time to time by phone, email, text and '
      + 'regular mail. You can unsubscribe at any time. To find out more about our privacy practices, visit ',
    privacy,
    '.',
  );
  const status = el('div', { class: 'lead-form-status', role: 'status' });
  const form = el(
    'form',
    { novalidate: '' },
    el('div', { class: 'lead-form-row' }, field('lf-first', 'First Name')),
    el('div', { class: 'lead-form-row' }, field('lf-last', 'Last Name')),
    methods,
    email,
    phone,
    field('lf-message', 'Message', { type: 'textarea', optional: true }),
    consent,
    disclaimer,
    el('button', { type: 'submit', class: 'lead-form-submit', text: 'Submit' }),
    status,
  );

  // email is required only when it is the preferred contact method (phone likewise)
  const sync = () => {
    const method = form.method.value;
    form.querySelector('#lf-email').required = method === 'email';
    form.querySelector('#lf-phone').required = method === 'phone';
    email.querySelector('.lead-form-optional')?.remove();
    phone.querySelector('.lead-form-optional')?.remove();
    const optionalGroup = method === 'email' ? phone : email;
    optionalGroup.querySelector('.lead-form-field').after(el('p', { class: 'lead-form-optional', text: 'Optional' }));
  };
  form.querySelectorAll('input[name="method"]').forEach((r) => r.addEventListener('change', sync));

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let firstInvalid = null;
    form.querySelectorAll('input:not([type=radio]):not([type=checkbox]), textarea').forEach((input) => {
      const err = form.querySelector(`#${input.id}-error`);
      const ok = input.checkValidity();
      input.setAttribute('aria-invalid', ok ? 'false' : 'true');
      if (err) err.textContent = ok ? '' : `Please enter a valid ${input.labels[0].textContent.toLowerCase()}.`;
      if (!ok && !firstInvalid) firstInvalid = input;
    });
    if (firstInvalid) {
      firstInvalid.focus();
      return;
    }
    const first = form.querySelector('#lf-first').value.trim();
    status.textContent = `Thanks, ${first}. This is a demo form, so nothing was sent. On a live site, Michael's office would reply within one business day.`;
    status.classList.add('is-visible');
    form.reset();
    sync();
  });

  block.replaceChildren(intro, form);
  sync();
}
