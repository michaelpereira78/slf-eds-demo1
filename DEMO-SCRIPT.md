# 15-minute business demo: "Advisor websites without a developer"

All firms, people and contact details are fictional. Not affiliated with Sun Life.
Preview host used below: `https://main--slf-eds-demo1--michaelpereira78.aem.page` (shortened to **PREVIEW**).

## Before the meeting (10 minutes)

- Content is uploaded and previewed (v3 workspaces included). Confirm Sidekick JSON matches `docs/sidekick.json` ([docs/ADMIN-SETUP.md](docs/ADMIN-SETUP.md) step 3).
- Until step 4 is done, forms stay in **demo mode** (confirmation says so; the audit sheet will be empty). Until step 5 is done, advisors can still publish — mention that, or skip the “Publish greyed out” contrast.
- AEM Sidekick installed, pinned and turned on. Pop-ups allowed for the preview site.
- Open these tabs, in this order:
  1. **PREVIEW/demo**, the hub (start here)
  2. The Google Drive content folder
  3. The `index` Google Doc (Maple Ridge home)
  4. The `northstar/index` Google Doc
  5. **PREVIEW/advisor** (Advisor workspace dashboard)
  6. **PREVIEW/admin** (Supervisor console dashboard)
  7. The `forms/compliance-audit-log` Google Sheet, on the `incoming` tab (only if ADMIN-SETUP step 4 is done)
- On `/admin`, click **Reset demo** in the approval queue so it starts clean, and **Clear this
  browser** under the audit log and the Figma requests, so only your live rows show.
- Best: sign in to Sidekick with an **advisor** account in one Chrome profile and a **supervisor**
  account in another (ADMIN-SETUP step 5), so you can show Publish greyed out vs enabled.
- Optional: a phone with **PREVIEW/campaigns/retirement-checkup** open, or Chrome DevTools at 375 px.
- Rehearse once, then undo the document edits (see "Reset afterwards").

---

### 0:00 to 1:00: The promise *(Tab 1, `/demo`)*
> "Our business wants three things from advisor websites: speed, brand control and compliance.
> Everything you'll see is authored in ordinary Google Docs, runs on Adobe Edge Delivery
> Services, and no developer touches it during the demo."

Start with **Two workspaces, two roles**. Then the seven capability cards. Scroll to **Three sites, one platform**.

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
> "In production, the supervisor reviews the exact version (Sidekick's Review button can lock it
> into a review snapshot), and only the supervisor role can publish. No extra workflow product."


### 11:00 to 13:00: Two workspaces, two roles *(Tabs 5 and 6)*
- **Advisor workspace** (`/advisor`):
> "This is the advisor's home. Notice the menu is theirs: Dashboard, My website, Edit content,
> Approved content, Submissions, Help. Not the public marketing site."
- Click **Submit a change for review**. The form opens as a popup. Fill Advisor `Priya Nair`,
  page `/campaigns/retirement-checkup`, a one-line summary, tick the checks, **Submit for review**.
  Show the confirmation and reference number. Close the popup and open **Submissions**.
- In the advisor's toolbar, show **Publish unavailable**:
> "That's not a hidden button. The platform rejects a publish from an advisor account."
- **Supervisor console** (`/admin`):
> "The supervisor gets a dashboard of their own, with a different menu: Approvals, Sites, New site,
> Layouts, Figma import, Audit log, Roles."
- Open **Approvals**, **Approve** the campaign. Then open **Audit log**: both rows are there
  (Submitted, then Approved). If the sheet is connected, switch to Tab 7 and show the same rows.
> "Every submission and every decision lands in a spreadsheet Compliance can audit."
- Open **Figma import**, fill the form, **Send to MarTech Engineering**:
> "Custom designs go to the design-and-build team as a short request, with a reference number
> and a row in their intake sheet. They come back as approved sections, not a one-off site."

### 13:00 to 14:00: 1, Generate a new website *(PREVIEW/new-site, or **Create a new advisor website** on `/admin`)*
- Type `Prairie Sky Financial`, `Regina, SK`, `Sam Rivera, CFP`. Click the **Harbour** and **Slate**
  themes and watch the page change. Choose **Advisor team**, then **Create site request**.
> "The platform team runs this one command. It creates the starter documents in our brand and
> template, plus the single admin call that creates the site. Harbourview and Northstar were set
> up this way. A new advisor site is a same-day task, not a project."

### 14:00 to 15:00: Close
> "Seven capabilities, no developer in the loop, one platform we already license. SSO, hosting,
> CDN, security and approvals are part of the platform. A custom CMS would have to build every
> one of them."

---

## Optional add-on (5 minutes): Google Docs vs da.live

Only if the second site is set up ([docs/DA-LIVE-SETUP.md](docs/DA-LIVE-SETUP.md)). Open two tabs: the `index`
Google Doc of the Drive site, and the same page in da.live
(`https://da.live/edit#/michaelpereira78/slf-eds-demo1-da/index`).

1. **0:00, Google Docs today.** Change Priya's title in the Google Doc, Sidekick **Preview**.
   *"Today this is a normal Google Doc plus the Sidekick."*
2. **1:00, da.live.** Make the same change in da.live and click **Preview**.
   *"Same page, edited in a browser editor made for web pages: blocks as tables, one-click preview,
   no Google account needed."* Open `https://main--slf-eds-demo1-da--michaelpereira78.aem.page/` to show it renders with the same code.
3. **2:00, blocks.** Use the editor's **Block** and **Library** menus. *"Advisors insert approved blocks."*
4. **3:00, roles.** As the pretend advisor, click **Publish**: it is refused (403). *"Advisors author, supervisors publish, on both."*
   As the supervisor, **Publish**, then open the `.aem.live` page.
5. **4:30, close.** *"Two ways to edit, one codebase. Which one a team uses is a setting."*

Be ready to say: da.live needs an Adobe ID for every editor; the two sites hold separate copies of the
content; forms on the da.live site stay in demo mode unless the Apps Script option is connected.

---

**If something goes wrong**
- Preview shows old content: wait 5 seconds and refresh. Docs save automatically, but give it a moment.
- No compliance bar: it only shows on `.aem.page` previews (never on `.aem.live`), and only on pages
  in the review process. Pages under `/tools/` and `/fragments/` don't show it.
- Queue shows odd states from a rehearsal: click **Reset demo** on `/compliance`.
- Sidekick buttons missing: the Sidekick JSON hasn't been posted yet (ADMIN-SETUP step 3). Use the
  status bar and the `/compliance` page instead; they work without it.

- Form says **Demo mode**: the sheet isn't connected yet (ADMIN-SETUP step 4). The demo still works;
  say "in production this row lands in the Google Sheet" and show the table on the page.
- Sidekick asks you to sign in: roles are on (ADMIN-SETUP step 5). Sign in with your Google account.

**Reset afterwards:** in `index`, change Priya back to `Priya Nair, CFP`, the section style back to
`Light` and the theme back to `Forest`. Delete any pasted fragment link in `northstar/index`.
Preview both. On `/admin`, click **Reset demo** and **Clear this browser**. If the sheets are
connected, delete your rehearsal rows from the `incoming` tabs (or leave them: they are your audit trail).
