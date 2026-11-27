import { decorateVideoPosters } from '../../scripts/advisor-ui.js';

/**
 * Media Text: a picture (or video poster) beside text, in two equal columns.
 * Each row is one pair: [picture] [text]. A row with only a picture keeps its column.
 * Variants: (right) puts the media on the right; (video) shows a play button on the picture
 * (also automatic when the picture's alt text starts with "Video:").
 * @param {Element} block The block element
 */
export default function decorate(block) {
  const forceVideo = block.classList.contains('video');
  [...block.children].forEach((row) => {
    row.classList.add('media-text-row');
    [...row.children].forEach((cell) => {
      const pic = cell.querySelector('picture');
      if (pic && cell.textContent.trim() === '') {
        cell.classList.add('media-text-media');
        if (forceVideo) {
          const img = pic.querySelector('img');
          if (img && !/^video\s*:/i.test(img.alt)) img.alt = `Video: ${img.alt}`;
        }
      } else if (cell.textContent.trim() === '' && !cell.querySelector('img')) {
        cell.remove();
      } else {
        cell.classList.add('media-text-text');
      }
    });
    if (!row.querySelector('.media-text-text')) row.classList.add('media-only');
  });
  decorateVideoPosters(block);
}
