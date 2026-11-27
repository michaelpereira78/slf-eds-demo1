# Advisor web platform demo on Adobe Edge Delivery Services

A business-user demo showing that advisor websites on [Adobe Edge Delivery Services (EDS)](https://www.aem.live/)
can be created, edited, re-styled and approved without a developer. Everything is authored in Google
Docs (or Word) and runs on one shared codebase.

> **Demo only. Not affiliated with Sun Life.** Maple Ridge Wealth Partners, Harbourview Financial
> Group, Northstar Planning and every person, phone number (555) and email address (`@example.com`)
> are fictional. The colours are deliberately unlike any real brand.

> **Exception: `/michael-pereira/` is an internal demo replica of a real Sun Life advisor site.**
> At Michael's request (26 Nov 2026) it reproduces the layout of
> https://advisor.sunlife.ca/ben.aldridge/ with Michael Pereira's name, using the `sunlife-advisor`
> template. The Sun Life fonts and the Sun Life, CIPF and CIRO logos are **hotlinked** from
> advisor.sunlife.ca (not copied into this repo). The headshot is a grey placeholder, and the phone,
> email and address are placeholders (555 number, `@example.com`, "Example Street"). Keep it internal:
> do not publish it to a public audience or present it as a live advisor site. See
> [docs/MICHAEL-PEREIRA-REPLICA.md](docs/MICHAEL-PEREIRA-REPLICA.md).

**Start here:** https://main--slf-eds-demo1--michaelpereira78.aem.page/demo (after the content
upload in [docs/ADMIN-SETUP.md](docs/ADMIN-SETUP.md)).
**Presenter script:** [DEMO-SCRIPT.md](DEMO-SCRIPT.md), a 15-minute walkthrough of the seven capabilities plus the Advisor workspace and Supervisor console.
**Optional second editor (da.live):** [docs/DA-LIVE-SETUP.md](docs/DA-LIVE-SETUP.md), step by step: add a second repoless site `slf-eds-demo1-da` on this same code with content authored in da.live (Document Authoring / Experience Workspace) instead of Google Drive. The Drive site is not changed.
**Developer handoff:** [docs/TECHNICAL-HANDOFF.md](docs/TECHNICAL-HANDOFF.md), the technical reference for developers taking
over the platform (architecture diagrams, repository map, workspaces, forms, audit log, roles, content model, templates, theming, compliance
workflow, new-site generation, configuration, security, known issues and backlog).

## The seven capabilities and how each is built

