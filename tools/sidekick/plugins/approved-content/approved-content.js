/**
 * Sidekick Library plugin: "Approved content".
 * Lists the Compliance-approved fragments from the `helix-approved-content` sheet of
 * /tools/sidekick/library (columns: name, path, approval, description).
 * "Copy link" puts a link on the clipboard; pasted on its own line in a document,
 * the page embeds the approved fragment, so authors reuse the wording without editing it.
 */
function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'class') e.className = v;
    else if (k === 'text') e.textContent = v;
    else e.setAttribute(k, v);
  });
  children.flat().forEach((c) => c && e.append(c));
  return e;
}

async function copyLink(url, label) {
  const html = `<a href="${url}">${url}</a>`;
  if (window.ClipboardItem) {
    await navigator.clipboard.write([new ClipboardItem({
      'text/html': new Blob([html], { type: 'text/html' }),
      'text/plain': new Blob([url], { type: 'text/plain' }),
    })]);
  } else {
    await navigator.clipboard.writeText(url);
  }
  return label;
}

export async function decorate(container, data, query) {
  const rows = (data || []).filter((r) => !query
    || `${r.name} ${r.description} ${r.approval}`.toLowerCase().includes(query.toLowerCase()));
  const style = el('style', {
    text: `.ac{font-family:sans-serif;padding:12px;display:grid;gap:12px}
.ac-item{background:#fff;border-radius:8px;padding:12px 14px;border-left:5px solid #f9a66c}
.ac-item h3{margin:0 0 4px;font-size:16px}.ac-item p{margin:4px 0;font-size:13px;color:#444}
.ac-id{font-weight:700;color:#1e4d3b}.ac-actions{display:flex;gap:8px;margin-top:8px}`,
  });
  const list = el(
    'div',
    { class: 'ac' },
    style,
    ...rows.map((r) => {
      const url = new URL(r.path, window.location.origin).href;
      const copy = el('sp-button', { size: 's', text: 'Copy link' });
      copy.addEventListener('click', async () => {
        try {
          await copyLink(url, r.name);
          container.dispatchEvent(new CustomEvent('Toast', { detail: { message: `Copied "${r.name}". Paste it on its own line.`, variant: 'positive' } }));
          copy.textContent = 'Copied';
        } catch (e) {
          copy.textContent = 'Copy failed';
        }
      });
      const view = el('sp-button', { size: 's', variant: 'secondary', text: 'Preview' });
      view.addEventListener('click', () => window.open(url, '_blank'));
      return el(
        'div',
        { class: 'ac-item' },
        el('h3', { text: r.name }),
        el('p', { class: 'ac-id', text: `Approval ${r.approval}` }),
        el('p', { text: r.description }),
        el('div', { class: 'ac-actions' }, copy, view),
      );
    }),
  );
  if (!rows.length) list.append(el('p', { text: 'No approved content matches your search.' }));
  container.replaceChildren(list);
}

export default { title: 'Approved content', searchEnabled: true };
