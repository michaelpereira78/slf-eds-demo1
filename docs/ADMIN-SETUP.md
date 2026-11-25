# One-time setup for the platform demo (Michael's to-do list)

Code is already deployed: every push to `main` goes out through AEM Code Sync. Everything below
needs your Google or Adobe sign-in, so it can't be done from the repository. Allow about 30 minutes
the first time (steps 1 to 3 are the demo; steps 4 to 6 add the real form logging and roles).

Content folder: https://drive.google.com/drive/u/0/folders/1lC_k-4iU8d2cmsKwagdWcDEDz5wQRQ1O
Preview host: https://main--slf-eds-demo1--michaelpereira78.aem.page (below: **PREVIEW**)

## 1. Replace the content in Google Drive (about 10 minutes)

1. **Turn on automatic conversion.** Drive > gear icon > **Settings** > **General** > tick
   **Convert uploads to Google Docs editor format** > **Done**. (Edge Delivery Services reads
   Google Docs and Google Sheets, not .docx or .xlsx.)
2. **Empty the site folder.** Select everything in it and move it to the Trash. Almost every
   document changed, and Drive happily keeps two files with the same name.
3. **Upload.** Unzip `slf-eds-demo1-content.zip` and drag everything into the empty folder
   **except** `UPLOAD-ME.txt` and the `_new-sites` folder. Drive keeps the subfolders:
   `admin`, `advisors`, `campaigns`, `forms`, `fragments`, `harbourview`, `northstar`, `tools`.
4. Check every file shows the blue Docs or green Sheets icon. If one still says DOCX or XLSX,
   open it, **File > Save as Google Docs** (or Sheets), and delete the original.

New in this version: `advisor`, `admin`, `admin/figma-import`, the three sheets in `forms/`,
and four library documents in `tools/sidekick/blocks/` (`stats`, `testimonials`, `banner`, `cards`).

## 2. Preview everything, publish the approved pages (about 5 minutes)

In the Drive folder, open AEM Sidekick. Select files, then **Preview** (it works on many files at once).

**Preview** every file in every folder, including the spreadsheets.

**Publish** only these, so the compliance story holds up:

| Publish | Leave as preview only ("pending review" in the demo) |
|---|---|
| `index`, `nav`, `footer`, `advisors/jordan-lee` | `harbourview/*` (index, nav, footer) |
| `fragments/disclosure`, everything in `fragments/products` and `fragments/cta` | `northstar/*` (index, nav, footer) |
| `demo`, `advisor`, `admin`, `admin/figma-import`, `templates`, `layouts`, `approved-content`, `new-site`, `compliance` | `campaigns/retirement-checkup` |
| `tools/sidekick/library`, everything in `tools/sidekick/templates` and `tools/sidekick/blocks` | |
| the three sheets in `forms/` (only after step 4; the submission service reads the **published** form definition) | |

`compliance-queue` only needs a preview.

Check: PREVIEW/demo, PREVIEW/advisor, PREVIEW/admin, PREVIEW/admin/figma-import.
Until step 4 is done, the forms work in **demo mode**: the confirmation appears, the row is kept in
your browser and shown on the page, and nothing is written to Drive. The confirmation says so.

## 3. Update the Sidekick configuration (about 3 minutes)

Adds **Library**, **Advisor workspace**, **Supervisor console**, **Request compliance review**,
**Review...** and **Compliance queue**, and makes **Publish** ask "Are you sure?" first.

1. Go to https://tools.aem.live, open **Admin Edit**, sign in with the Google account that owns the site.
2. URL `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1/sidekick.json`,
   method **GET**, send. Keep note of anything other than `project` and `plugins`.
3. Method **POST**, paste the contents of [`docs/sidekick.json`](sidekick.json) as the body
   (plus anything you noted), send.
4. Reload the extension (`chrome://extensions` > AEM Sidekick > reload) and your document tab.

