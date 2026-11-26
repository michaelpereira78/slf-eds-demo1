/**
 * Workspace template: modal forms and current-nav highlighting for subpages.
 * Links to a workspace page with ?modal (e.g. /advisor/submit-review?modal) open
 * in a dialog. Without JavaScript they are ordinary pages.
 */
// eslint-disable-next-line import/no-cycle
import { decorateMain } from '../../scripts/scripts.js';
import { loadSections } from '../../scripts/aem.js';

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'class') node.className = v;
    else if (k === 'text') node.textContent = v;
    else node.setAttribute(k, v);
  });
  children.flat().forEach((c) => c && node.append(c));
  return node;
}

/** Load a page as a fragment, dropping its Metadata block so it is not loaded as a component. */
async function loadModalFragment(path) {
  const resp = await fetch(`${path}.plain.html`);
  if (!resp.ok) return null;
  const main = document.createElement('main');
  main.innerHTML = await resp.text();
  main.querySelectorAll('.metadata').forEach((block) => {
    const wrap = block.parentElement;
    block.remove();
    if (wrap && !wrap.children.length) wrap.remove();
  });
  decorateMain(main);
  await loadSections(main);
  return main;
}

function isModalLink(anchor) {
  if (!anchor || anchor.target === '_blank') return false;
  try {
    const url = new URL(anchor.href, window.location);
    return url.origin === window.location.origin && url.searchParams.has('modal');
  } catch (e) {
    return false;
  }
}

function markCurrentNav() {
  const nav = document.getElementById('nav');
  if (!nav) return;
  const here = (window.location.pathname.replace(/\/$/, '') || '/');
  nav.querySelectorAll('.nav-sections a[href]').forEach((a) => {
    const url = new URL(a.href, window.location);
    const path = url.pathname.replace(/\/$/, '') || '/';
    a.removeAttribute('aria-current');
    if (here === path) {
      a.setAttribute('aria-current', 'page');
      return;
    }
    // highlight a parent item for nested pages, but never the workspace home itself
    const isHome = path === '/advisor' || path === '/admin' || path === '/';
    if (!isHome && here.startsWith(`${path}/`)) a.setAttribute('aria-current', 'page');
  });
}

async function openModal(href) {
  const url = new URL(href, window.location);
  url.searchParams.delete('modal');
  const path = url.pathname;

  const close = el('button', {
    type: 'button', class: 'workspace-dialog-close', 'aria-label': 'Close', text: '×',
  });
  const body = el('div', { class: 'workspace-dialog-body' });
  const panel = el('div', { class: 'workspace-dialog-panel', role: 'document' }, el('div', { class: 'workspace-dialog-head' }, close), body);
  const dialog = el('dialog', { class: 'workspace-dialog', 'aria-modal': 'true' }, panel);
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => dialog.remove());
  document.body.append(dialog);
  dialog.showModal();
  close.focus();

  try {
    const fragment = await loadModalFragment(path);
    if (!fragment) throw new Error('empty');
    const hero = fragment.querySelector('.hero-container');
    const heading = hero && hero.querySelector('h1, h2');
    const intro = hero
      ? [...hero.querySelectorAll('.hero-content > p:not(.hero-eyebrow)')]
        .filter((p) => !p.classList.contains('button-wrapper') && !p.querySelector('a.button'))
      : [];
    if (hero) hero.remove();
    body.replaceChildren(...fragment.children);
    if (heading) {
      heading.id = heading.id || 'workspace-dialog-title';
      dialog.setAttribute('aria-labelledby', heading.id);
      const head = dialog.querySelector('.workspace-dialog-head');
      head.prepend(heading);
    }
    if (intro.length) body.prepend(...intro);
    const first = body.querySelector('input, select, textarea, button');
    if (first) first.focus();
  } catch (e) {
    body.replaceChildren(
      el(
        'p',
        { class: 'workspace-dialog-error' },
        el('span', { text: 'This form could not be opened here. ' }),
        el('a', { href: path, text: 'Open it as a page' }),
        el('span', { text: '.' }),
      ),
    );
  }
}

export default function decorate() {
  markCurrentNav();
  // header is loaded in parallel; mark again once it is in the page
  const header = document.querySelector('body > header');
  if (header && !header.querySelector('nav')) {
    const watch = new MutationObserver(() => {
      if (header.querySelector('nav')) {
        markCurrentNav();
        watch.disconnect();
      }
    });
    watch.observe(header, { childList: true, subtree: true });
  }

  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!isModalLink(a)) return;
    e.preventDefault();
    openModal(a.href);
  });
}
