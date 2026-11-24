const ICONS = {
  office: '<path d="M12 2a7 7 0 0 1 7 7c0 5.2-7 13-7 13S5 14.2 5 9a7 7 0 0 1 7-7Zm0 4.5A2.5 2.5 0 1 0 12 11.5 2.5 2.5 0 0 0 12 6.5Z"/>',
  phone: '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1l-2.2 2.2Z"/>',
  email: '<path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm1 2.4V17h16V7.4l-8 5.3-8-5.3ZM5.8 7l6.2 4.1L18.2 7H5.8Z"/>',
  hours: '<path d="M12 2a10 10 0 1 1 0 20 10 10 0 0 1 0-20Zm0 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16Zm1 3v4.6l3.2 1.9-1 1.7L11 12.7V7h2Z"/>',
};

function iconFor(label) {
  const l = label.toLowerCase();
  if (/(office|address|location|visit)/.test(l)) return 'office';
  if (/(phone|line|call|tel)/.test(l)) return 'phone';
  if (/(email|e-mail|mail)/.test(l)) return 'email';
  if (/(hour|open)/.test(l)) return 'hours';
  return null;
}

/**
 * Contact block. Authored as two-column rows: label | value.
 * Phone and email values are turned into tel:/mailto: links automatically.
 * A row whose value is a link (e.g. "Get directions") becomes a button.
 * Variant (Card) renders a compact sidebar card.
 * @param {Element} block The contact block element
 */
export default function decorate(block) {
  const dl = document.createElement('dl');
  const actions = document.createElement('div');
  actions.className = 'contact-actions';

  [...block.children].forEach((row) => {
    const [labelCell, valueCell] = row.children;
    if (!labelCell) return;
    const label = labelCell.textContent.trim();
    const valueEl = valueCell || labelCell;
    const value = valueEl.textContent.trim();
    const link = valueEl.querySelector('a[href]');

    // link-only rows (e.g. Directions) become buttons
    if (link && value === link.textContent.trim() && !/^(mailto|tel):/.test(link.getAttribute('href'))) {
      link.className = 'button secondary';
      if (/^https?:/.test(link.href) && new URL(link.href).origin !== window.location.origin) {
        link.target = '_blank';
        link.rel = 'noopener';
        link.setAttribute('aria-label', `${link.textContent.trim()} (opens in a new tab)`);
      }
      actions.append(link);
      return;
    }

    const item = document.createElement('div');
    item.className = 'contact-item';
    const icon = iconFor(label);
    const dt = document.createElement('dt');
    if (icon) {
      dt.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">${ICONS[icon]}</svg>`;
    }
    const span = document.createElement('span');
    span.textContent = label;
    dt.append(span);

    const dd = document.createElement('dd');
    if (!link && icon === 'phone' && /\d{3}.*\d{4}/.test(value)) {
      const a = document.createElement('a');
      a.href = `tel:${value.replace(/[^\d+]/g, '')}`;
      a.textContent = value;
      dd.append(a);
    } else if (!link && icon === 'email' && value.includes('@')) {
      const a = document.createElement('a');
      a.href = `mailto:${value}`;
      a.textContent = value;
      dd.append(a);
    } else {
      dd.append(...valueEl.childNodes);
    }
    item.append(dt, dd);
    dl.append(item);
  });

  block.replaceChildren(dl);
  if (block.classList.contains('card')) {
    const h = document.createElement('h2');
    h.className = 'contact-heading';
    h.textContent = 'Get in touch';
    block.prepend(h);
  }
  if (actions.children.length) block.append(actions);
}
