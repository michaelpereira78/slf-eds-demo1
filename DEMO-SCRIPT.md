# Two-minute demo script: "Edit in Word, live in seconds"

**Setup before the meeting (5 minutes)**
- Tab 1: `index` document open in Word Online / Google Docs (content folder).
- Tab 2: the live site, https://main--slf-eds-demo1--michaelpereira78.aem.live/
- AEM Sidekick installed, pinned and signed in.
- Phone on the same Wi-Fi with the live URL open (or Chrome DevTools device mode at 375 px).
- Have a spare placeholder avatar ready to paste (e.g. `_avatars/daniel-whitford.png`).
- Rehearse once, then undo the edits so the demo starts clean.

---

**0:00 to 0:15: Set the scene** *(Tab 2, live site)*
> "This is a typical advisor team page: the team, their bios, how to reach them, and the
> disclosure. It's running on Edge Delivery Services, which we already license.
> No CMS screens, no developer. The 'editor' is Word."

Scroll once: hero → team cards → contact → disclosure.

**0:15 to 0:45: Edit a bio** *(Tab 1, Word)*
> "Priya just got a new designation. Here's her row in the team table."

- In the **Team Cards** table, change Priya's name cell to `Priya Nair, CFP, CLU` and add a
  sentence to her bio, e.g. *"She also leads our women and wealth workshops."*
- Click **Sidekick → Preview**.
> "That's the preview site: same look, not public yet. Compliance could review this link."

**0:45 to 1:15: Add a new team member** *(Word)*
> "We just hired someone. Adding them is adding a row."

- Put the cursor in Sofia's row → **Insert row below**, then fill in:
  image (paste the avatar) | `Alex Chen` | `Client Service Associate` |
  `Alex helps clients with account updates and paperwork.` | `alex.chen@example.com` | `403-555-0199`
- **Sidekick → Preview**. Point out the new card, styled automatically, with tap-to-call and
  tap-to-email links.

**1:15 to 1:35: Publish** *(preview tab)*
- **Sidekick → Publish**. Switch to Tab 2 and refresh.
> "That's live, globally, on Adobe's CDN. Seconds, not a release cycle."

**1:35 to 1:50: Show it on a phone**
- Hold up the phone (or switch DevTools to 375 px) and refresh: one-column cards, hamburger menu,
  tap a phone number.
> "Responsive by default, and it scores around 100 on Google Lighthouse for performance,
> accessibility and SEO."

**1:50 to 2:00: The close**
- Click Jordan's **View profile**.
> "Same blocks, a second page type. Every advisor site reuses these blocks. The disclosure at the
> bottom is a single shared document that Compliance owns: change it once, and every site updates.
> SSO, hosting, CDN, security and approvals are already part of the platform. A custom CMS has to
> build all of that."

---

**If something goes wrong**
- Preview shows old content → wait 5 to 10 seconds and refresh; make sure the document was saved.
- Pop-up blocked → allow pop-ups for the Sidekick.
- Image not showing → images must be pasted *into* the document, not linked.

**Reset after the demo**: delete Alex's row and Priya's extra sentence, then Preview and Publish.
