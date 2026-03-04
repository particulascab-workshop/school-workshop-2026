#!/usr/bin/env python3
"""
sync_participants.py
--------------------
Reads confirmed participants from a public Google Sheet (CSV export)
and injects them into the `var participants = [...]` array in index.html.

The Google Sheet must have two column headers: name, affiliation
The sheet must be published as CSV via:
  File -> Share -> Publish to web -> Sheet1 -> CSV -> Publish

Usage (local):
    SHEET_CSV_URL=<url> python sync_participants.py

In GitHub Actions, SHEET_CSV_URL is read from repository secrets.
"""

import csv
import json
import os
import re
import sys

import requests

# ── Config ────────────────────────────────────────────────────────────────────

SHEET_CSV_URL = os.environ.get("SHEET_CSV_URL", "")
HTML_FILE = "index.html"

# Matches the full `var participants = [ ... ];` block in the JS
PARTICIPANTS_RE = re.compile(
    r"var participants\s*=\s*\[[^\]]*\];",
    re.DOTALL,
)

# ── Fetch & parse ─────────────────────────────────────────────────────────────

def fetch_participants(url):
    if not url:
        print("ERROR: SHEET_CSV_URL environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    lines = response.content.decode("utf-8").splitlines()
    reader = csv.DictReader(lines)
    participants = []
    for row in reader:
        name = row.get("name", "").strip()
        affiliation = row.get("affiliation", "").strip()
        if name:
            participants.append({"name": name, "affiliation": affiliation})
    return participants

# ── Inject into HTML ──────────────────────────────────────────────────────────

def inject_participants(html_path, participants):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Sort alphabetically by last name
    participants.sort(key=lambda p: p["name"].split()[-1].lower())
    entries = ",\n    ".join(json.dumps(p, ensure_ascii=False) for p in participants)
    replacement = f"var participants = [\n    {entries}\n  ];"
    new_content, n = PARTICIPANTS_RE.subn(replacement, content)
    if n == 0:
        print("ERROR: Could not find `var participants = [...]` in the HTML.", file=sys.stderr)
        sys.exit(1)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: {len(participants)} participants written to {html_path}")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fetching participants from Google Sheet...")
    people = fetch_participants(SHEET_CSV_URL)
    print(f"  Found {len(people)} entries.")
    inject_participants(HTML_FILE, people)
    print("Done. Commit and push index.html to publish.")
