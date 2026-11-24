/**
 * Library Metadata block: read by the Sidekick Library (name, description, type).
 * It is authoring information only, so it is removed from the rendered page.
 * @param {Element} block The block element
 */
export default function decorate(block) {
  const section = block.closest('.section');
  block.closest('.library-metadata-wrapper')?.remove();
  if (section && !section.querySelector('.block, .default-content-wrapper > *')) section.remove();
}
