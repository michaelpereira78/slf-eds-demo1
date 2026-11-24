/**
 * Helpers for author-only features (compliance status, approval badges).
 * These only show on authoring hosts: local dev, *.aem.page (preview) and
 * *.aem.reviews (review snapshots). Site visitors on *.aem.live never see them.
 */

export function isAuthorHost(host = window.location.hostname) {
  return host === 'localhost'
    || host === '127.0.0.1'
    || host.endsWith('.aem.page')
    || host.endsWith('.aem.reviews');
}

/**
 * Removes an "Approved | <id>" row from an approved-content block and, on authoring hosts,
 * shows it as a small badge so authors and reviewers can see the content is pre-approved.
 * @param {Element} block the block element
 * @returns {string} the approval text ('' if none)
 */
export function takeApproval(block) {
  const row = [...block.children].find((r) => r.children.length === 2
    && r.children[0].textContent.trim().toLowerCase() === 'approved');
  if (!row) return '';
  const text = row.children[1].textContent.trim();
  row.remove();
  block.dataset.approval = text;
  if (isAuthorHost()) {
    const badge = document.createElement('p');
    badge.className = 'approval-badge';
    badge.textContent = `Approved content: ${text}`;
    block.append(badge);
  }
  return text;
}
