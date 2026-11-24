/**
 * Hero block.
 * Default: a single cell with an optional eyebrow paragraph, an H1, intro text and CTAs.
 * (Profile) variant: an image cell plus a text cell, rendered side by side on larger screens.
 * @param {Element} block The hero block element
 */
export default function decorate(block) {
  const cells = [...block.querySelectorAll(':scope > div > div')];
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
      const h1 = cell.querySelector('h1');
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
