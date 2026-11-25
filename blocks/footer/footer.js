import { getMetadata } from '../../scripts/aem.js';
import { loadFragment } from '../fragment/fragment.js';

/**
 * loads and decorates the footer
 * @param {Element} block The footer block element
 */
export default async function decorate(block) {
  // load footer as fragment
  const footerMeta = getMetadata('footer');
  const footerPath = footerMeta ? new URL(footerMeta, window.location).pathname : '/footer';
  const fragment = await loadFragment(footerPath);

  // decorate footer DOM
  block.textContent = '';
  const footer = document.createElement('div');
  while (fragment.firstElementChild) footer.append(fragment.firstElementChild);

  // name the footer sections: first = brand, last = legal (demo banner),
  // anything between = link columns
  const sections = [...footer.children];
  sections.forEach((section, i) => {
    if (i === 0) section.classList.add('footer-brand');
    else if (i === sections.length - 1 && sections.length > 2) section.classList.add('footer-legal');
    else section.classList.add('footer-links', 'footer-col');
  });
  footer.style.setProperty('--footer-cols', Math.max(1, sections.length - 2));

  block.append(footer);
}
