/**
 * CTA Box: a cream call-to-action panel with a picture beside a heading, text and link.
 * One row, two cells: [picture] [heading, text, link].
 * @param {Element} block The block element
 */
export default function decorate(block) {
  block.querySelectorAll(':scope > div > div').forEach((cell) => {
    cell.className = cell.querySelector('picture') && cell.textContent.trim() === ''
      ? 'cta-box-media' : 'cta-box-text';
  });
}
