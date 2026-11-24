# 12-minute business demo: "Advisor websites without a developer"

All firms, people and contact details are fictional. Not affiliated with Sun Life.
Preview host used below: `https://main--slf-eds-demo1--michaelpereira78.aem.page` (shortened to **PREVIEW**).

## Before the meeting (10 minutes)

- One-time setup in [docs/ADMIN-SETUP.md](docs/ADMIN-SETUP.md) is done: content uploaded, previewed, Sidekick JSON posted.
- AEM Sidekick installed, pinned and turned on. Pop-ups allowed for the preview site.
- Open these tabs, in this order:
  1. **PREVIEW/demo**, the hub (start here)
  2. The Google Drive content folder
  3. The `index` Google Doc (Maple Ridge home)
  4. The `northstar/index` Google Doc
  5. **PREVIEW/compliance**
- On `/compliance`, click **Reset demo** so the queue starts clean.
- Optional: a phone with **PREVIEW/campaigns/retirement-checkup** open, or Chrome DevTools at 375 px.
- Rehearse once, then undo the document edits (see "Reset afterwards").

---

### 0:00 to 1:00: The promise *(Tab 1, `/demo`)*
> "Our business wants three things from advisor websites: speed, brand control and compliance.
> Everything you'll see is authored in ordinary Google Docs, runs on Adobe Edge Delivery
> Services, and no developer touches it during the demo."

Point at the seven cards: "We'll go through each one." Scroll to **Three sites, one platform**.

### 1:00 to 3:00: 2, Make a content change *(Tab 3, `index` doc)*
> "Priya just earned a new designation."
- In the **Team Cards** table, change `Priya Nair, CFP` to `Priya Nair, CFP, CLU`.
- **Sidekick > Preview.** The preview opens with the change in about 3 seconds.
> "That's the preview site. Not public yet. Notice the bar at the bottom: Compliance has already
> approved the version that's live, and this edit hasn't been reviewed. We'll come back to that."

### 3:00 to 4:30: 3, Minor layout change *(same doc)*
- Scroll to the **Section Metadata** table under Our team. Change `Light` to `Dark`. **Preview.**
> "One word changes the layout. No ticket, no release."
- Open **PREVIEW/layouts** to show every option. Change the word back to `Light`.

### 4:30 to 6:00: 5, Brand themes *(Tab 1, hub > Three sites)*
- Open **Harbourview**, then **Northstar**.
> "Same platform, same blocks, three brands: green and coral, indigo and teal, charcoal and amber
> with serif headings. Each site's brand is one line in its metadata: `Theme: Harbour`."
- Optional live moment: in the `index` doc's **Metadata** table, change `Theme` from `Forest` to
  `Slate`, Preview, show it, then change it back.

### 6:00 to 7:30: 4, Approved templates *(PREVIEW/templates)*
> "Every page starts from a template that Brand and Compliance already approved."
- Click **See an example** for **Campaign**. Point out the focused header and the single call to
  action. On a phone (or 375 px), scroll and show the sticky **Book my check-up** button.
- Back in Drive: open `tools > sidekick > templates`, right-click `campaign`, choose **Make a copy**.
> "That's how an advisor starts a new campaign page. New templates are added by the platform team
> once and become available to every site; existing pages don't change."
- If Sidekick is configured: in any doc, **Sidekick > Library > Blocks** shows the templates and blocks.

### 7:30 to 9:00: 6, Approved content *(PREVIEW/approved-content, then Tab 4)*
> "Product descriptions and disclosures are written once by Compliance and reused everywhere.
> Advisors can place them but can't reword them."
- Show the approval badges (for example `AC-2026-022`).
- In the `northstar/index` doc: **Sidekick > Library > Approved content > Copy link** on
  *Insurance protection*. Paste it on its own line, then **Preview**.
  (No Sidekick? Copy the "Link to paste" URL from the approved content page instead.)
> "When Compliance updates this wording, every site picks it up on the next publish."

### 9:00 to 11:00: 7, Compliance review and approval *(Northstar preview, then Tab 5)*
- On the Northstar preview, the bar is red: **Changes requested**, with the reviewer's note.
- Click **Request review** (or Sidekick **Request compliance review**). Fill in "What changed",
  tick the three checks, then **Submit for review**. The bar turns amber: **Pending review**.
- Open **Review queue** (`/compliance`):
> "This is Compliance's view: pending items, who submitted them, the preview link, and the real
> times each page was last previewed and published."
- On Northstar, click **Approve**. Go back to the Northstar preview: the bar is green, **Approved**.
> "In production, Sidekick's Review button puts the exact version into a locked review snapshot.
> Compliance approves it and that approval publishes it, and only the Compliance role has
> Publish. No Power Automate, no extra workflow product."

### 11:00 to 12:00: 1, Generate a new website *(PREVIEW/new-site)*
- Type `Prairie Sky Financial`, `Regina, SK`, `Sam Rivera, CFP`. Click the **Harbour** and **Slate**
  themes and watch the page change. Choose **Advisor team**, then **Create site request**.
> "The platform team runs this one command. It creates the starter documents in our brand and
> template, plus the single admin call that creates the site. Harbourview and Northstar were set
> up this way. A new advisor site is a same-day task, not a project."

### Close
> "Seven capabilities, no developer in the loop, one platform we already license. SSO, hosting,
> CDN, security and approvals are part of the platform. A custom CMS would have to build every
> one of them."

---

**If something goes wrong**
- Preview shows old content: wait 5 seconds and refresh. Docs save automatically, but give it a moment.
- No compliance bar: it only shows on `.aem.page` previews (never on `.aem.live`), and only on pages
  in the review process. Pages under `/tools/` and `/fragments/` don't show it.
- Queue shows odd states from a rehearsal: click **Reset demo** on `/compliance`.
- Sidekick buttons missing: the Sidekick JSON hasn't been posted yet (ADMIN-SETUP step 3). Use the
  status bar and the `/compliance` page instead; they work without it.

**Reset afterwards:** in `index`, change Priya back to `Priya Nair, CFP`, the section style back to
`Light` and the theme back to `Forest`. Delete any pasted fragment link in `northstar/index`.
Preview both. Click **Reset demo** on `/compliance`.
