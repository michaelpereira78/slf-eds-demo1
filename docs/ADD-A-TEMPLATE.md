# Adding a new approved template (developer task, about 30 minutes)

A template is a named look for a whole page. Authors choose it with the `Template` row in the
page's Metadata table. Existing pages don't change until an author picks the new template.

1. **Code.** Create `templates/<name>/<name>.css`. Scope every rule to `body.<name>` so it can't
   affect other pages. Add `templates/<name>/<name>.js` only if the template needs behaviour
   (see `templates/campaign/campaign.js`). It must export `default function decorate(main)`.
2. **Register it** in `TEMPLATES` in `scripts/scripts.js`, e.g. `'branch-office': { js: false }`.
   Pages that name a template not on this list fall back to the default layout. This is how
   only approved templates can be used.
3. **Use theme tokens only** (`var(--navy-color)`, `var(--accent-color)`, `var(--radius)` and so on),
   never hard-coded colours, so the template works with every brand theme.
4. **Starter document.** Add a page to `tools/content.py` under `tools/sidekick/templates/<name>`,
   with a `Library Metadata` section (`type` = `template`) and a Metadata table setting `Template`,
   `Theme` and `Compliance Status` = `Draft`. Run `python3 tools/build-content.py`, upload the new
   document to `tools/sidekick/templates/` in Drive, then preview and publish it.
5. **Library entry.** Add a row (`name`, `path`) to the `helix-blocks` sheet of
   `tools/sidekick/library`, then preview and publish the sheet.
6. **Gallery.** Add a card to the `templates` page.
7. Run `npm run lint`, push to `main`, and have Brand and Compliance review an example page
   before the template is announced.

## Adding a brand theme

Add a `body.<theme>` rule to the BRAND THEMES section of `styles/styles.css` that overrides the
colour tokens (and optionally `--heading-font-family` and `--radius`). Check that text keeps
4.5:1 contrast. Authors then type the theme name in the `Theme` metadata row. Add it to
`THEMES` in `blocks/site-request/site-request.js` and `tools/new-site/new-site.py` so new sites
can choose it.
