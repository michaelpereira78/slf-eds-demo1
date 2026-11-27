# `/michael-pereira/`: internal demo replica of a Sun Life advisor site

**Purpose.** For an internal demo, show that an advisor site that looks exactly like today's
advisor.sunlife.ca sites can run on Edge Delivery Services and be edited in **Google Docs** (this site,
`slf-eds-demo1`) or in **da.live** (the second site, `slf-eds-demo1-da`, see
[DA-LIVE-SETUP.md](DA-LIVE-SETUP.md)).

- Reference page: https://advisor.sunlife.ca/ben.aldridge/ (and its About, Products and services,
  Stay informed, Resources and Connect pages). Captured 26 Nov 2026.
- Replica: `/michael-pereira/` with the same six pages, personalised for **Michael Pereira**,
  Cambridge, Ontario.
- Requested by Michael on 26 Nov 2026. This overrides the "must not look like Sun Life" rule **for
  this one site only**. The other sample sites keep their fictional brands.

## Keep it internal

- Contact details are placeholders: `(519) 555-0100`, `michael.pereira@example.com`,
  `100 Example Street, Suite 200, Cambridge, ON N1R 0A0`. "Book an appointment" goes to the
  Connect page form, not Sun Life's booking tool.
- The headshot is a grey placeholder. Replace `images/photos/mp-headshot-placeholder.jpg` (or the
  picture in the Google Doc) with a real headshot if wanted.
- No photo or text of Ben Aldridge is used. The page copy follows the same structure, rewritten for
  Michael. The bio, the assistant ("Jamie Silva") and the community paragraph are **fictional demo
  text**; edit them in the docs before showing them to anyone who knows Michael.
- Sun Life fonts (`Sun Life New Text`, `Sun Life New Display`) and the Sun Life, CIPF and CIRO logos
  are **hotlinked** from `advisor.sunlife.ca` (public files, served with `Access-Control-Allow-Origin: *`).
  Nothing proprietary is committed. If advisor.sunlife.ca moves those files, the page falls back to
  Helvetica/Arial and a "Sunlife" text wordmark, and the regulator logos are hidden.
- The contact form is **demo only**: it validates and shows a confirmation, and nothing is sent.
- The footer adds one line: "Internal demo replica built on AEM Edge Delivery Services. Not a live
  advisor site".

## How it is built

| Piece | Where | Notes |
|---|---|---|
| Template | `templates/sunlife-advisor/` | `Template: sunlife-advisor` in the page Metadata. CSS sets the Sun Life tokens (text `#202223`, links `#00588B`, navy `#004570`, teal `#184A58`, yellow `#FFCB05`, cream `#FFF8E0`), the 1128 px column, 56 px section spacing, the two-row header (utility bar plus nav) and the white footer. JS swaps the nav brand for the logo, highlights only the current page, adds the regulator logos and the link icons (arrow-in-circle for internal "more" links, box-arrow for external links). |
| Advisor Banner | `blocks/advisor-banner/` | `[picture] [H1, text, bold link = yellow button]`. 520 px tall with a button, 400 px without one (subpages), cream 368 px panel on the left; on mobile the photo stacks above the panel. |
| Advisor Profile | `blocks/advisor-profile/` | `[headshot] [H2 name, lines, link, bullet list of Facebook/Instagram/LinkedIn links]`. Social links become icons. |
| Media Text | `blocks/media-text/` | Rows of `[picture] [text]`. `(right)` puts the picture on the right, `(video)` adds a play button (also automatic when the picture's alt text starts with `Video:`). A row with only a picture keeps its column. |
| Info Cards | `blocks/info-cards/` | Rows of `[picture] [text]`, three per row, bordered. `(news)` for social posts (keeps "- item" lines tight), `(plain)` borderless columns with dividers (Services). |
| Office Map | `blocks/office-map/` | `[place name] [office details]`. The place name becomes a keyless Google Maps embed. |
| Lead Form | `blocks/lead-form/` | `[H2, intro]`. The fields are built in code to match the original form. Demo mode only. |
| CTA Box | `blocks/cta-box/` | `[picture] [H2, text, link]` on cream ("Have questions?"). |
| Section styles | template CSS | `Style: intro` (758 px reading width), `Style: header-link` (heading with a link on the right). |
| Shared helper | `scripts/advisor-ui.js` | Video poster play button. |
| Content source | `tools/michael-pereira/content_mp.py` | One Python file; `build.py` renders it to `drafts/michael-pereira/*.plain.html` (local preview), Word files for Drive, and da.live HTML. |
| Images | `images/photos/hero-mp-*.jpg`, `mp-*.jpg` | Built by `tools/michael-pereira/make-images.py`. Credits: [PHOTO-CREDITS.md](PHOTO-CREDITS.md). |

Nothing global changed: `scripts/scripts.js` only gains `'sunlife-advisor': { js: true }` in
`TEMPLATES`. `/`, `/harbourview/`, `/northstar/`, `/advisor`, `/admin` were re-checked locally with
no console errors.

## Rebuild

```sh
python3 tools/michael-pereira/make-images.py          # only if images change
python3 tools/michael-pereira/build.py ../slf-eds-demo1-michael-pereira-content
npm start                                              # http://localhost:3000/michael-pereira/
```

## Version 1: Google Docs (site `slf-eds-demo1`)

1. In the site's Google Drive root folder (the one that already holds `index`, `advisor`, `admin`,
   `harbourview`, ...), create a **new folder named `michael-pereira`**.
