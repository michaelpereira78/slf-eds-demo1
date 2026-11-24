/**
 * Template: Campaign.
 * Copies the hero's primary button into a sticky bar that slides up on phones
 * once the hero has scrolled out of view.
 * @param {Element} main the main element
 */
export default function decorate(main) {
  const primary = main.querySelector('.hero a.button.primary');
  if (!primary) return;
  const bar = document.createElement('div');
  bar.className = 'campaign-sticky-cta';
  const a = primary.cloneNode(true);
  a.tabIndex = -1;
  bar.append(a);
  document.body.append(bar);
  const hero = main.querySelector('.hero');
  const io = new IntersectionObserver(([entry]) => {
    const show = !entry.isIntersecting;
    bar.classList.toggle('visible', show);
    a.tabIndex = show ? 0 : -1;
  });
  io.observe(hero);
}
