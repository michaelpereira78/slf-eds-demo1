import { createOptimizedPicture } from '../../scripts/aem.js';

/**
 * Cards block. One row per card.
 * Variants (word in brackets after the block name):
 *  (Services)  icon (type :invest: etc.), heading, text, optional link
 *  (Steps)     numbered process steps
 *  (Actions)   task tiles for the advisor and supervisor workspaces; the last link is the action
 *  (Capabilities), (Sites), (Templates)  text cards used on the demo pages
 * @param {Element} block The cards block element
 */
export default function decorate(block) {
  const ul = document.createElement('ul');
  [...block.children].forEach((row) => {
    const li = document.createElement('li');
    while (row.firstElementChild) li.append(row.firstElementChild);
    [...li.children].forEach((div) => {
      if (div.children.length === 1 && div.querySelector('picture')) div.className = 'cards-card-image';
      else div.className = 'cards-card-body';
    });
    // an icon on its own line becomes the card's badge;
    // tinted with the theme's colours via CSS mask
    li.querySelectorAll('.cards-card-body > p > span.icon:only-child').forEach((span) => {
      const p = span.parentElement;
      if (p.textContent.trim()) return;
      const img = span.querySelector('img');
      const badge = document.createElement('span');
      badge.className = 'cards-icon';
      badge.setAttribute('aria-hidden', 'true');
      if (img) badge.style.setProperty('--icon', `url("${img.src}")`);
      p.replaceWith(badge);
    });
    // the last link in an action card becomes a button
    if (block.classList.contains('actions')) {
      const links = li.querySelectorAll('.cards-card-body a[href]');
      const last = links[links.length - 1];
      if (last && !last.classList.contains('button')) {
        last.classList.add('button', 'secondary');
        last.closest('p')?.classList.add('button-wrapper');
      }
    }
    ul.append(li);
  });
  ul.querySelectorAll('picture > img').forEach((img) => {
    const src = img.getAttribute('src') || '';
    if (src.includes('media_')) img.closest('picture').replaceWith(createOptimizedPicture(img.src, img.alt, false, [{ width: '750' }]));
  });
  block.replaceChildren(ul);
}
