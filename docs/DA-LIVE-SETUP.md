# Add da.live (Document Authoring) as a second editing option

**Goal:** let advisors edit the same demo websites in the browser at **da.live** instead of Google Docs,
and show both side by side, **without touching anything already built**. The Google Drive site
`slf-eds-demo1` stays exactly as it is.

**Approach (Adobe calls it "repoless"):** create a **second site**, `slf-eds-demo1-da`, that runs on
the **same GitHub repository and the same code**, but reads its content from da.live instead of
Google Drive. Every block, template, popup and workspace page keeps working because the code is
shared. Content is *not* shared: the two sites have separate copies of every page.

| | Existing site | New site |
|---|---|---|
| Org / site | `michaelpereira78` / `slf-eds-demo1` | `michaelpereira78` / `slf-eds-demo1-da` |
| Code | github.com/michaelpereira78/slf-eds-demo1 | **same repo, same branch** |
| Content source | Google Drive folder (type `google`) | `https://content.da.live/michaelpereira78/slf-eds-demo1-da/` (type `markup`) |
| Edited in | Google Docs + Sidekick | da.live (`https://da.live/#/michaelpereira78/slf-eds-demo1-da`) |
| Preview | https://main--slf-eds-demo1--michaelpereira78.aem.page | https://main--slf-eds-demo1-da--michaelpereira78.aem.page |
| Live | https://main--slf-eds-demo1--michaelpereira78.aem.live | https://main--slf-eds-demo1-da--michaelpereira78.aem.live |

