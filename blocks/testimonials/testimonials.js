/**
 * Testimonials block.
 * One row per quote: quote | name | context (for example "Client since 2015").
 * An optional first cell with a picture becomes a small round photo.
 * Testimonials are regulated advertising: keep the Compliance Status workflow
 * on any page that uses them.
 * @param {Element} block The testimonials block element
 */
export default function decorate(block) {
  const ul = document.createElement('ul');
  ul.setAttribute('role', 'list');
  [...block.children].forEach((row) => {
    const cells = [...row.children];
    const picCell = cells.find((c) => c.querySelector('picture') && !c.textContent.trim());
    const text = cells.filter((c) => c !== picCell);
    const [quote, name, context] = text;
    if (!quote) return;
    const li = document.createElement('li');
    const figure = document.createElement('figure');
    const bq = document.createElement('blockquote');
    bq.append(...quote.childNodes);
    const cap = document.createElement('figcaption');
    if (picCell) {
      const media = document.createElement('span');
      media.className = 'testimonials-photo';
      media.append(picCell.querySelector('picture'));
      cap.append(media);
    }
    const who = document.createElement('span');
    who.className = 'testimonials-who';
    const strong = document.createElement('strong');
    strong.textContent = name ? name.textContent.trim() : '';
    who.append(strong);
    if (context && context.textContent.trim()) {
      const small = document.createElement('span');
      small.textContent = context.textContent.trim();
      who.append(small);
    }
    cap.append(who);
    figure.append(bq, cap);
    li.append(figure);
    ul.append(li);
  });
  block.replaceChildren(ul);
}
