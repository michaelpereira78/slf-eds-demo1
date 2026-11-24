import { createOptimizedPicture } from '../../scripts/aem.js';

const ICONS = {
  email: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm1 2.4V17h16V7.4l-8 5.3-8-5.3ZM5.8 7l6.2 4.1L18.2 7H5.8Z"/></svg>',
  phone: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1l-2.2 2.2Z"/></svg>',
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^\+?[\d\s().-]{7,}$/;

function contactLink(type, value, person) {
  const a = document.createElement('a');
  a.className = `team-cards-${type}`;
  a.href = type === 'email' ? `mailto:${value}` : `tel:${value.replace(/[^\d+]/g, '')}`;
  a.setAttribute('aria-label', `${type === 'email' ? 'Email' : 'Call'} ${person}: ${value}`);
  a.innerHTML = ICONS[type];
  const span = document.createElement('span');
  span.textContent = value;
  a.append(span);
  return a;
}

/**
 * Team Cards block.
 * One authored row per person: image | name, credentials | title | bio | email | phone.
 * Cells are detected defensively, so authors can skip or reorder the contact cells.
 * @param {Element} block The team-cards block element
 */
export default function decorate(block) {
  const ul = document.createElement('ul');
  ul.setAttribute('role', 'list');

  [...block.children].forEach((row) => {
    const li = document.createElement('li');
    li.className = 'team-cards-card';
    const body = document.createElement('div');
    body.className = 'team-cards-body';
    const contacts = document.createElement('div');
    contacts.className = 'team-cards-contacts';

    let picture;
    let nameText = '';
    let profileHref;
    const textCells = [];

    [...row.children].forEach((cell) => {
      const pic = cell.querySelector('picture');
      if (pic && !picture) {
        picture = pic;
        return;
      }
      const text = cell.textContent.trim();
      if (!text) return;
      if (!nameText) {
        nameText = text;
        const link = cell.querySelector('a[href]');
        if (link) profileHref = link.getAttribute('href');
        return;
      }
      const mail = cell.querySelector('a[href^="mailto:"]');
      if (mail || EMAIL_RE.test(text)) {
        textCells.push({ type: 'email', value: mail ? mail.href.replace('mailto:', '') : text });
      } else if (PHONE_RE.test(text)) {
        textCells.push({ type: 'phone', value: text });
      } else {
        textCells.push({ type: 'text', cell });
      }
    });

    const [name, ...creds] = nameText.split(',').map((s) => s.trim());

    if (picture) {
      const img = picture.querySelector('img');
      const media = document.createElement('div');
      media.className = 'team-cards-image';
      const src = img.getAttribute('src') || '';
      if (src.startsWith('./media_') || src.includes('/media_')) {
        media.append(createOptimizedPicture(img.src, img.alt || name, false, [{ width: '400' }]));
      } else {
        if (!img.alt) img.alt = name;
        media.append(picture);
      }
      li.append(media);
    }

    const h3 = document.createElement('h3');
    if (profileHref) {
      const a = document.createElement('a');
      a.href = profileHref;
      a.textContent = name;
      h3.append(a);
    } else {
      h3.textContent = name;
    }
    body.append(h3);

    if (creds.length) {
      const c = document.createElement('p');
      c.className = 'team-cards-credentials';
      c.textContent = creds.join(', ');
      body.append(c);
    }

    let titleDone = false;
    textCells.forEach((item) => {
      if (item.type === 'text') {
        const p = document.createElement('p');
        p.className = titleDone ? 'team-cards-bio' : 'team-cards-title';
        p.textContent = item.cell.textContent.trim();
        titleDone = true;
        body.append(p);
      } else {
        contacts.append(contactLink(item.type, item.value, name));
      }
    });

    if (profileHref) {
      const more = document.createElement('a');
      more.className = 'team-cards-more';
      more.href = profileHref;
      more.textContent = 'View profile';
      more.setAttribute('aria-label', `View profile: ${name}`);
      contacts.append(more);
    }

    li.append(body);
    if (contacts.children.length) li.append(contacts);
    ul.append(li);
  });

  block.replaceChildren(ul);
}
