# Advisor site demo on Adobe Edge Delivery Services

A small, responsive demo site that shows how easy it is to run an advisor team website on
[Adobe Edge Delivery Services (EDS)](https://www.aem.live/): advisors edit a Word document,
click **Preview** and **Publish** in AEM Sidekick, and the page updates in seconds.

> **Demo only. Not affiliated with Sun Life.** "Maple Ridge Wealth Partners" and every person,
> photo, phone number (555 numbers) and email address (`@example.com`) on this site are fictional.
> The avatars are generated initials placeholders, not photos of real people. No Sun Life logos
> or trademarks are used; the colours are only *a neutral forest-green and coral palette, deliberately unlike any real brand.

| | URL |
|---|---|
| Preview (after setup) | https://main--slf-eds-demo1--michaelpereira78.aem.page/ |
| Live (after setup) | https://main--slf-eds-demo1--michaelpereira78.aem.live/ |
| Advisor profile page | `/advisors/jordan-lee` on either host |

## What's in it

Two pages, modelled on the structure of a typical advisor team page:

1. **Team home page** (`/`, document `index`): hero, team profile cards, contact and office
   details, and the regulatory disclosure.
2. **Advisor profile page** (`/advisors/jordan-lee`): bigger photo, bio, services list and a
   contact card, reusing the same blocks.

### Blocks (all vanilla JS/CSS, in `blocks/<name>/<name>.js|css`)

| Block | How authors write it in Word | What it renders |
|---|---|---|
| `hero` | One cell: short eyebrow line, Heading 1, intro paragraph, **bold link** (primary button), *italic link* (secondary button). `Hero (Profile)` adds an image cell on the left. | Forest-green hero band with coral accent and buttons; profile variant shows a round portrait. |
| `team-cards` | One table row per person: image \| name, credentials \| title \| bio \| email \| phone. Making the name a link adds a "View profile" link. | Card grid: 1 column on mobile, 2 on tablet, 3 on desktop. Email and phone become `mailto:`/`tel:` links. Cells are detected defensively, so a missing phone or email does not break anything. |
| `contact` | Two-column rows: label \| value (Office, Main line, Email, Hours, Directions). `Contact (Card)` is the compact sidebar version. | Icon list with tap-to-call / tap-to-email links and a "Get directions" button. |
| `disclosure` | One cell: heading + text. | Styled regulatory note (`role="note"`). |
| `header` / `footer` | The `nav` and `footer` documents (boilerplate blocks, restyled). | Text wordmark "Advisor Demo", Home / Our team / Contact, mobile hamburger, and a visible **"Demo, not affiliated with Sun Life"** banner in the footer. |

Section styles (Section Metadata → Style): `Light` (warm grey band) and `Sidebar` (main content
on the left, the last block, e.g. the contact card, sticky on the right on desktop).

**Shared disclosure fragment.** The disclosure lives in one document, `fragments/disclosure`.
Each page only contains a link to it, and the boilerplate's fragment auto-blocking pulls it in.
In production, Compliance would own that one document: change the wording once, publish it, and
every advisor site shows the new text, with no edits to individual advisor pages.

### Quality checks (local, mobile Lighthouse, Nov 24, 2026)

| Page | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| `/` | 100 | 100 | 96* | 100 |
| `/advisors/jordan-lee` | 100 | 100 | 96* | 100 |

\*The only Best Practices miss is "missing doctype", which comes from the local `aem up` dev
server's draft rendering; pages served from aem.page / aem.live include `<!DOCTYPE html>`.

`npm run lint` passes (ESLint airbnb-base + Stylelint from the boilerplate).

## Run it locally

Requires Node 18+ (tested on Node 24).

```sh
npm install
npm start          # = npx -y @adobe/aem-cli up --html-folder drafts --html-mount / --no-open
```

Open http://localhost:3000/ and http://localhost:3000/advisors/jordan-lee.

Until the content source is connected, the pages come from `drafts/` (EDS-style `.plain.html`
markup generated from `tools/content.py`). `drafts/` and `tools/` are in `.hlxignore`, so they
are never served from aem.page / aem.live.

To regenerate the drafts and the Word documents after changing `tools/content.py`:

```sh
pip install python-docx
python3 tools/build-content.py ../slf-eds-demo1-content   # writes drafts/*.plain.html and the .docx files
```

(The Word files embed PNG avatars from `<docx_out_dir>/_avatars/<slug>.png`.)

## Make it live on aem.live: exact next steps

> Note: `fstab.yaml` is **retired** in the current boilerplate. The content source is now set in
> the site configuration (during AEM Code Sync setup, or later at https://tools.aem.live or
> https://labs.aem.live/tools/site-admin/index.html), so this repo intentionally has no `fstab.yaml`.

1. **Install AEM Code Sync on this repo.**
   Go to https://github.com/apps/aem-code-sync/installations/new, choose the
   `michaelpereira78` account, select **Only select repositories** → `slf-eds-demo1`, and click
   **Install / Save**. On the setup screen that follows, keep yourself as site admin and click
   **Finish setup**. (By default the site points to Document Authoring at https://da.live; step 3
   switches it to SharePoint or Google Drive.)
2. **Create the content folder** (pick one):
   - **Google Drive (fastest for a demo):** create a folder, e.g. `slf-eds-demo1`, and share it
     as **Editor** with `helix@adobe.com`
     ([docs](https://www.aem.live/developer/setup-google-drive)).
   - **SharePoint:** create a website root folder in a SharePoint site, e.g.
     `https://<tenant>.sharepoint.com/sites/<site>/Shared%20Documents/slf-eds-demo1`. Using a
     corporate tenant needs your SharePoint/Entra admin to register the AEM application and grant
     `Sites.Selected` on that site ([docs](https://www.aem.live/docs/setup-customer-sharepoint)).
3. **Point the site at the folder.** Open https://labs.aem.live/tools/site-admin/index.html
   (or https://tools.aem.live), sign in, open org `michaelpereira78` / site `slf-eds-demo1`, set
   **Content source** to the folder URL (Drive folder URL, or the canonical SharePoint URL above)
   and **Save**.
4. **Upload the documents** from `slf-eds-demo1-content/` keeping this structure
   (do not upload `_avatars/`):

   ```
   index.docx
   nav.docx
   footer.docx
   advisors/jordan-lee.docx
   fragments/disclosure.docx
   ```

   In Google Drive, convert each `.docx` to a native Google Doc
   (open it → **File → Save as Google Docs**) and remove the `.docx` copies; Google Drive content
   must be Google Docs. In SharePoint, upload the `.docx` files as they are.
5. **Install AEM Sidekick** from the Chrome Web Store
   (https://chromewebstore.google.com/detail/aem-sidekick/igkmdomcgoebiipaifhmpfjhbjccggml)
   and pin it.
6. **Preview and Publish each document once**: open the document, click the Sidekick icon →
   **Preview**, then on the preview page → **Publish**. Do `nav`, `footer` and
   `fragments/disclosure` too: they are separate documents with their own preview/publish.
7. Check https://main--slf-eds-demo1--michaelpereira78.aem.page/ (preview) and
   https://main--slf-eds-demo1--michaelpereira78.aem.live/ (live) on desktop and on a phone.

Code changes ship by pushing to `main` (Code Sync deploys them in seconds); content ships
separately through Sidekick.

## Presenting it

See [DEMO-SCRIPT.md](DEMO-SCRIPT.md) for a two-minute click-by-click script.

## Built on

[adobe/aem-boilerplate](https://github.com/adobe/aem-boilerplate) (Apache-2.0). See the
[developer tutorial](https://www.aem.live/developer/tutorial) and
[block collection](https://www.aem.live/developer/block-collection).
