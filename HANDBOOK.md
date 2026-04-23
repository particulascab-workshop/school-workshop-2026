# Site Management Handbook
### QFT Bariloche 2026 — For the Non-Expert Editor

This guide explains how to do every common task for the conference website.
No programming knowledge is required. You just need a GitHub account and the
access rights to the repository.

**Live website:** https://particulascab-workshop.github.io/school-workshop-2026/

---

## Table of Contents

1. [How the site works (big picture)](#1-how-the-site-works-big-picture)
2. [How to edit text on the page](#2-how-to-edit-text-on-the-page)
3. [How to add or change a speaker photo](#3-how-to-add-or-change-a-speaker-photo)
4. [How to add or edit a lecturer card](#4-how-to-add-or-edit-a-lecturer-card)
5. [How to update the participants list](#5-how-to-update-the-participants-list)
6. [How to update the workshop speakers list](#6-how-to-update-the-workshop-speakers-list)
7. [How to open or close registration](#7-how-to-open-or-close-registration)
8. [How to update the program schedule](#8-how-to-update-the-program-schedule)
9. [How to trigger a manual sync](#9-how-to-trigger-a-manual-sync)
10. [Quick reference: where is each piece of text?](#10-quick-reference-where-is-each-piece-of-text)

---

## 1. How the site works (big picture)

The entire website lives in **one file: `index.html`**.
When you save a change to that file and push it to GitHub, the live website
updates automatically within a minute or two (this is called GitHub Pages).

There are also two helper Python scripts (`sync_participants.py` and
`sync_speakers.py`) that can automatically pull names from a Google Sheet and
inject them into `index.html`. Those run on a schedule every day via
**GitHub Actions** (the automation system built into GitHub).

```
Google Sheet (participants / speakers)
        │  (daily automatic pull)
        ▼
  GitHub Actions  ──►  updates index.html  ──►  live website
```

You almost never need to touch the Python scripts or the workflows. The two
things you will actually edit are:

- **`index.html`** — for any text, layout, or speaker changes.
- **The Google Sheet** — for participants and workshop-speakers data.

---

## 2. How to edit text on the page

### Step-by-step

1. Go to the repository on GitHub:
   https://github.com/particulascab-workshop/school-workshop-2026

2. Click on **`index.html`** in the file list.

3. Click the **pencil icon** (✏ Edit this file) at the top-right of the file view.

4. Use **Ctrl+F** (or **Cmd+F** on Mac) in your browser to search for the
   exact text you want to change.

5. Edit the text directly in the browser editor.

6. Scroll to the bottom of the page. Under **"Commit changes"**, write a short
   description of what you changed (e.g. *"Update registration deadline"*).

7. Make sure **"Commit directly to the `main` branch"** is selected, then
   click **Commit changes**.

8. Wait about 60–90 seconds, then reload the live website to see your update.

> **Tip:** If you are unsure what you are changing, look for the text in the
> page source and only modify the human-readable words — never delete the
> surrounding `<` and `>` tags or the `"` quotes inside them.

---

## 3. How to add or change a speaker photo

Photos are stored as plain image files (`.jpg` or `.jpeg`) in the root of the
repository.

### Uploading a new photo

1. In the repository, click **Add file → Upload files**.
2. Drag in the new photo (JPEG or PNG). Use a simple filename with no spaces,
   e.g. `lastname.jpg`.
3. Click **Commit changes**.

### Linking the photo to a speaker card

Open `index.html` for editing (see Section 2). Find the speaker's card — for
example:

```html
<img class="speaker-photo" src="fewster.jpg" alt="Christopher J. Fewster" ...
```

Change `src="fewster.jpg"` to the filename of the new image you uploaded.

### What if there is no photo yet?

The code already handles missing photos gracefully: if the image file is not
found, it shows a circle with the speaker's initials instead. So it is safe
to have a card without a photo while you wait for one.

---

## 4. How to add or edit a lecturer card

The "Invited Lecturers" cards are in `index.html`, inside the
`<!-- Speakers Section -->` block (around line 643).

### Adding a new lecturer

Find an existing card (they all look like this) and copy it:

```html
<!-- Christopher Fewster -->
<div class="speaker-card">
  <img class="speaker-photo" src="fewster.jpg" alt="Christopher J. Fewster"
       onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
  <div class="speaker-photo-placeholder" style="display:none;">CF</div>
  <div class="speaker-info">
    <span class="speaker-name">
      <a href="https://..." target="_blank">Christopher J. Fewster</a>
    </span>
    <span class="speaker-affil">University of York, Dept. of Mathematics</span>
  </div>
</div>
```

Paste the copy right below the last `</div>` of the existing card, then
replace:

| Placeholder | What to put |
|---|---|
| `fewster.jpg` | The filename of the new photo (see Section 3) |
| `"Christopher J. Fewster"` (in `alt=`) | The person's full name |
| `CF` | The person's initials (shown if photo is missing) |
| `https://...` | Their personal or institutional webpage |
| `Christopher J. Fewster` (link text) | Their full name |
| `University of York, Dept. of Mathematics` | Their affiliation |

### Editing an existing lecturer

Find the card using Ctrl+F on their name, then change only the fields you
need to update.

### Removing a lecturer

Delete everything from `<!-- Their Name -->` down to and including the closing
`</div>` of the card. Be careful to delete complete blocks — if the page
breaks, it is usually because a `<div>` was left open or deleted by mistake.

---

## 5. How to update the participants list

The participants list is maintained via a **Google Sheet**. You do **not**
need to edit `index.html` manually.

### Normal workflow

1. Add (or remove) rows in the Google Sheet that is connected to this site.
   The sheet must have two columns with these exact headers: `name` and
   `affiliation`.

2. The site will update automatically the next morning (the sync runs daily
   at **08:00 UTC**).

3. If you want to update immediately (without waiting until tomorrow), see
   [Section 9 — How to trigger a manual sync](#9-how-to-trigger-a-manual-sync).

### What the sync does

The script reads every row from the sheet, sorts the people alphabetically by
last name, and replaces the `var participants = [...]` block in `index.html`
with the new list. It then commits the change automatically.

### Troubleshooting

- If the list is not updating, make sure the Google Sheet is still published
  as CSV. In Google Sheets: **File → Share → Publish to web → Sheet1 → CSV → Publish**.
- The URL of that published CSV must match the secret `SHEET_CSV_URL` stored
  in the repository's GitHub Secrets. If someone changed the sheet's sharing
  settings, ask a repository admin to update the secret.

---

## 6. How to update the workshop speakers list

This works exactly the same as the participants list (Section 5), but uses a
**separate** Google Sheet and a separate secret (`SPEAKERS_CSV_URL`).

- The sync runs daily at **09:00 UTC** (one hour after participants).
- The sheet must also have columns `name` and `affiliation`.
- For an immediate update, use the manual trigger described in Section 9,
  but choose the **"Sync Speakers List"** workflow instead.

The workshop speakers appear as a compact inline list (not cards) in the
"Confirmed Workshop Speakers" subsection of the Speakers section.

---

## 7. How to open or close registration

There are two places in `index.html` that control the registration state.

### The navigation bar button (top-right of every page)

Search for:

```html
<a href="#" target="_blank" class="btn-nav-reg">Register (Closed)</a>
```

- To **open** registration: replace `href="#"` with the Google Form URL, and
  change the button text to something like `Register Now`.
- To **close** registration: set `href="#"` back, and change the text to
  `Registration Closed` (or `Register (Closed)`).

### The big call-to-action box in the Registration section

Search for:

```html
<div class="reg-cta-box">
    <h3>Registration is Closed</h3>
    ...
    <a href="#" target="_blank" class="btn-main">Registration Closed</a>
</div>
```

- Change the `<h3>` heading text (e.g. to `Register Now`).
- Replace `href="#"` with the Google Form URL.
- Change the button text.

> **Important:** remember to revert both places when you close registration
> again after the deadline passes.

---

## 8. How to update the program schedule

The program is split into two tabs: **Week I (School)** and
**Week II (Workshop)**. Both are in `index.html` inside the
`<!-- Program Section -->` block (around line 729).

### Structure of a schedule row

```html
<div class="schedule-row">
    <div class="time-slot">May 18 (Mon)</div>
    <div>
        <div class="session-title">Arrival &amp; Registration</div>
        <div class="session-desc">Welcome reception at IB Campus.</div>
    </div>
</div>
```

- `time-slot`: the date or time shown on the left in gold.
- `session-title`: the bold session name.
- `session-desc`: the smaller italic description (optional — you can omit this
  whole `<div>` if there is nothing to add).

### Adding a row

Copy one existing `<div class="schedule-row">...</div>` block and paste it
right before the closing `</div>` of the relevant week container
(`id="week1"` or `id="week2"`). Then edit the text.

### Special characters

In HTML, the `&` character must be written as `&amp;`. So "Registration &
Welcome" becomes `Registration &amp; Welcome`. This is already done
consistently throughout the file.

---

## 9. How to trigger a manual sync

If you want to refresh the participants or speakers list immediately, without
waiting for the daily schedule:

1. In the repository, click the **Actions** tab (at the top of the page).

2. In the left sidebar, click either:
   - **Sync Participants List** — to refresh the participants.
   - **Sync Speakers List** — to refresh the workshop speakers.

3. On the right side of the screen, click **Run workflow → Run workflow** (the
   green button).

4. The workflow will run in about 30–60 seconds. When it finishes you will see
   a green checkmark. The live site updates within another minute.

> **If you see a red ✗ instead of a green checkmark**, click on the failed run
> to see the error message. The most common cause is that the Google Sheet
> URL has changed or the sheet is no longer published as CSV.

---

## 10. Quick reference: where is each piece of text?

Use Ctrl+F (Cmd+F on Mac) in the GitHub editor to find these strings quickly.

| What you want to change | Search for this text |
|---|---|
| Page title (browser tab) | `<title>School` |
| Event dates in hero | `May 18–27, 2026` |
| Registration deadline in hero | `April 7, 2026` |
| About / description paragraph | `Organized at the` |
| Registration open/closed (nav button) | `btn-nav-reg` |
| Registration open/closed (big box) | `reg-cta-box` |
| Registration deadline (big box) | `Registration deadline:` |
| Financial support note | `Financial support for travel` |
| Week I schedule rows | `id="week1"` |
| Week II schedule rows | `id="week2"` |
| Venue address | `Av. Bustillo km 9.5` |
| Closing dinner venue | `Closing Dinner` |
| Social program text | `social` (look for placeholder paragraph nearby) |
| Organising committee names | `Organizing Committee:` (appears twice) |
| Contact email | `particulas.cab@gmail.com` |
| Footer links | `footer-links` |

---

*Last updated: April 2026. For questions, contact the organizing committee at
[particulas.cab@gmail.com](mailto:particulas.cab@gmail.com).*