If the GET answers **401**, you are not signed in to Admin Edit (or you are signed in with an
account that is not in the site's `admin` role); sign in again with the owner account. (When this
was prepared, anonymous calls to the site's Admin API already answered 401 "not authenticated",
which means sign-in is already required for this site's admin API.)

## 4. Connect the forms to Google Sheets (about 10 minutes)

Three forms write rows to sheets in the `forms/` folder:

| Form (page) | Sheet in Drive | Who reads it |
|---|---|---|
| Submit for compliance review (`/advisor`), plus the Approve / Request changes buttons (`/admin`, `/compliance`) and Sidekick publishes | `forms/compliance-audit-log` | Compliance, auditors |
| Import a custom website design from Figma (`/admin/figma-import`) | `forms/figma-import-requests` | MarTech Engineering |
| Request a layout change (`/advisor`) | `forms/layout-change-requests` | Supervisors |

Each sheet has three tabs, already set up in the zip: `shared-aem` (the form definition the
service checks), `incoming` (headers only; rows are appended here) and `README`.

### Option A (preferred): Adobe's Forms Submission Service, no code, no server

This is the Edge Delivery Services way to save form submissions to a spreadsheet. Requirements:
the AEM Forms license and Adobe enabling the service for the repository (ask your Adobe
contact or open a support ticket: "enable the Forms Submission Service for
github.com/michaelpereira78/slf-eds-demo1"). Then, for **each** of the three sheets:

1. Open the sheet. Check the tabs are named exactly `shared-aem`, `incoming`, `README`, and that
   row 1 of `incoming` holds the column names (`timestamp`, `event`, `advisor`, ...). Do not rename them.
2. **Share** > add `forms@adobe.com` as **Editor** > untick "Notify people" > **Share**.
3. Adobe's documentation also asks for **General access: Anyone with the link: Viewer** on Google
   Sheets. That means anyone who has the sheet's URL can read the audit rows. Fine for the demo;
   for production, prefer Option B (private sheet) or a SharePoint/OneDrive content source.
4. In Drive, select the sheet, then Sidekick **Preview**, then **Publish**. Publishing only exposes
   the `shared-aem` tab as JSON (EDS serves tabs whose names start with `shared-`); `incoming`
   and `README` are never served.
5. Test: submit the form on the PREVIEW page. The confirmation should say **Recorded in the
   ... sheet** and a row appears in `incoming` within a few seconds. If it says **Demo mode**, the
   service rejected it (not enabled yet, sheet not published, or tab names changed).

The browser sends the same request the AEM Forms block uses:
`POST https://forms.adobe.com/adobe/forms/af/submit/<base64 of /forms/<name>.json>` with
`x-adobe-routing: tier=live,bucket=main--slf-eds-demo1--michaelpereira78`.

### Option B (fallback): a Google Apps Script web app, private sheet

No Adobe enablement needed, nothing to pay for, and the sheet can stay private. About 5 minutes;
full steps are at the top of [`docs/apps-script/form-to-sheet.gs`](apps-script/form-to-sheet.gs).
In short: create one private Google Sheet with tabs `compliance-audit-log`,
`figma-import-requests`, `layout-change-requests` (headers copied from the `incoming` tabs),
paste the script into **Extensions > Apps Script**, **Deploy > Web app** (Execute as: Me; Who
has access: Anyone), then set each form's **Submit to** row in its Google Doc to
`<web app URL>?sheet=<tab name>` and preview. For the audit log, send the URL to whoever
maintains the code: it goes in `scripts/forms.js` (`FORMS['compliance-audit'].endpoint`),
because the console buttons log to it as well.

### Make MarTech Engineering see new Figma requests

Share `forms/figma-import-requests` with the MarTech Engineering group (Editor, so they can
update the `status` column), and ask them to turn on **Tools > Notification settings >
Edit notifications > Any changes are made**. That emails them on every new request with no
extra workflow tool.

## 5. Roles: advisors author, supervisors publish (about 5 minutes, production behaviour)

Edge Delivery Services checks roles on **every Admin API call**, so this is real enforcement,
not just a hidden button:

| Role | Can | Cannot |
|---|---|---|
| `author` (advisors) | preview, edit, delete previews, list files, read snapshots, read the publish log | publish, unpublish, bulk publish, create or approve review snapshots (`live:write`, `snapshot:write`) |
| `publish` (supervisors) | everything `author` can, plus publish, unpublish, bulk publish, snapshot review and approval | (see note) |
| `admin` (you, platform team) | everything | |

Note, from Adobe's role table (https://www.aem.live/docs/roles-permissions): the built-in
`publish` role also includes `config:write`, so a supervisor could technically change the site
configuration through the Admin API. Keep the `publish` list to people you trust with that, and
keep `docs/access-admin.json` in the repository as the reviewed source of truth.

Use `author`, not `basic_author`: `basic_author` cannot list or bulk-select files in Sidekick.

1. Edit [`docs/access-admin.json`](access-admin.json): put **your own Google account** in `admin`
   (if you leave yourself out you lock yourself out of the configuration), supervisors in
   `publish`, advisors in `author`. Entries can be addresses or a whole domain like `*@yourcompany.com`.
2. Admin Edit: URL `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1/access/admin.json`,
   **GET** first (keep anything already there), then **POST** the edited JSON.
3. Test with an advisor account: Sidekick shows **Publish** greyed out; a direct call to the
   publish API answers 403. With a supervisor account, Publish works and asks for confirmation.

What this changes for everyone: once roles exist, Sidekick asks every user to **sign in** before
preview or publish. People not in any role can still read the preview and live sites (site
viewing is a separate setting), but they cannot preview or publish.

What is **not** protected by roles: the `/advisor` and `/admin` pages themselves are ordinary
web pages anyone with the URL can open. In the demo the Approve buttons only change the demo
queue in that browser and add an audit row; the real control is that only `publish` can publish.
To hide the preview site itself, use **site authentication** (Admin Edit:
`.../access/site.json` or `.../access/preview.json`), which is a separate decision.

## 6. Audit trail: what is automatic and what is manual

| Event | Written to the audit log | How |
|---|---|---|
| Advisor submits a page for review (form on `/advisor`, the status bar's **Request review**, or Sidekick **Request compliance review**) | Automatic | the page posts a `Submitted` row |
| Supervisor clicks **Approve** or **Request changes** (`/admin`, `/compliance`) | Automatic | `Approved` / `Changes requested` row with reviewer and decision date |
| Supervisor publishes with Sidekick on a page of this site | Automatic (best effort) | `Published` row, when Sidekick is open on the page and the browser is online |
| Publishes from the Drive file list or bulk publish | **Not** in the sheet | use the Admin API log below |
| Approving a snapshot in the snapshot admin tool | **Not** in the sheet | record the decision in the console, or rely on the Admin API log |

The authoritative "who published what, when" record is the Admin API's own log, which EDS keeps
for every preview and publish: Admin Edit, **GET**
`https://admin.hlx.page/log/michaelpereira78/slf-eds-demo1/main?since=7d` (needs `admin` or the
`log:read` permission). Export it into the audit sheet monthly if Compliance wants one place.

Also protect the sheet: in `incoming`, **Data > Protect sheets and ranges** so only you can
edit existing rows (the service still appends).

## 7. Optional: create a real second site (repoless)

`python3 tools/new-site/new-site.py --firm "..." --city "..." --lead "..." --theme harbour --template advisor-team`
writes starter documents, `sidekick.json` and `create-site.sh` (the Admin API calls, including the
commented role mapping from step 5). It needs an admin token, or use **Site Admin** at
https://tools.aem.live. For the demo itself this isn't needed: `/harbourview/` and `/northstar/`
show the result inside the existing site.
