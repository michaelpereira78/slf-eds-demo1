import { decorateVideoPosters } from '../../scripts/advisor-ui.js';

/**
 * Info Cards: bordered cards in a three-column grid (Sun Life advisor-site style).
 * Each row is one card: [picture] [heading, text, link]. The picture is optional.
 * Variants: (news) for social posts, keeps line breaks tight;
 * (plain) borderless columns with dividers.
 * A picture whose alt text starts with "Video:" gets a play button.
 * @param {Element} block The block element
 */
export default function decorate(block) {
  const list = document.createElement('ul');
  [...block.children].forEach((row) => {
    const li = document.createElement('li');
    li.className = 'info-card';
    [...row.children].forEach((cell) => {
      if (cell.querySelector('picture') && cell.textContent.trim() === '') {
        cell.className = 'info-card-image';
      } else {
        cell.className = 'info-card-body';
      }
      li.append(cell);
    });
    // lines that continue a list ("You're:" then "- Building a career") sit tight together
    li.querySelectorAll('.info-card-body p').forEach((p) => {
      const prev = p.previousElementSibling;
      const text = p.textContent.trim();
      if (prev && prev.tagName === 'P' && /^[-\u2022]/.test(text)
        && (/:$/.test(prev.textContent.trim()) || /^[-\u2022]/.test(prev.textContent.trim()))) {
        p.classList.add('info-card-line');
      }
      const a = p.querySelector('a');
      if (a && p.textContent.trim() === a.textContent.trim()) p.classList.add('info-card-link');
    });
    list.append(li);
  });
  block.replaceChildren(list);
  decorateVideoPosters(block);
}
