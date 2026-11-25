/**
 * Stats block: a strip of key facts.
 * One row per fact: value | label (for example "20+" | "years serving Halifax families").
 * @param {Element} block The stats block element
 */
export default function decorate(block) {
  const ul = document.createElement('ul');
  ul.setAttribute('role', 'list');
  [...block.children].forEach((row) => {
    const [value, label] = [...row.children].map((c) => c.textContent.trim());
    if (!value) return;
    const li = document.createElement('li');
    const strong = document.createElement('strong');
    strong.textContent = value;
    const span = document.createElement('span');
    span.textContent = label || '';
    li.append(strong, span);
    ul.append(li);
  });
  block.replaceChildren(ul);
}
