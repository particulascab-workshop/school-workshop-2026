#!/usr/bin/env python3
"""
sync_speakers.py
----------------
Reads confirmed workshop speakers from a public Google Sheet (CSV export)
and injects them into the `var speakers = [...]` array in index.html.

The Google Sheet must have two column headers: name, affiliation
The sheet must be published as CSV via:
  File -> Share -> Publish to web -> Sheet1 -> CSV -> Publish

Usage (local):
  SPEAKERS_CSV_URL=<url> python sync_speakers.py

In GitHub Actions, SPEAKERS_CSV_URL is read from repository secrets.
"""

import csv
import json
import os
import re
import sys

import requests

# ── Config ────────────────────────────────────────────────────────────────────

SPEAKERS_CSV_URL = os.environ.get("SPEAKERS_CSV_URL", "")
HTML_FILE = "index.html"

# Matches the full `var speakers = [ ... ];` block in the JS
SPEAKERS_RE = re.compile(
    r"var speakers\s*=\s*\[[^\]]*\];",
    re.DOTALL,
)

# ── Fetch & parse ─────────────────────────────────────────────────────────────

def fetch_speakers(url):
    if not url:
        print("ERROR: SPEAKERS_CSV_URL environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    lines = response.content.decode("utf-8").splitlines()
    reader = csv.DictReader(lines)
    speakers = []
    for row in reader:
        name = row.get("name", "").strip()
        affiliation = row.get("affiliation", "").strip()
        if name:
            speakers.append({"name": name, "affiliation": affiliation})
    return speakers

# ── Inject into HTML ──────────────────────────────────────────────────────────

def inject_speakers(html_path, speakers):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Sort alphabetically by last name
    speakers.sort(key=lambda p: p["name"].split()[-1].lower())
    entries = ",\n      ".join(json.dumps(p, ensure_ascii=False) for p in speakers)
    replacement = f"var speakers = [\n      {entries}\n      ];"
    new_content, n = SPEAKERS_RE.subn(replacement, content)
    if n == 0:
        print("ERROR: Could not find `var speakers = [...]` in the HTML.", file=sys.stderr)
        sys.exit(1)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: {len(speakers)} speakers written to {html_path}")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fetching speakers from Google Sheet...")
    people = fetch_speakers(SPEAKERS_CSV_URL)
    print(f"  Found {len(people)} entries.")
    inject_speakers(HTML_FILE, people)
    print("Done. Commit and push index.html to publish.")