| # | Capability | Where to see it | How it works (all standard aem.live features) |
|---|---|---|---|
| 1 | **Generate new websites** | `/new-site`, `/harbourview/`, `/northstar/` | The `site-request` block is the intake form: picking a theme re-themes the page live, and submitting gives the exact generator command. [`tools/new-site/new-site.py`](tools/new-site/new-site.py) writes the starter documents (home, nav, footer) already set to the theme and template, plus `create-site.sh`, the single [repoless](https://www.aem.live/docs/repoless) Admin API call (`PUT /config/{org}/sites/{site}.json`) that creates a new site on this same code. Creating a site needs an admin token. `--mode folder` instead creates a sub-site inside this site, which is how Harbourview and Northstar are set up (their own `Nav`/`Footer` metadata). |
| 2 | **Content changes** | any page; `/advisor` | Edit the Google Doc, then Sidekick **Preview**. Submit for review from the Advisor workspace (or the preview status bar). **Publish** is intended for supervisors only, once `docs/access-admin.json` is posted. |
| 3 | **Minor layout changes** | `/layouts` | Section Metadata `Style`: `Light`, `Dark`, `Accent`, `Centered`, `Narrow`, `Sidebar`, combinable (`Dark, Centered`). Block variants: `Hero (Light)`, `Hero (Centered)`, `Hero (Profile)`, `Contact (Card)`, `Callout (CTA)`, `Cards (...)`. |
| 4 | **Templates: approved set plus a way to add more** | `/templates`, `/campaigns/retirement-checkup` | `Template` metadata loads `templates/<name>/<name>.css` (and `.js`) from an **allow-list** in `scripts/scripts.js`: `advisor-team`, `solo-advisor`, `campaign` (focused header, sticky phone call to action), plus `workspace` for the Advisor and Supervisor apps (not a marketing template). Starter docs live in `tools/sidekick/templates/` and appear in the Sidekick **Library** as templates. See [docs/ADD-A-TEMPLATE.md](docs/ADD-A-TEMPLATE.md). |
| 5 | **Custom branding per site** | Maple Ridge (Forest), Harbourview (Harbour), Northstar (Slate) | `Theme` metadata becomes a body class, and `body.harbour` / `body.slate` in `styles/styles.css` swap the design tokens (colours, heading font, corner radius). Blocks use tokens only, so every block follows the theme. |
| 6 | **Authoring with approved content** | `/approved-content`, Sidekick > Library > Approved content | Compliance-owned fragments under `/fragments/` (product descriptions, a call to action, the disclosure). A link on its own line embeds the fragment, and advisors can't change the wording. Each carries an approval ID, shown as a badge on preview only. The custom Sidekick Library plugin [`tools/sidekick/plugins/approved-content`](tools/sidekick/plugins/approved-content/approved-content.js) lists them from the `helix-approved-content` sheet with **Copy link**. |
| 7 | **Compliance review and approval** | status bar on preview pages; `/advisor` and `/admin` workspaces; `/compliance` | Advisors submit from the Advisor workspace (full page or a `?modal` popup) or the preview status bar. Supervisors review in `/admin` and `/admin/approvals` (`/compliance` still works). Queue data comes from the `compliance-queue` sheet (fallback: `tools/compliance/demo-queue.json`). Decisions write to the compliance audit log when forms are connected; otherwise they stay in the presenter’s browser (demo mode). In production, locking and publishing come from native [Snapshots and Reviews](https://www.aem.live/docs/snapshots-reviews), with **Publish restricted to the `publish` role** ([roles](https://www.aem.live/docs/authentication-setup-authoring)) once `docs/access-admin.json` is posted. No Power Automate. |

## Pages (content documents)

| Path | Purpose | Template / Theme | Compliance in demo |
|---|---|---|---|
| `/demo` | presenter hub: seven capability cards, links to both workspaces | n/a / Forest | n/a |
| `/advisor` and `/advisor/*` | Advisor workspace dashboard and subpages (edit, add a page, approved content, submissions, help; review and layout forms also open as popups) | workspace / Forest | n/a |
| `/admin` and `/admin/*` | Supervisor console dashboard and subpages (approvals, sites, new site, layouts, Figma import, audit log, roles) | workspace / Forest | n/a |
| `/` , `/advisors/jordan-lee` | Maple Ridge team site and profile | advisor-team / Forest | Approved |
| `/harbourview/` (+ nav, footer) | second firm | advisor-team / Harbour | Pending review |
| `/northstar/` (+ nav, footer) | solo practice | solo-advisor / Slate | Changes requested |
| `/campaigns/retirement-checkup` | campaign landing page | campaign / Forest | Pending review |
| `/michael-pereira/` (+ about, products-services, stay-informed, resources, connect, nav, footer) | internal demo replica of a Sun Life advisor site (advisor.sunlife.ca layout) for Michael Pereira | sunlife-advisor / n/a | Pending review |
| `/layouts`, `/templates`, `/approved-content`, `/new-site`, `/compliance` | capability pages | n/a / Forest | n/a |
| `/fragments/...` | approved content (5 fragments) | n/a | Approved (badge) |
| `/tools/sidekick/templates/*`, `/tools/sidekick/blocks/*`, `/tools/sidekick/library` (sheet) | Sidekick Library content | n/a | n/a |
| `/compliance-queue` (sheet) | review queue owned by Compliance | n/a | n/a |
| `/forms/compliance-audit-log`, `/forms/figma-import-requests`, `/forms/layout-change-requests` (sheets) | form submissions (`incoming` tab) and the compliance audit log | n/a | n/a |

Roles (advisors author, supervisors publish): `docs/access-admin.json`. Form logging and exact Drive
steps: `docs/ADMIN-SETUP.md` steps 4 to 6. Photo credits: `docs/PHOTO-CREDITS.md`.

## Repository layout

```
blocks/             hero, team-cards, contact, disclosure, callout, cards, columns, fragment,
                    site-request (intake form), compliance-queue (review queue),
                    request-form (review / layout / Figma intake), stats, testimonials, banner,
                    library-metadata (hidden)
templates/          advisor-team, solo-advisor, campaign (approved templates);
                    workspace (Advisor and Supervisor app chrome);
                    sunlife-advisor (internal replica of the advisor.sunlife.ca layout)
blocks/ (replica)   advisor-banner, advisor-profile, media-text, info-cards, office-map,
                    lead-form, cta-box (used by the sunlife-advisor template)
tools/michael-pereira/   content_mp.py (replica content), build.py (drafts, .docx, da.live HTML),
                    make-images.py (crops and generated card images)
styles/styles.css   tokens, BRAND THEMES (forest default, harbour, slate), section styles
styles/compliance.css   status bar and review dialog (preview hosts only)
scripts/compliance*.js  status bar, review dialog, queue data
scripts/forms.js, audit-log.js   form posting, logAudit, audit log UI
tools/sidekick/     library.html + approved-content plugin (served by EDS)
tools/compliance/demo-queue.json   fallback queue data
tools/content.py    single source of truth for all demo content
tools/build-content.py  writes drafts/*.plain.html (local preview) and the .docx/.xlsx to upload
tools/new-site/new-site.py   new site generator
docs/               TECHNICAL-HANDOFF.md (developer handoff), ADMIN-SETUP.md (manual steps),
                    ADD-A-TEMPLATE.md, sidekick.json, access-admin.json, PHOTO-CREDITS.md,
                    apps-script/form-to-sheet.gs
```

`drafts/`, `docs/`, `tools/*.py` and `tools/new-site/` are listed in `.hlxignore`, so they are
never served. `tools/sidekick/` and `tools/compliance/` **are** served, because Sidekick needs them.

## Run it locally

```sh
npm install
npm start                       # http://localhost:3000/demo  (serves drafts/ as the content)
npm run lint
pip install python-docx openpyxl
python3 tools/build-content.py ../slf-eds-demo1-content   # regenerate drafts + Word/Excel files
npm run new-site -- --firm "Prairie Sky Financial" --city "Regina, SK" --lead "Sam Rivera, CFP" --theme harbour --template advisor-team
```

## Quality (local, Lighthouse mobile, Nov 24, 2026)

Performance 97 to 100 and Accessibility 100 on every page tested (`/`, `/harbourview/`, `/northstar/`,
`/campaigns/retirement-checkup`, `/demo`, `/compliance`, `/new-site`, `/templates`,
`/approved-content`, `/advisors/jordan-lee`; `/layouts` scores 97 because of a small font-swap shift).
Best Practices is 96 locally ("missing doctype" comes from the dev server's draft rendering).
SEO is lower locally only because the dev server proxies the preview host's `robots.txt`, which
blocks crawling on every `*.aem.page` site. `npm run lint` passes.

## Limitations (honest list)

- **Site creation needs an admin.** The intake form doesn't create anything. It produces the request
  and the generator command. Creating a repoless site is one Admin API call that needs an AEM admin
  token (or Site Admin at tools.aem.live).
- **Forms and demo approvals stay in the browser until sheets are connected.** Until ADMIN-SETUP
  step 4 is done, submit / approve / layout / Figma rows are saved in `localStorage` (the confirmation
  says **Demo mode**). The authoritative operational log is the `forms/` sheets once connected; the
  authoritative publish trail is the Admin API log. In production, Snapshots and Reviews are where
  Approve actually publishes. The review dialog doesn't send email; it offers a pre-filled `mailto:` link.
- **Publish restriction is ready, not yet posted.** `docs/access-admin.json` maps advisors to
  `author` and supervisors to `publish`. It is not posted yet, so advisors can still publish. Posting
  it (ADMIN-SETUP step 5) forces sign-in and is the intended demo setup. GET the existing config first
  and keep the owner account in `admin`.
- **Approved content is per site.** Fragments load from the same site. A repoless sister site needs
  its own `/fragments/` copy, or a shared fragment source set up by the platform team.
- **Sidekick buttons need the configuration POST** in docs/ADMIN-SETUP.md, step 3 (a repo file can't do
  it on a configuration-service site). Confirm the posted config matches the current
  `docs/sidekick.json` (workspace links and Publish confirmation).

Built on [adobe/aem-boilerplate](https://github.com/adobe/aem-boilerplate) (Apache-2.0).
