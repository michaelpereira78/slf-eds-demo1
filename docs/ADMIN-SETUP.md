# One-time setup for the platform demo (Michael's to-do list)

Code is already live: every push to `main` is deployed by AEM Code Sync. What's left needs your
Google and Adobe sign-ins, so it can't be done from the repo. Allow about 20 minutes.

## 1. Replace the content in the Google Drive folder (about 10 minutes)

Content folder: https://drive.google.com/drive/u/0/folders/1lC_k-4iU8d2cmsKwagdWcDEDz5wQRQ1O

1. **Turn on automatic conversion.** In Google Drive, click the gear icon, then **Settings**,
   then **General**, and tick **Convert uploads to Google Docs editor format**. Click **Done**.
   (Edge Delivery Services reads Google Docs and Google Sheets, not .docx or .xlsx files.)
2. **Empty the site folder.** Open the folder, select everything in it (`index`, `nav`, `footer`,
   `advisors`, `fragments`) and move it to the Trash. Several of these documents changed. Drive
   allows two files with the same name, so uploading on top of the old ones would leave duplicates.
3. **Upload the new content.** Unzip `slf-eds-demo1-content.zip`. Drag everything in it into
   the empty Drive folder, **except** `UPLOAD-ME.txt` and any folder whose name starts with `_`
   (`_avatars`, `_new-sites`). Drive keeps the subfolders: `advisors`, `campaigns`, `fragments`,
   `harbourview`, `northstar`, `tools`.
4. Check that every file shows a blue Docs icon or a green Sheets icon. If a file still shows
   "DOCX" or "XLSX", open it and choose **File > Save as Google Docs** (or Sheets), then delete
   the original.

## 2. Preview everything, and publish the approved pages (about 5 minutes)

In the Drive folder, click the AEM Sidekick icon. It can preview many files at once: select files
in the list, then choose **Preview** in Sidekick.

**Preview** everything: all files in the root folder and in every subfolder, including both
spreadsheets (`compliance-queue`, `tools/sidekick/library`).

**Publish** only the approved pages, so the compliance story holds up in the demo:

| Publish | Leave as preview only (they are "pending review" in the demo) |
|---|---|
| `index`, `nav`, `footer`, `advisors/jordan-lee` | `harbourview/*` (index, nav, footer) |
| `fragments/disclosure` and everything under `fragments/products`, `fragments/cta` | `northstar/*` (index, nav, footer) |
| `demo`, `templates`, `layouts`, `approved-content`, `new-site`, `compliance` | `campaigns/retirement-checkup` |
| `tools/sidekick/library`, everything under `tools/sidekick/templates` and `tools/sidekick/blocks` | |

`compliance-queue` only needs a preview, because the queue is read from the preview site.

Check: https://main--slf-eds-demo1--michaelpereira78.aem.page/demo

## 3. Update the Sidekick configuration (about 3 minutes)

This adds the **Library**, **Request compliance review**, **Review...** and **Compliance queue**
buttons. It also removes the leftover `editUrlPattern` line that sends **Edit** to da.live.

1. Go to https://tools.aem.live, open **Admin Edit** and sign in with the account you used for setup.
2. URL: `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1/sidekick.json`.
   Method **GET**, then send. Note anything in it other than `project`, `editUrlPattern` and
   `plugins`. If there is anything else, keep it in the JSON below.
3. Switch the method to **POST**, replace the body with the JSON below and send it:

```json
{
  "project": "Advisor Demo",
  "plugins": [
    {
      "id": "library",
      "title": "Library",
      "environments": ["edit"],
      "url": "/tools/sidekick/library.html"
    },
    {
      "id": "request-compliance-review",
      "title": "Request compliance review",
      "environments": ["dev", "preview"],
      "event": "request-compliance-review"
    },
    {
      "id": "review",
      "title": "Review...",
      "environments": ["dev", "preview", "review"],
      "url": "https://tools.aem.live/tools/snapshot-admin/popover.html",
      "isPopover": true,
      "popoverRect": "width:400px; height:400px",
      "passConfig": true,
      "passReferrer": true
    },
    {
      "id": "compliance-queue",
      "title": "Compliance queue",
      "environments": ["preview", "review"],
      "url": "/compliance",
      "pinned": false
    }
  ]
}
```

(The same JSON is in [`docs/sidekick.json`](sidekick.json).)

4. Run the **GET** again to confirm that `editUrlPattern` is gone. Reload the extension
   (`chrome://extensions`, then reload AEM Sidekick) and reload your document tab.
   **Edit** now opens the Google Doc, and **Library** appears in Sidekick when a Google Doc is open.

If a POST to `sidekick.json` is rejected, use the site-level URL
`https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1.json`: GET it, edit only the
`sidekick` object in the response, and POST the whole document back.

## 4. Optional (production only, not for the demo): only Compliance can publish

Edge Delivery Services roles: `basic_author` can edit and preview but **cannot publish**;
`publish` adds publishing. The snapshot **Approve** action also needs the `publish` role.
In production you would map roles to groups:

```
POST https://admin.hlx.page/config/<org>/sites/<site>/access/admin.json
{ "role": { "basic_author": ["*@yourcompany.com"], "publish": ["compliance-publishers@yourcompany.com"], "admin": ["platform-admins@yourcompany.com"] } }
```

Do **not** do this on the demo site: once roles are set, Sidekick asks everyone to sign in, and
anyone not in the list gets "forbidden".

## 5. Optional: create a real second site (repoless)

`python3 tools/new-site/new-site.py --firm "..." --city "..." --lead "..." --theme harbour --template advisor-team`
writes starter documents plus `create-site.sh` (one `PUT /config/<org>/sites/<site>.json` call
that reuses this repository's code). It needs an AEM admin token, or you can use **Site Admin**
at https://tools.aem.live to add the site with the new Drive folder as its content source. For
the demo itself this isn't needed: `/harbourview/` and `/northstar/` show the result inside
the existing site.
