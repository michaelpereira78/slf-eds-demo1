/**
 * Advisor Banner: a full-width photo with a cream text panel on the left
 * (Sun Life advisor-site style).
 * One row, two cells: [picture] [heading, text, button]. Cell order does not matter.
 * Without a button the banner is shorter (400px instead of 520px on desktop).
 * @param {Element} block The block element
 */
export default function decorate(block) {
  const cells = [...block.querySelectorAll(':scope > div > div')];
  const mediaCell = cells.find((c) => c.querySelector('picture') && c.textContent.trim() === '');
  const textCells = cells.filter((c) => c !== mediaCell);

  const media = document.createElement('div');
  media.className = 'advisor-banner-media';
  if (mediaCell) {
    const img = mediaCell.querySelector('img');
    if (img) {
      img.loading = 'eager';
      img.fetchPriority = 'high';
    }
    media.append(...mediaCell.childNodes);
  }

  const inner = document.createElement('div');
  inner.className = 'advisor-banner-inner';
  const panel = document.createElement('div');
  panel.className = 'advisor-banner-panel';
  textCells.forEach((c) => panel.append(...c.childNodes));
  inner.append(panel);
  // without a button the banner is shorter, as on the original's subpages
  if (!panel.querySelector('a')) block.classList.add('no-cta');

  block.replaceChildren(media, inner);
}