> **Naming note.** Adobe has renamed Document Authoring **Experience Workspace** (EW). The address is
> still da.live and the Adobe docs use both names ("DA" in older pages). This guide says "da.live".
> The older editor (`https://da.live/edit#/...`) is what the steps below use; the newer EW editor
> (`/canvas`) is an optional switch, see step 14.
>
> **Why the DA folder is named `slf-eds-demo1-da` and not `slf-eds-demo1`.** The Sidekick's Edit
> button builds its link from the Edge Delivery *site* name, and Adobe's examples use the same
> name for the Edge Delivery site and its da.live folder. Using the same name for both keeps the
> Edit button, the permissions sheet and the content URL consistent. (An earlier outline
> suggested `.../slf-eds-demo1/` as the da.live folder. Because the Sidekick pattern uses the
> Edge Delivery site name, the folder should carry the new site's name; use `slf-eds-demo1-da`.)

**Time:** about 60 to 90 minutes the first time (most of it is checking the imported pages).
**Nothing in this guide changes the existing site's config, content or code.**

---

## 0. What the research says (sources) and what is unclear

Everything below was checked against Adobe's current documentation on 26 November 2026:

| Topic | Source |
|---|---|
| Repoless sites, the `PUT .../sites/{site}.json` call | https://www.aem.live/docs/repoless and https://www.aem.live/docs/config-service-setup |
| Config service rules (canonical site, changing content source) | https://www.aem.live/docs/config-service-setup |
| Roles (`author`, `publish`, `admin`) and `access/admin.json` | https://www.aem.live/docs/authentication-setup-authoring and https://www.aem.live/docs/roles-permissions |
| da.live permissions sheet | https://www.aem.live/docs/ew/administering/permissions and https://da.live/docs/administration/permissions and https://www.aem.live/docs/ew/administering/access-control |
| da.live and Edge Delivery config are two different things | https://www.aem.live/docs/ew/administering/configs |
| Importing from an existing aem.page site | https://www.aem.live/docs/ew/administering/restore-from-aem |
| Upgrading a Drive/SharePoint site to da.live (differences, known limits) | https://docs.da.live/administrators/guides/upgrade-site and https://docs.da.live/developers/guides/upgrading |
| Sidekick `editUrlLabel` / `editUrlPattern` | https://www.aem.live/developer/sidekick-development and https://www.aem.live/docs/ew/about |
| Bulk preview and publish | https://www.aem.live/docs/ew/authoring/bulk-operations and https://docs.da.live/authors/guides/apps/bulk-operations |
| Content browser, editor, publishing | https://www.aem.live/docs/ew/authoring/browsing-content , `/document-editor` , `/publishing` , `/editing-sheets` (same folder) |
| Admin API reference (create = PUT, delete = DELETE) | https://www.aem.live/docs/admin.html |
| Forms Submission Service | https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/edge-delivery/build-forms/forms-submission-service |

**Answers to the questions that decide whether the plan is safe**

- **Does repoless need `fstab.yaml` or the repo changed?** No. `slf-eds-demo1` already has **no
  `fstab.yaml`** (see `AGENTS.md` and `docs/TECHNICAL-HANDOFF.md` section 10); its content source lives in the
  **configuration service**. Repoless sites are defined only in the configuration service
  (`code` + `content.source`); Adobe's table lists `fstab.yaml` as the old "document mode"
  location of the content source, and says that once the configuration service is used, its
  settings override repository files. **No commit to the repo is needed to create the second site.**
- **Can the Drive site remain the "canonical" site?** Yes, and it must. Adobe requires one
  canonical site whose `org/site` equals the GitHub `owner/repo`. That is `michaelpereira78` /
  `slf-eds-demo1`. Do **not** change its `code` or `content` settings: Adobe warns that changing
  `content` on an existing site creates a new content bus, so everything would have to be re-previewed
  and republished. That is exactly why we **add a site** instead of switching the existing one.
- **Do code pushes reach both sites?** Yes. Every push to `main` is picked up through AEM Code Sync
  for every site that uses this repo. A change to a block changes both sites.
- **Content type value.** Adobe's repoless page shows the content source without a `type`;
  the configuration-service page and the Admin API schema require `"type": "markup"` for da.live
  (schema: `required: [type, url]`). This guide uses `"type": "markup"`.

**Things the documentation does not clearly say (marked "verify" in the steps)**

1. How a **brand-new da.live org/site folder** is created from nothing. Adobe's migration guidance
   says "create the DA org and site folders in da.live" but gives no menu path. Step 3 gives the
   simplest approach and what to expect.
2. Whether the **import app** keeps every block, section style and metadata table when it reads
   rendered `aem.page` pages. Adobe's restore guide says to import your `aem.page` URLs and
   "validate your content after importing". Step 9 includes the checks.
3. Whether the **Forms Submission Service** accepts a da.live-based site. Adobe documents Google
   Sheets, OneDrive and SharePoint only. See step 11.
4. Whether **Experience Workspace features (the AI assistant)** are included in your licence.
   See the caveats.

---

## 1. Prerequisites

- [ ] **An Adobe ID** (free) for Michael, using the email you want as the admin. da.live signs in
      with Adobe Identity (IMS). If your Adobe ID email differs from your Google email, use the
      **Adobe** email in the da.live lists below and the **same** address in the Edge Delivery
      `access/admin.json` role lists (da.live users authenticate with Adobe sign-in, per Adobe's authentication guide).
- [ ] **Chrome** with the **AEM Sidekick** extension (already installed for the Drive site).
- [ ] The **AEM Code Sync** GitHub app is already installed on `michaelpereira78/slf-eds-demo1`
      (it is: the first site works). Nothing to install again.
- [ ] You can open **Admin Edit** at https://tools.aem.live/tools/admin-edit/index.html and are
      signed in as the org owner (same as ADMIN-SETUP steps 3 and 5).
- [ ] Optional but helpful: a **second and third Adobe ID/email** (one pretend advisor, one pretend
      supervisor) for testing roles. Advisors and supervisors need an Adobe ID to edit in da.live.

---

## 2. Decide the names (2 minutes)

Use these exact values (everything below uses them):

| Thing | Value |
|---|---|
| Edge Delivery org | `michaelpereira78` |
| New Edge Delivery site | `slf-eds-demo1-da` |
| da.live path (org / folder) | `michaelpereira78` / `slf-eds-demo1-da` |
| Content source URL | `https://content.da.live/michaelpereira78/slf-eds-demo1-da/` |

---

## 3. Open da.live and secure it before adding content (10 minutes)

Content in da.live is **public by default** until a permissions sheet exists (Adobe's upgrade guide:
"By default, your content is public on [da.live]. You will be prompted to secure your sandbox"). Lock it
first, then import.

1. Go to https://da.live and **Sign in** with your Adobe ID.
2. Open your project folder: https://da.live/#/michaelpereira78/slf-eds-demo1-da
   *(Verify: if the folder does not exist yet, da.live may show an empty list or an error; that is
   expected. The folder appears when the first content is imported in step 9. If da.live offers a
   prompt to create or secure the sandbox, accept it.)*
3. Open the **organization config** (this is the da.live config, **not** the Edge Delivery config):
   https://da.live/config#/michaelpereira78/
   (From the content browser at the org level you can also click the **Settings** icon and choose
   the configuration, per https://www.aem.live/docs/ew/authoring/browsing-content.)
4. In the sheet, create a tab named **`permissions`** with the columns `path`, `groups`, `actions`
   (and optionally `comments`) and enter the rows below. **Put your own row first**; Adobe warns
   that without a `CONFIG` row for yourself you can lock yourself out.

   | path | groups | actions | comments |
   |---|---|---|---|
   | `CONFIG` | `YOUR-ADOBE-EMAIL@example.com` | `write` | Michael: can edit the da.live config and permissions |
   | `/ + **` | `YOUR-ADOBE-EMAIL@example.com` | `write` | Michael: everything in the org |
   | `/slf-eds-demo1-da/+**` | `supervisor.one@example.com, supervisor.two@example.com` | `write` | supervisors edit the whole site |
   | `/slf-eds-demo1-da/+**` | `advisor.one@example.com, advisor.two@example.com` | `write` | advisors edit pages |
   | `/slf-eds-demo1-da/admin/+**` | `advisor.one@example.com, advisor.two@example.com` | `read` | advisors can read but not change the supervisor console |
   | `/slf-eds-demo1-da/compliance-queue.json` | `advisor.one@example.com, advisor.two@example.com` | `read` | only Compliance edits the queue |
   | `/slf-eds-demo1-da/forms/+**` | `advisor.one@example.com, advisor.two@example.com` | `read` | form sheets are read only for advisors |
   | `/slf-eds-demo1-da/CONFIG` | `advisor.one@example.com, advisor.two@example.com` | `read` | lets advisors use the da.live block library; read only |

   Rules from Adobe's access-control page: `write` includes `read` and delete; an empty action
   means no access; the **longest matching path wins** per person; `/x/+**` includes the folder itself,
   `/x/**` does not; for people listed individually the rules are **per email and then merged**, so an
   advisor who is *also* given broader `write` somewhere else keeps it. Use real addresses
   for the people you test with. Everyone must use their **Adobe ID** email.
5. **Save** the config. Reload https://da.live/#/michaelpereira78/slf-eds-demo1-da and confirm you
   still have access. If someone is added to a group later, they must **sign out and in** to da.live
   again (Adobe FAQ).

> **This sheet only controls who may edit and read content in da.live.** It does not control who may
> preview or publish. That is the Edge Delivery roles in step 6 (Adobe: "Does this have anything to
> do with previewing and publishing permissions? No.").

---

## 4. Read the existing site's config (3 minutes, read only)

You want the new site's `code` block to match the existing one exactly.

1. Open Admin Edit: https://tools.aem.live/tools/admin-edit/index.html
2. URL: `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1.json`, method **GET**,
   send. (Anonymous calls answer 401; you must be signed in.)
3. Note the `code` object. Expect `{"owner": "michaelpereira78", "repo": "slf-eds-demo1"}`
   (it may also contain a `source` object; if so, copy it into the new config too).
4. **Do not change anything here.**

---

## 5. Create the second site (3 minutes)

In Admin Edit:

- URL: `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1-da.json`
- Method: **PUT** (PUT *creates* a site; Adobe's API answers `409` if the site already exists)
- Body: the contents of [`docs/site-config-da.json`](site-config-da.json):

```json
{
  "code": {
    "owner": "michaelpereira78",
    "repo": "slf-eds-demo1"
  },
  "content": {
    "source": {
      "type": "markup",
      "url": "https://content.da.live/michaelpereira78/slf-eds-demo1-da/"
    }
  }
}
```

Equivalent `curl` (only if you have an admin token; Admin Edit is simpler and needs no token):

```sh
curl -X PUT https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1-da.json \
  -H 'x-auth-token: <token>' -H 'content-type: application/json' \
  --data @docs/site-config-da.json
```

**Check:** open https://main--slf-eds-demo1-da--michaelpereira78.aem.page/. Adobe says that on first
access you will most likely see only the `404.html` because no content has been previewed. That is
the success signal here: the host exists and serves your code. (If you get "site not found", wait a
minute and re-check the org/site spelling in the URL.)

**Immediately do step 6.** Until roles exist, a new site has Adobe's defaults: with `requireAuth: auto` and no
role mapping, the default role is `basic_publish`, which includes publishing.

---

## 6. Roles on the new site: advisors author, supervisors publish (5 minutes)

Same model as ADMIN-SETUP step 5, posted to the **new** site. Edge Delivery enforces these roles on
every API call, including calls made by da.live's Preview and Publish buttons.

1. Open [`docs/access-admin-da.json`](access-admin-da.json) and put **real addresses** in (the
   same Adobe sign-in emails you used in step 3). **Keep your own address in `admin`** or you lock
   yourself out of the site's configuration.

```json
{
  "role": {
    "admin":   ["YOUR-ADOBE-EMAIL@example.com"],
    "publish": ["supervisor.one@example.com", "supervisor.two@example.com"],
    "author":  ["advisor.one@example.com", "advisor.two@example.com"]
  },
  "requireAuth": "auto"
}
```

2. Admin Edit: URL `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1-da/access/admin.json`,
   method **POST**, body = the JSON above.
   (There is nothing to GET first; the site is new. If you want to be careful, GET it to see `{}` or 404.)
3. Roles recap (https://www.aem.live/docs/roles-permissions): `author` can preview, list and edit
   source, but has **no** `live:write`, so cannot publish; `publish` adds publish, unpublish,
   snapshots, **and `config:write`** (a supervisor can technically change site config; keep the list short);
   `admin` can do everything.
4. With roles defined, Edge Delivery requires sign-in for preview and publish actions
   (`requireAuth: auto`). People not listed can still view the preview and live sites.

> **Expect this in the demo:** an advisor in da.live **will still see the Publish button**,
> because da.live does not hide it. Clicking it fails with a permission error from Edge Delivery
> (403). That is real enforcement; say so in the demo. In da.live the same advisor can
> **Preview**. (Verify this once with a test account; the exact wording of da.live's error message
> is not documented.)

---

## 7. Sidekick for the new site (3 minutes)

Posts the same custom Sidekick as the Drive site, plus the two fields that make the Sidekick's
**Edit** button open da.live.

1. Admin Edit: URL `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1-da/sidekick.json`,
   method **POST**, body = [`docs/sidekick-da.json`](sidekick-da.json).
2. The new fields at the top are:

```json
"project": "Advisor Demo (da.live)",
"editUrlLabel": "Document Authoring",
"editUrlPattern": "https://da.live/edit#/{{org}}/{{site}}{{pathname}}"
```

   (`{{org}}`, `{{site}}` and `{{pathname}}` are Sidekick placeholders; pattern from Adobe's
   da.live Sidekick examples.) The plugins (Library, Advisor workspace, Supervisor console, Request
   compliance review, Review..., Compliance queue) are the same as `docs/sidekick.json`.
3. Reload the extension (`chrome://extensions`, AEM Sidekick, reload), then open the new site's
   preview URL. If you see a **picker with both sites**, choose `slf-eds-demo1-da`
   (Adobe: the Sidekick lists all matching sites once the new site has been added to it from its
   preview or live URL).
4. The Sidekick's **Library** plugin is limited to `edit` environments in the existing config, which
   are Google/Word editor tabs. da.live has its **own** block library (step 12).

---

## 8. Get the content out of the Drive site (5 minutes)

The best source is the **live preview of the existing site**: the 53 pages and 5 sheets are already
published to `aem.page`. Two ready-made lists are in this repo (every URL was checked as HTTP 200 on
26 Nov 2026):

- [`docs/da-import-urls.txt`](da-import-urls.txt): 53 pages (home, `/advisor`, `/admin`, subpages,
  nav and footer documents, fragments, Sidekick library blocks and templates, firm sites, campaigns)
- [`docs/da-import-sheets.txt`](da-import-sheets.txt): the 5 sheets as `.json` URLs
  (`compliance-queue`, `tools/sidekick/library`, and the three `forms/*` sheets)

Adobe's alternative for a full re-list (any site, any size): call the **Status API** with
`select: ["preview"]` or `["live"]` and `pathsOnly: true`, then add `/details` to the job URL; the
response lists every doc, sheet and image (see https://www.aem.live/docs/ew/administering/restore-from-aem).
For this demo the lists above are enough.

If the Drive site requires sign-in for **preview** (site authentication), the import cannot fetch
the pages. The demo site does not have site authentication on (`access/admin.json` is a role list;
viewing is open).

---

## 9. Import into da.live (15 to 25 minutes)

1. Open https://da.live/apps/import (signed in).
2. Paste the contents of `docs/da-import-urls.txt` (one fully qualified URL per line).
   Adobe: "submit the list of resources … prefix the paths with your fully-qualified `aem.page` domain".
3. Choose the destination as your new site, `michaelpereira78` / `slf-eds-demo1-da`.
   *(Verify the destination field on the page: the exact layout of the import app is not documented.)*
4. Start the import. Wait for it to finish; fix and rerun any failed URLs.
5. Import the sheets from `docs/da-import-sheets.txt` the same way. Adobe says the restore query
   covers "docs, sheets, redirects, images, and video". **If a sheet does not import**, create it in da.live
   (content browser, **New** or the add icon at the end of the breadcrumbs, **Sheet**, name it,
   Create), then paste the rows. All sheets are **public by default**; a sheet whose name starts with
   `private-` is private. The sheets here must be public because the pages read them in the browser.
6. Images: the import brings the page's images with it (limits: 10 MB per image, 100 images per
   document; the demo is far below both).
7. **Forms sheets:** the three `forms/*` sheets are served from a `shared-aem` tab only; the
   `incoming` tab (where rows land) never reaches the aem.page URL, so it cannot be imported. See step 11.

**Open each page in da.live and spot check** (list view in the content browser, click a row):

| Check | What good looks like |
|---|---|
| Blocks | Hero, Cards, Contact, Callout, Stats, Request form, Compliance queue appear as **tables** with the block name in the first row |
| Metadata | The page's `Template`, `Theme`, `Nav`, `Footer` rows are in a **Metadata** table at the bottom (the workspace pages depend on these) |
| Section styles | `Section Metadata` tables keep `Style: Light / Dark / Accent / ...` |
| Links | Links to the other site: search for `slf-eds-demo1--` (see below) |

**Fix absolute links.** Some documents contain links that include the full Drive-site host
(`main--slf-eds-demo1--michaelpereira78.aem.page/...`), for example the approved-content link
list. In the da.live content browser, use the search field, press **Enter** to search subfolders,
open **Advanced Search**, and use **Replace with** to change `slf-eds-demo1--michaelpereira78` to
`slf-eds-demo1-da--michaelpereira78`. Adobe warns that replacing text **does not create a version**,
so search first and read the match list before replacing.

---

## 10. Preview and publish the content (10 minutes)

Preview first, publish after you have checked.

**Preview everything (bulk):**
1. In the da.live content browser, open the site folder, tick the checkbox at the top of the list
   to select everything, and use the action bar's **Preview** (or **Share**, which copies the
   URLs). Repeat for each sub-folder (`admin`, `advisor`, `fragments`, `tools`, `forms`, ...).
2. Alternative for many URLs at once: **Apps**, **Bulk Operations** (https://da.live/apps/bulk),
   paste the URLs (use **Share** in the browser to collect them, or **Traverse** at
   https://da.live/apps to crawl `/michaelpereira78/slf-eds-demo1-da`), choose **Preview**, **Submit**.
3. Open https://main--slf-eds-demo1-da--michaelpereira78.aem.page/demo and click through
   `/advisor`, `/admin`, `/harbourview/`, `/northstar/`, `/templates`, `/layouts`.

**Publish (admin or supervisor account only):**
1. The same action bar, **Publish**; or in the editor use **Publish** (top right),
   or the Sidekick's **Publish** on the preview page (it asks "Are you sure?").
2. Check the `.aem.live` host: https://main--slf-eds-demo1-da--michaelpereira78.aem.live/

**Verification checklist** (what "working" means):

- [ ] `https://main--slf-eds-demo1-da--michaelpereira78.aem.page/` shows the Maple Ridge home page styled exactly like the Drive site.
- [ ] `/advisor` and `/admin` show their **own navigation** (the `workspace` template and the
      `Nav` metadata fragments came across).
- [ ] The Advisor workspace's "Submit for compliance review" opens as a **popup** (`?modal`), not a full page.
- [ ] `/harbourview/` is blue/serif (Harbour theme) and `/northstar/` is slate (themes work).
- [ ] The Sidekick on a preview page shows **Edit**, which opens da.live on the same page, and the custom buttons (Advisor workspace, ...).
- [ ] An **advisor account** cannot publish (403); a **supervisor account** can.

**Header menu check.** da.live and Drive markup differ slightly: a list nested inside another
list gets an extra `<p>` wrapper (Adobe's "known issues"). Our nav and footer documents use flat
lists, so this should not matter, but click the main navigation once on desktop and mobile width.

---

## 11. Forms and the audit log (decide before the demo)

The demo's three forms and the compliance audit log are written by `scripts/forms.js`. Three
destinations are supported; **the code is shared by both sites**:

- **Demo mode (default if nothing is connected):** the confirmation still shows and the submission is
  stored in the presenter's browser. **This is what the da.live site does until you connect something.**
  For a side-by-side editing demo this is perfectly fine.
- **Forms Submission Service:** Adobe documents Google Sheets, OneDrive and SharePoint as the places
  rows land. da.live sheets are **not documented** as a target. Assume it will **not** work for the
  da.live site and that the page will fall back to demo mode. (Not tested; Adobe would have to confirm.)
- **Google Apps Script web app (recommended if you want real logging on both sites):** the same web
  app from `docs/apps-script/form-to-sheet.gs` can serve both sites. For the two request forms,
  set the form's **Submit to** row to `<web app URL>?sheet=<tab>` in each da.live document, same as
  Drive. The **audit log** endpoint is in code (`FORMS['compliance-audit'].endpoint` in
  `scripts/forms.js`), so pointing it at the Apps Script changes **both** sites at once; that is a
  code change for the developers, not a content change.

---

## 12. Block and template library for authors (optional, 15 minutes)

da.live has its own library (blocks, templates, icons). It is separate from the Sidekick Library
plugin (which opens from Google Docs). Setup is documented at
https://docs.da.live/administrators/guides/setup-library and the content already exists in the imported
`tools/sidekick/blocks/*` and `tools/sidekick/templates/*` documents:

1. In da.live create a `library` folder in the site. Create a sheet `library/blocks` with columns
   `name`, `path` and one row per block: `path` =
   `https://content.da.live/michaelpereira78/slf-eds-demo1-da/tools/sidekick/blocks/hero`, etc.
2. Create `library/templates` with columns `key`, `value` pointing at the three template documents.
3. Open the **site config** (https://da.live/config#/michaelpereira78/slf-eds-demo1-da, or the gear/Settings
   icon at the site root), add a tab **`library`** with columns `title`, `path`, `format`, `ref`, `icon`,
   `experience`, and rows `Blocks` and `Templates` whose `path` is the published `.json` URL of each sheet.
4. Authors need `read` on `/slf-eds-demo1-da/CONFIG` (already in step 3) to see it.
5. Test: open a page, place the cursor, open the tools panel, **Blocks**.

---

## 13. Add or remove advisors and supervisors

A person needs **two** entries because there are two systems:

| System | Where | What it controls |
|---|---|---|
| da.live permissions | `https://da.live/config#/michaelpereira78/`, tab `permissions` | who can **open and edit** content |
| Edge Delivery roles | Admin Edit: `POST .../sites/slf-eds-demo1-da/access/admin.json` | who can **preview** (`author`) and **publish** (`publish`) |

To add an advisor: add their Adobe email to the two advisor `write` / `read` rows (step 3), then
add it to the `author` array and re-post the **whole** `access/admin.json` (POST replaces it; GET
first to keep other entries). To add a supervisor: the supervisor row in step 3 and the `publish`
array. To add an admin: `admin` array (and a `CONFIG` write row in da.live if they should edit
da.live settings). Wildcards such as `*@yourcompany.com` are supported in the Edge Delivery roles (Adobe
authentication guide); in da.live use an IMS org ID, group, or individual emails (see the access
control page). **After a person is added to a da.live group they must sign out and in.**
A user who sees a 404 in da.live lacks permission to that path or the page does not exist.

---

## 14. Optional: the newer Experience Workspace editor

Nothing above requires it. If you want to show it:

1. Open https://da.live/config#/michaelpereira78/slf-eds-demo1-da, add a sheet tab **`flags`** with
   columns `key`, `value`, and a row `ew.enabled` = `true` (Adobe: "Experience Workspace is disabled by
   default"). Adobe also has a guided starter:
   https://da.live/app/adobe-rnd/ew-extensions/tools/ew-setup/ew-setup
2. Change `editUrlPattern` (step 7) to `https://da.live/canvas#/{{org}}/{{site}}{{pathname}}` and re-post.
3. **Licensing caution:** the EW editor includes an **AI assistant** (Adobe Coworker). Your sales deck
   says AI Coworker is a future add-on that is **not licensed** for Sun Life. Adobe's documentation
   does not say what a free da.live account includes. Unless you have confirmed this with Adobe, keep
   the classic editor, or add the flag `ew.disableChat` = `true`, and do not describe the assistant as
   part of the offer.
4. Optional WYSIWYG "quick edit" needs extra code in the repo and is not needed for this demo.

---

## 15. Side-by-side demo: Google Docs vs da.live (add to the 15-minute script, 5 minutes)

(Also in `DEMO-SCRIPT.md`.) Have two browser tabs ready: Tab A the Drive-site `index` document in
Google Docs, Tab B the same page open in da.live
(https://da.live/edit#/michaelpereira78/slf-eds-demo1-da/index).

| Time | What you do | What to say |
|---|---|---|
| 0:00 | Show Tab A, the Google Doc, change Priya's title and Sidekick **Preview** | "This is how it works today: a normal Google Doc, plus the Sidekick." |
| 1:00 | Show Tab B in da.live, change the same title, click **Preview** (top right) | "Same page, edited in a browser editor built for web pages: no Google account, blocks as tables, one-click preview." |
| 2:00 | Click into the hero block and show the **Block** and **Library** menus | "Advisors add approved blocks from the library, not from memory." |
| 3:00 | As a pretend **advisor** account, click **Publish** and show it is refused | "Same rule on both: advisors author, supervisors publish. That is enforced by the platform." |
| 4:00 | As the supervisor, **Publish**; open the `.aem.live` page | "Nothing else changes: same code, same blocks, same compliance workspace." |
| 4:30 | Close | "Two ways to edit; one codebase; the choice is a configuration setting." |

**Honest trade-offs to mention if asked:** da.live needs an **Adobe ID** for every editor; the two
sites hold **separate copies** of the content; Google Docs gives comments and sharing people already know;
da.live is built for web pages (blocks, preview, versions) but is a newer tool for your people.

---

## 16. Rollback (nothing here touches the Drive site)

1. **Remove the second site's config** (Admin Edit): URL
   `https://admin.hlx.page/config/michaelpereira78/sites/slf-eds-demo1-da.json`, method **DELETE**
   (Adobe: "Permanently deletes the site level configuration"). The new preview and live hosts stop working.
   The Drive site, its Google Drive documents, its roles, its Sidekick and the GitHub repo are
   unaffected: they are separate configuration objects.
2. **Remove the content** in da.live (content browser, select the site folder, delete). Deleting
   moves items to the hidden `/.trash` folder; deleting from `/.trash` is permanent. Optionally unpublish first.
3. **Remove the permission rows** for `/slf-eds-demo1-da/...` from the da.live `permissions` tab.
4. No change to the repo is needed, since none was made.

If you only want to **pause** the experiment, stop here after step 1 or just stop using the site.
Config changes made through the config service keep **versions** (`.../sites/{site}/versions.json`),
so an earlier site config can be restored.

---

## 17. Caveats and open items

- **Separate content.** Edits in Google Docs do **not** appear on the da.live site and vice versa.
  Re-run the import (step 9) if you want to refresh the da.live copy from Drive; importing over
  existing da.live pages may overwrite edits made there (da.live keeps version history, but check
  before re-importing).
- **Same code, two content formats.** Adobe lists small differences: nested lists get an extra
  `<p>`; query indexes from da.live sheets are strongly typed (arrays stay arrays); da.live
  sheets are public by default (use a `private-` prefix for private ones) and limited to about 5,000
  rows. This demo uses none of the affected features except flat nav lists.
- **Dot folders are hidden** in the da.live content browser (`/.helix`, `/.trash`, `/.da`); enter their
  paths in the address bar.
- **Sidekick on da.live pages.** Adobe describes using the Sidekick on previewed or published pages.
  The `environments: ["edit"]` plugins of the Drive site (the Library plugin) are for Google/Word editor
  tabs and will not show on da.live; use the da.live library (step 12).
- **New sites from `/admin`** (`tools/new-site/new-site.py`, `create-site.sh`) generate a Drive-based
  site (`"type": "google"`). A da.live-based new site would use the `markup` content source shown in step 5
  and documents created in da.live instead.
- **da.live org name.** da.live org folders are plain folder names; Adobe does not describe
  claiming an org name. If `michaelpereira78` is already taken in da.live by another user,
  use another org name consistently in steps 3, 5 and 7.
- **The whole thing is a demo.** Both preview sites are viewable by anyone with the link, as before.
