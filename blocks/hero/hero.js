import { createOptimizedPicture } from '../../scripts/aem.js';

/**
 * Hero block.
 * Default: a single cell with an optional eyebrow paragraph, an H1, intro text and CTAs.
 * Photo background: put a picture in its own row (above or below the text row). The photo
 *   fills the band behind the text with a brand-coloured overlay.
 * (Profile) layout: an image cell next to a text cell in the same row, side by side.
 * @param {Element} block The hero block element
 */
export default function decorate(block) {
  const rows = [...block.children];
  // a row that holds nothing but a picture becomes the background photo
  const photoRow = rows.find((row) => row.querySelector('picture') && row.textContent.trim() === ''
    && row.children.length === 1 && rows.length > 1);
  if (photoRow) {
    const img = photoRow.querySelector('img');
    const bg = document.createElement('div');
    bg.className = 'hero-bg';
    const src = img.getAttribute('src') || '';
    const pic = src.includes('media_')
      ? createOptimizedPicture(img.src, img.alt || '', true, [{ media: '(min-width: 900px)', width: '2000' }, { width: '900' }])
      : photoRow.querySelector('picture');
    const bgImg = pic.querySelector('img');
    bgImg.loading = 'eager';
    bgImg.fetchPriority = 'high';
    bgImg.alt = img.alt || '';
    bg.append(pic);
    photoRow.remove();
    block.prepend(bg);
    block.classList.add('hero-photo');
  }

  const cells = [...block.querySelectorAll(':scope > div:not(.hero-bg) > div')];
  cells.forEach((cell) => {
    const pic = cell.querySelector('picture');
    if (pic && cell.textContent.trim() === '') {
      cell.classList.add('hero-media');
      const img = pic.querySelector('img');
      if (img) {
        // the hero image is the LCP candidate: load it eagerly
        img.loading = 'eager';
        img.fetchPriority = 'high';
      }
    } else {
      cell.classList.add('hero-content');
      // a short paragraph before the H1 becomes the eyebrow
      const h1 = cell.querySelector('h1, h2');
      const prev = h1 && h1.previousElementSibling;
      if (prev && prev.tagName === 'P' && !prev.querySelector('a')) prev.classList.add('hero-eyebrow');
      // group consecutive button paragraphs into one action row
      const buttons = [...cell.querySelectorAll(':scope > p.button-wrapper')];
      if (buttons.length) {
        const actions = document.createElement('div');
        actions.className = 'hero-actions';
        buttons[0].before(actions);
        actions.append(...buttons);
      }
    }
  });
  if (block.querySelector('.hero-media')) block.classList.add('hero-has-media');
}
