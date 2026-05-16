# School & Workshop on Advanced Aspects of QFT — Bariloche 2026

Conference website for the Simons-Balseiro School and Workshop on Advanced Aspects of QFT, hosted at the Instituto Balseiro / Centro Atómico Bariloche, May 18–27, 2026.

**Live site:** <https://particulascab-workshop.github.io/school-workshop-2026/>

## Structure

```
index.html                            ← single-page site
participants.json                     ← participant list (bootstrap; see Privacy below)
speakers.json                         ← workshop speaker list (bootstrap; see Privacy below)
sync_participants.py                  ← generates participants.json from Google Sheet
sync_speakers.py                      ← generates speakers.json from Google Sheet
Alexander-Zamolodchikov-700x467.jpeg  ← speaker photos
fewster.jpg
gomis.jpg
hollands.jpg
shifman.jpg
srednicki.jpg
```

## GitHub Pages deployment

The site is deployed via **GitHub Actions** (`.github/workflows/deploy.yml`).

### Initial setup

1. Push this repo to GitHub.
2. Go to **Settings → Pages**.
3. Under *Source*, select **GitHub Actions**.
4. The workflow will run automatically on every push to `main` and deploy the site.

> **Note:** If you are still on *Deploy from a branch*, change the source to **GitHub Actions**  
> to take advantage of the privacy improvements described below.

### Participant / speaker data (Google Sheet secrets)

The deploy workflow optionally fetches fresh participant and speaker data from Google Sheets.
Set the following repository secrets (**Settings → Secrets and variables → Actions**):

| Secret | Used by |
|--------|---------|
| `SHEET_CSV_URL` | `sync_participants.py` — published CSV of the participants sheet |
| `SPEAKERS_CSV_URL` | `sync_speakers.py` — published CSV of the speakers sheet |

If the secrets are not set, the workflow falls back to the `participants.json` /
`speakers.json` files already in the repository (bootstrap data).

## Privacy

Personal data (participant names and affiliations) is **not embedded in `index.html`**.
Instead, `index.html` loads it at runtime from `participants.json` and `speakers.json`.

The current `participants.json` / `speakers.json` files are **bootstrap copies** committed
to the repository. To remove personal data from the git repository entirely:

1. Ensure the deploy workflow runs successfully with the Google Sheet secrets configured
   (so the live site still shows data after the files are removed from git).
2. Stop tracking the files:
   ```sh
   git rm --cached participants.json speakers.json
   printf "participants.json\nspeakers.json\n" >> .gitignore
   git add .gitignore
   git commit -m "chore: stop tracking generated data files"
   git push
   ```
3. Optionally, rewrite git history to remove the bootstrap data from past commits  
   (use `git filter-repo --path participants.json --path speakers.json --invert-paths`).

After these steps, participant data will exist only in Google Sheets and in the
GitHub Pages deployment artifact — never committed to the git repository.

## What to fill in before launch

| Section | What to update | Status |
|---|---|---|
| **Speakers** | Replace the "To be announced" cards with real names, affiliations, and photos. | ✅ Done (6 speakers listed) |
| **Registration fees** | Fill in the TBA cells in the fee table. | ⬜ Pending |
| **Key dates** | Fill in the deadline rows in the Registration section. | ⬜ Pending |
| **Register Now** | Replace `href="#"` on the button with the Google Form URL. | ✅ Done |
| **Social program** | Edit the placeholder paragraph when events are confirmed. | ⬜ Pending |
| **Map** | The iframe already targets Instituto Balseiro; verify the embed URL is loading correctly. | ✅ Done |

## Sponsors

This event is supported by the **Simons Foundation**, **CONICET**, and the **Instituto Balseiro**.

## Organizing Committee

- H. Casini
- M. Huerta
- J. Magán
- G. Torroba

## Contact

- **Email:** [particulas.cab@gmail.com](mailto:particulas.cab@gmail.com)
- **Research group:** <https://sites.google.com/view/particulasycampos-cabib/home>
