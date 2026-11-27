/**
 * Small helpers shared by the Sun Life advisor-site blocks
 * (advisor-*, media-text, info-cards).
 */

/** True when an image is marked as a video poster (alt text starts with "Video:"). */
export function isVideoPoster(img) {
  return !!img && /^video\s*:/i.test(img.alt || '');
}

/**
 * Wraps a picture in a poster frame with a round play button.
 * The demo has no video files, so the button only explains that.
 * @param {Element} picture The picture element
 */
export function addPlayButton(picture) {
  const img = picture.querySelector('img');
  const frame = document.createElement('div');
  frame.className = 'video-poster';
  picture.replaceWith(frame);
  frame.append(picture);
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'video-play';
  const label = (img && img.alt.replace(/^video\s*:\s*/i, '')) || 'video';
  button.setAttribute('aria-label', `Play ${label}`);
  button.addEventListener('click', () => {
    if (frame.querySelector('.video-note')) return;
    const note = document.createElement('p');
    note.className = 'video-note';
    note.textContent = 'Demo placeholder: the advisor\u2019s video plays here.';
    frame.append(note);
  });
  frame.append(button);
  return frame;
}

/** Decorates every video poster picture inside an element. */
export function decorateVideoPosters(el) {
  el.querySelectorAll('picture').forEach((pic) => {
    if (isVideoPoster(pic.querySelector('img')) && !pic.closest('.video-poster')) addPlayButton(pic);
  });
}
