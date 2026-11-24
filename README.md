# Advisor web platform demo on Adobe Edge Delivery Services

A business-user demo showing that advisor websites on [Adobe Edge Delivery Services (EDS)](https://www.aem.live/)
can be created, edited, re-styled and approved without a developer. Everything is authored in Google
Docs (or Word) and runs on one shared codebase.

> **Demo only. Not affiliated with Sun Life.** Maple Ridge Wealth Partners, Harbourview Financial
> Group, Northstar Planning and every person, phone number (555) and email address (`@example.com`)
> are fictional. The colours are deliberately unlike any real brand.

**Start here:** https://main--slf-eds-demo1--michaelpereira78.aem.page/demo (after the content
upload in [docs/ADMIN-SETUP.md](docs/ADMIN-SETUP.md)).
**Presenter script:** [DEMO-SCRIPT.md](DEMO-SCRIPT.md), a 12-minute walkthrough of all seven capabilities.
**Developer handoff:** [docs/TECHNICAL-HANDOFF.md](docs/TECHNICAL-HANDOFF.md), the technical reference for developers taking
over the platform (architecture diagrams, repository map, content model, templates, theming, compliance
workflow, new-site generation, configuration, security, known issues and backlog).

## The seven capabilities and how each is built

| # | Capability | Where to see it | How it works (all standard aem.live features) |
|---|---|---|---|
| 1 | **Generate new websites** | `/new-site`, `/harbourview/`, `/northstar/` | The `site-request` block is the intake form: picking a theme re-themes the page live, and submitting gives the exact generator command. [`tools/new-site/new-site.py`](tools/new-site/new-site.py) writes the starter documents (home, nav, footer) already set to the theme and template, plus `create-site.sh`, the single [repoless](https://www.aem.live/docs/repoless) Admin API call (`PUT /config/{org}/sites/{site}.json`) that creates a new site on this same code. Creating a site needs an admin token. `--mode folder` instead creates a sub-site inside this site, which is how Harbourview and Northstar are set up (their own `Nav`/`Footer` metadata). |
| 2 | **Content changes** | any page | Edit the Google Doc, then Sidekick **Preview**, then **Publish**. |
| 3 | **Minor layout changes** | `/layouts` | Section Metadata `Style`: `Light`, `Dark`, `Accent`, `Centered`, `Narrow`, `Sidebar`, combinable (`Dark, Centered`). Block variants: `Hero (Light)`, `Hero (Centered)`, `Hero (Profile)`, `Contact (Card)`, `Callout (CTA)`, `Cards (...)`. |
| 4 | **Templates: approved set plus a way to add more** | `/templates`, `/campaigns/retirement-checkup` | `Template` metadata loads `templates/<name>/<name>.css` (and `.js`) from an **allow-list** in `scripts/scripts.js`: `advisor-team`, `solo-advisor`, `campaign` (focused header, sticky phone call to action). Starter docs live in `tools/sidekick/templates/` and appear in the Sidekick **Library** as templates. See [docs/ADD-A-TEMPLATE.md](docs/ADD-A-TEMPLATE.md). |
| 5 | **Custom branding per site** | Maple Ridge (Forest), Harbourview (Harbour), Northstar (Slate) | `Theme` metadata becomes a body class, and `body.harbour` / `body.slate` in `styles/styles.css` swap the design tokens (colours, heading font, corner radius). Blocks use tokens only, so every block follows the theme. |
| 6 | **Authoring with approved content** | `/approved-content`, Sidekick > Library > Approved content | Compliance-owned fragments under `/fragments/` (product descriptions, a call to action, the disclosure). A link on its own line embeds the fragment, and advisors can't change the wording. Each carries an approval ID, shown as a badge on preview only. The custom Sidekick Library plugin [`tools/sidekick/plugins/approved-content`](tools/sidekick/plugins/approved-content/approved-content.js) lists them from the `helix-approved-content` sheet with **Copy link**. |
| 7 | **Compliance review and approval** | status bar on every preview page, `/compliance` | Preview pages (`*.aem.page`, `*.aem.reviews`, localhost only, never the live site) show a status bar: Not yet submitted, Pending review, Changes requested or Approved. **Request review** (in the bar, or the custom Sidekick button) opens a checklist dialog. `/compliance` is the review queue with Approve / Request changes and **real** preview and publish times from the Admin status API. Queue data comes from the Compliance-owned `compliance-queue` sheet (fallback: `tools/compliance/demo-queue.json`), and clicks made during a demo are kept in the browser. In production the locking and publishing come from native [Snapshots and Reviews](https://www.aem.live/docs/snapshots-reviews) (Sidekick **Review...**: request review, then approve to publish or reject to unlock), with **Publish restricted to a Compliance role** ([roles](https://www.aem.live/docs/authentication-setup-authoring)). No Power Automate. |

## Pages (content documents)

| Path | Purpose | Template / Theme | Compliance in demo |
|---|---|---|---|
| `/demo` | presenter hub: seven capability cards | n/a / Forest | n/a |
| `/` , `/advisors/jordan-lee` | Maple Ridge team site and profile | advisor-team / Forest | Approved |
| `/harbourview/` (+ nav, footer) | second firm | advisor-team / Harbour | Pending review |
| `/northstar/` (+ nav, footer) | solo practice | solo-advisor / Slate | Changes requested |
| `/campaigns/retirement-checkup` | campaign landing page | campaign / Forest | Pending review |
| `/layouts`, `/templates`, `/approved-content`, `/new-site`, `/compliance` | capability pages | n/a / Forest | n/a |
| `/fragments/...` | approved content (5 fragments) | n/a | Approved (badge) |
| `/tools/sidekick/templates/*`, `/tools/sidekick/blocks/*`, `/tools/sidekick/library` (sheet) | Sidekick Library content | n/a | n/a |
| `/compliance-queue` (sheet) | review queue owned by Compliance | n/a | n/a |

## Repository layout

```
blocks/             hero, team-cards, contact, disclosure, callout, cards, columns, fragment,
                    site-request (intake form), compliance-queue (review queue), library-metadata (hidden)
templates/          advisor-team, solo-advisor, campaign (approved templates)
styles/styles.css   tokens, BRAND THEMES (forest default, harbour, slate), section styles
styles/compliance.css   status bar and review dialog (preview hosts only)
scripts/compliance*.js  status bar, review dialog, queue data
tools/sidekick/     library.html + approved-content plugin (served by EDS)
tools/compliance/demo-queue.json   fallback queue data
tools/content.py    single source of truth for all demo content
tools/build-content.py  writes drafts/*.plain.html (local preview) and the .docx/.xlsx to upload
tools/new-site/new-site.py   new site generator
docs/               TECHNICAL-HANDOFF.md (developer handoff), ADMIN-SETUP.md (manual steps),
                    ADD-A-TEMPLATE.md, sidekick.json
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
- **Demo approvals are kept in the browser.** Approve and Request changes on `/compliance` are saved in
  `localStorage` so the flow can be clicked through safely. The authoritative state is the
  `compliance-queue` sheet (owned by Compliance) and, in production, Snapshots and Reviews, where
  Approve actually publishes. The review dialog doesn't send email; it offers a pre-filled `mailto:` link.
- **Publish restriction is described, not switched on.** Enabling roles forces sign-in for everyone, so
  it isn't applied to the demo site (see docs/ADMIN-SETUP.md, step 4).
- **Approved content is per site.** Fragments load from the same site. A repoless sister site needs
  its own `/fragments/` copy, or a shared fragment source set up by the platform team.
- **Sidekick buttons need the configuration POST** in docs/ADMIN-SETUP.md, step 3 (a repo file can't do
  it on a configuration-service site). Until then, use the status bar and the `/compliance` page, which
  work without Sidekick changes.

Built on [adobe/aem-boilerplate](https://github.com/adobe/aem-boilerplate) (Apache-2.0).
