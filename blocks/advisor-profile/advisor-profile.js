const ICONS = {
  facebook: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12"/><path d="M13.4 24v-8.6h2.9l.4-3.4h-3.3V9.9c0-1 .3-1.6 1.7-1.6h1.8V5.2a24 24 0 0 0-2.6-.1c-2.6 0-4.3 1.6-4.3 4.4V12H7.1v3.4H10V24z" fill="#fff"/></svg>',
  instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1.5" y="1.5" width="21" height="21" rx="6" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="12" cy="12" r="4.8" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="18" cy="6" r="1.5"/></svg>',
  linkedin: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="2"/><path d="M5 9.5h3V19H5zM6.5 5a1.7 1.7 0 1 1 0 3.5 1.7 1.7 0 0 1 0-3.5zM10.2 9.5H13v1.3c.4-.8 1.4-1.6 2.9-1.6 3.1 0 3.6 2 3.6 4.6V19h-3v-4.6c0-1.1 0-2.5-1.5-2.5s-1.8 1.2-1.8 2.4V19h-3z" fill="#fff"/></svg>',
};

/**
 * Advisor Profile: round headshot beside name, title, details, a booking link and social icons.
 * One row, two cells: [picture] [h2 name, paragraphs, link, bullet list of social links].
 * @param {Element} block The block element
 */
export default function decorate(block) {
  const cells = [...block.querySelectorAll(':scope > div > div')];
  cells.forEach((cell) => {
    if (cell.querySelector('picture') && cell.textContent.trim() === '') {
      cell.classList.add('advisor-profile-photo');
    } else {
      cell.classList.add('advisor-profile-details');
    }
  });

  block.querySelectorAll('.advisor-profile-details ul').forEach((ul) => {
    ul.classList.add('advisor-profile-social');
    ul.querySelectorAll('a').forEach((a) => {
      const host = a.hostname.replace(/^www\./, '').split('.')[0];
      const svg = ICONS[host];
      if (!svg) return;
      a.setAttribute('aria-label', a.textContent.trim());
      a.title = a.textContent.trim();
      a.innerHTML = svg;
      a.target = '_blank';
      a.rel = 'noopener';
    });
  });
}
