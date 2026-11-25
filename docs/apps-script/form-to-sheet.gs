/**
 * Fallback receiver for the site's request forms (only needed if the AEM Forms Submission
 * Service is not enabled for this repository). No Power Automate, no server: a Google Apps
 * Script web app owned by the supervisor's Google account appends each row to a private sheet.
 *
 * Setup (about 5 minutes, see docs/ADMIN-SETUP.md, "Option B"):
 *  1. Create a Google Sheet (it can stay private) with three tabs named exactly:
 *       compliance-audit-log, figma-import-requests, layout-change-requests
 *     Row 1 of each tab = the column headers from the `incoming` tab of the matching .xlsx in
 *     the content zip (forms/*.xlsx). Extra or reordered columns are fine.
 *  2. Extensions > Apps Script. Replace the code with this file. Save.
 *  3. Deploy > New deployment > type "Web app". Execute as: Me. Who has access: Anyone.
 *     Copy the web app URL (https://script.google.com/macros/s/.../exec).
 *  4. In each form's Google Doc, set the block's "Submit to" row to the URL plus ?sheet=<tab>, e.g.
 *       https://script.google.com/macros/s/XXXX/exec?sheet=figma-import-requests
 *     and Preview the page. (The compliance audit log URL goes in scripts/forms.js, FORMS
 *     'compliance-audit'.endpoint, because the log is also written by the console buttons.)
 *
 * The site posts JSON as text/plain with mode "no-cors", so the browser never sees the
 * response: the confirmation on the page cannot prove the row was written. Check the sheet.
 * Anyone who knows the URL can post rows; treat the sheet as a convenience log, and use the
 * AEM Admin API publish log (GET https://admin.hlx.page/log/<org>/<site>/main) as the
 * authoritative record of who published what.
 */

const ALLOWED_SHEETS = ['compliance-audit-log', 'figma-import-requests', 'layout-change-requests'];
const MAX_CELL = 2000;

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const name = (e.parameter && e.parameter.sheet) || 'compliance-audit-log';
    if (ALLOWED_SHEETS.indexOf(name) < 0) return reply({ ok: false, error: 'unknown sheet' });
    const sheet = SpreadsheetApp.getActive().getSheetByName(name);
    if (!sheet) return reply({ ok: false, error: 'missing tab ' + name });

    let data = JSON.parse(e.postData.contents || '{}');
    if (data && data.data) data = data.data; // accept { data: {...} } as well

    const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const row = headers.map((h) => {
      let v = data[h] == null ? '' : String(data[h]).slice(0, MAX_CELL);
      if (/^[=+\-@]/.test(v)) v = "'" + v; // never let a submission become a formula
      return v;
    });
    // keep a server-side receive time next to the browser's timestamp
    const received = headers.indexOf('receivedAt');
    if (received >= 0) row[received] = new Date().toISOString();
    sheet.appendRow(row);
    return reply({ ok: true });
  } catch (err) {
    return reply({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