2. Make sure **Settings > Convert uploads to Google Docs editor format** is on (Drive, gear icon).
3. Upload the 8 files from `michael-pereira/` in the content zip into that folder. They become Google
   Docs named exactly: `index`, `about`, `products-services`, `stay-informed`, `resources`, `connect`,
   `nav`, `footer`. The folder is new, so nothing is duplicated. If you upload again later, **delete
   the old doc first** (or edit it in place); a same-named upload creates a second doc.
4. Preview in this order with the Sidekick: `nav`, `footer`, then `index`, `about`,
   `products-services`, `stay-informed`, `resources`, `connect`.
5. Open https://main--slf-eds-demo1--michaelpereira78.aem.page/michael-pereira/ and click through
   the six nav items. Publish only if you want it on `aem.live` (it is meant to stay internal; preview
   is enough for the demo).

## Version 2: da.live (site `slf-eds-demo1-da`)

Do [DA-LIVE-SETUP.md](DA-LIVE-SETUP.md) steps 1 to 7 first (permissions, site config, roles,
Sidekick). Then either:

- **A. Import from the Drive version (recommended, once Version 1 is previewed).** The 8 URLs are now in
  [`da-import-urls.txt`](da-import-urls.txt) (lines containing `/michael-pereira`). Paste just those
  into https://da.live/apps/import with destination `michaelpereira78/slf-eds-demo1-da`.
- **B. Upload the ready-made HTML (no Drive needed).** The content zip has `da/michael-pereira/*.html`
  in DA's format (`<body><header></header><main>…</main><footer></footer></body>`, blocks as
  `<div class="block-name">` tables). In da.live, open `https://da.live/#/michaelpereira78/slf-eds-demo1-da`,
  create a folder `michael-pereira`, and drag the 8 `.html` files into it. Images point at the copies
  in this repository (`https://main--slf-eds-demo1-da--michaelpereira78.aem.page/images/photos/...`),
  so no image upload is needed. *Drag-and-drop upload of `.html` files was not tested here; if da.live
  does not accept it, use option A or paste each page.*

Then preview `nav`, `footer` and the six pages in da.live (or with https://da.live/apps/bulk) and
check https://main--slf-eds-demo1-da--michaelpereira78.aem.page/michael-pereira/.

Internal links in the documents are paths (`/michael-pereira/about`), so they work on both sites
without a find-and-replace.

## What still differs from the reference

- **Photos.** Licence-free Pexels photos replace Sun Life's campaign photography; the
  "Stay informed" post images are generated look-alikes, not Sun Life's social graphics.
- **Videos.** The original embeds two advisor videos; the replica shows posters with a play button
  that explains it is a placeholder.
- **Copy.** Same headings and structure; the bio, mission and community text are rewritten for
  Michael and are fictional. Products and Resources pages are shortened (3 health, 3 life products,
  3 calculators, 1 partner card instead of 13 products and 2 named partners). "Stay informed" has
  5 posts.
- **Form.** Same fields and wording; demo mode (no submission, no reCAPTCHA).
- **Mobile.** Matches the original's stacking (hamburger left, logo centred, photo above the cream
  panel). "See more articles" stays next to the heading on mobile instead of moving below the cards.
- **Footer.** One extra small line marks it as an internal demo replica.
