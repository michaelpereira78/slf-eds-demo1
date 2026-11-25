/**
 * Accordion block: question | answer rows, rendered as native <details> elements.
 * @param {Element} block The accordion block element
 */
export default function decorate(block) {
  [...block.children].forEach((row) => {
    const [label, body] = row.children;
    if (!label) return;
    const details = document.createElement('details');
    details.className = 'accordion-item';
    const summary = document.createElement('summary');
    summary.className = 'accordion-item-label';
    summary.append(...label.childNodes);
    details.append(summary);
    if (body) {
      body.className = 'accordion-item-body';
      details.append(body);
    }
    row.replaceWith(details);
  });
}
