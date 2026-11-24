import { takeApproval } from '../../scripts/author.js';

/**
 * Callout block: a highlighted box. Approved-content fragments use it.
 * Optional last row "Approved | AC-2026-031 ..." is shown as a badge on preview only.
 * (CTA) variant: brand-colour call to action band.
 * @param {Element} block The callout block element
 */
export default function decorate(block) {
  const badgeText = takeApproval(block);
  const content = document.createElement('div');
  content.className = 'callout-content';
  [...block.querySelectorAll(':scope > div > div')].forEach((cell) => content.append(...cell.childNodes));
  [...block.children].filter((c) => c.tagName === 'DIV').forEach((c) => c.remove());
  block.prepend(content);
  if (badgeText) block.classList.add('callout-approved');
}
