import { takeApproval } from '../../scripts/author.js';

/**
 * Disclosure block: a styled regulatory note.
 * In production this content lives in ONE shared fragment (/fragments/disclosure)
 * owned by Compliance, and every advisor page links to it, so wording changes
 * are made once and picked up everywhere on the next publish.
 * @param {Element} block The disclosure block element
 */
export default function decorate(block) {
  takeApproval(block);
  const badge = block.querySelector('.approval-badge');
  const content = document.createElement('div');
  content.className = 'disclosure-content';
  [...block.querySelectorAll(':scope > div > div')].forEach((cell) => {
    content.append(...cell.childNodes);
  });
  const heading = content.querySelector('h1, h2, h3, h4, h5, h6');
  if (heading) {
    // keep the document outline tidy: the note is always a level-2 heading
    if (heading.tagName !== 'H2') {
      const h2 = document.createElement('h2');
      h2.id = heading.id;
      h2.textContent = heading.textContent;
      heading.replaceWith(h2);
    }
    const h = content.querySelector('h2');
    if (!h.id) h.id = 'disclosure-heading';
    block.setAttribute('aria-labelledby', h.id);
  } else {
    block.setAttribute('aria-label', 'Disclosure');
  }
  block.setAttribute('role', 'note');
  block.replaceChildren(content);
  if (badge) block.append(badge);
}
