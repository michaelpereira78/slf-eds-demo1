/**
 * Office Map: an embedded Google map beside the office details.
 * One row, two cells: [place to show on the map, e.g. "Cambridge, Ontario"] [office details].
 * The map uses Google's keyless embed URL (the block itself loads after the first section).
 * @param {Element} block The block element
 */
export default function decorate(block) {
  const [queryCell, details] = [...block.querySelectorAll(':scope > div > div')];
  if (!queryCell) return;
  const query = queryCell.textContent.trim();
  const map = document.createElement('div');
  map.className = 'office-map-map';
  if (query) {
    const iframe = document.createElement('iframe');
    iframe.src = `https://maps.google.com/maps?q=${encodeURIComponent(query)}&z=14&output=embed`;
    iframe.title = `Map of ${query}`;
    iframe.referrerPolicy = 'no-referrer-when-downgrade';
    map.append(iframe);
  }
  const info = document.createElement('div');
  info.className = 'office-map-details';
  if (details) {
    info.append(...details.childNodes);
    // a bold label ("Phone:") on its own line belongs to the line after it
    info.querySelectorAll('p').forEach((p) => {
      const strong = p.querySelector('strong');
      if (strong && p.textContent.trim() === strong.textContent.trim()) p.classList.add('office-map-label');
    });
  }
  block.replaceChildren(map, info);
}
