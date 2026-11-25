/**
 * Banner block: a full-width call-to-action band with a background photo.
 * Rows: a picture (own row) and a text row (heading, sentence, one or two button links).
 * Without a picture it renders as a solid brand-colour band.
 * @param {Element} block The banner block element
 */
export default function decorate(block) {
  const rows = [...block.children];
  const photoRow = rows.find((r) => r.querySelector('picture') && !r.textContent.trim());
  if (photoRow) {
    const bg = document.createElement('div');
    bg.className = 'banner-bg';
    bg.append(photoRow.querySelector('picture'));
    photoRow.remove();
    block.prepend(bg);
    block.classList.add('banner-photo');
  }
  const content = block.querySelector(':scope > div:not(.banner-bg)');
  if (content) {
    content.className = 'banner-content';
    const buttons = [...content.querySelectorAll('p.button-wrapper')];
    if (buttons.length) {
      const actions = document.createElement('div');
      actions.className = 'banner-actions';
      buttons[0].before(actions);
      actions.append(...buttons);
    }
  }
}
