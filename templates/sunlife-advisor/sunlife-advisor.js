/**
 * Sun Life advisor template (internal demo replica of the advisor.sunlife.ca layout).
 * - Swaps the text brand in the nav for the Sun Life logo (hotlinked public asset, text fallback).
 * - Highlights only the current page in the nav (Home is not highlighted on subpages).
 * - Adds the CIPF and CIRO regulator logos to the footer.
 * - Marks links: arrow-in-circle for links to other pages, box-arrow for external links.
 */
const ASSETS = 'https://advisor.sunlife.ca/sites/default/files';
const LOGO = `${ASSETS}/2026-11/Logo_Sunlife_RGB.svg`;
const REGULATORS = [
  { href: 'https://www.cipf.ca/', src: `${ASSETS}/2025-06/cipf-en.jpg`, alt: 'Canadian Investor Protection Fund (CIPF)' },
  { href: 'https://www.ciro.ca/', src: `${ASSETS}/2025-06/ciro-en.jpg`, alt: 'Regulated by Canadian Investment Regulatory Organization (CIRO)' },
];

function isExternal(a) {
  try {
    const url = new URL(a.href, window.location);
    return /^https?:$/.test(url.protocol) && url.origin !== window.location.origin;
  } catch (e) {
    return false;
  }
}

function markLinks(root) {
  root.querySelectorAll('a[href]').forEach((a) => {
    if (a.classList.contains('button') || a.querySelector('img, svg') || a.closest('.advisor-profile ul')) return;
    const p = a.closest('p, li');
    const standalone = p && p.textContent.trim() === a.textContent.trim();
    if (isExternal(a)) {
      if ((standalone && !a.closest('.footer')) || a.closest('.nav-tools')) a.classList.add('sl-external');
      a.target = '_blank';
      a.rel = 'noopener';
    } else if (standalone && !a.closest('nav, .footer') && !a.href.startsWith('tel:') && !a.href.startsWith('mailto:')) {
      a.classList.add('sl-more');
    }
  });
}

function decorateHeader(header) {
  const brand = header.querySelector('.nav-brand a');
  if (brand && !brand.querySelector('img')) {
    const img = document.createElement('img');
    img.src = LOGO;
    img.alt = 'Sunlife';
    img.width = 132;
    img.height = 32;
    img.addEventListener('error', () => img.replaceWith('Sunlife'));
    brand.replaceChildren(img);
  }
  // "my Sunlife" with an italic "my", as on the original
  header.querySelectorAll('.nav-tools a').forEach((a) => {
    const m = a.textContent.match(/^my (.*)$/);
    if (m && !a.querySelector('em')) {
      const em = document.createElement('em');
      em.textContent = 'my';
      a.replaceChildren(em, ` ${m[1]}`);
    }
  });
  const here = window.location.pathname.replace(/\/$/, '');
  header.querySelectorAll('.nav-sections a[href]').forEach((a) => {
    const path = new URL(a.href, window.location).pathname.replace(/\/$/, '');
    if (path === here) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });
  markLinks(header);
}

function decorateFooter(footer) {
  const inner = footer.querySelector('.footer > div');
  if (!inner || inner.querySelector('.sl-footer-logos')) return;
  const logos = document.createElement('div');
  logos.className = 'sl-footer-logos';
  REGULATORS.forEach(({ href, src, alt }) => {
    const a = document.createElement('a');
    a.href = href;
    a.target = '_blank';
    a.rel = 'noopener';
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    img.loading = 'lazy';
    img.addEventListener('error', () => a.remove());
    a.append(img);
    logos.append(a);
  });
  inner.prepend(logos);
  markLinks(footer);
}

/** Runs fn once the header/footer block has finished loading (they load after the template). */
function whenLoaded(selector, fn) {
  const run = () => {
    const block = document.querySelector(selector);
    if (block && block.dataset.blockStatus === 'loaded') {
      fn(block.closest('header, footer'));
      return true;
    }
    return false;
  };
  if (run()) return;
  const observer = new MutationObserver(() => {
    if (run()) observer.disconnect();
  });
  observer.observe(document.body, { subtree: true, attributes: true, attributeFilter: ['data-block-status'] });
}

export default function decorate(main) {
  markLinks(main);
  // blocks rebuild their markup when they load, so mark their links again afterwards
  new MutationObserver((records) => {
    records.forEach((r) => {
      if (r.target.dataset && r.target.dataset.blockStatus === 'loaded') markLinks(r.target);
    });
  }).observe(main, { subtree: true, attributes: true, attributeFilter: ['data-block-status'] });
  whenLoaded('header .header', decorateHeader);
  whenLoaded('footer .footer', decorateFooter);
}
