#!/usr/bin/env python3
"""
sync_speakers.py
----------------
Reads confirmed workshop speakers from a public Google Sheet (CSV export)
and writes them to speakers.json (used by the GitHub Actions deploy
workflow to serve the list without committing personal data to git).

The Google Sheet must have two column headers: name, affiliation
The sheet must be published as CSV via:
  File -> Share -> Publish to web -> Sheet1 -> CSV -> Publish

Usage (local):
  SPEAKERS_CSV_URL=<url> python sync_speakers.py

In GitHub Actions, SPEAKERS_CSV_URL is read from repository secrets.
Output: speakers.json (sorted alphabetically by last name)
"""

import csv
import json
import os
import sys

import requests

# ── Config ────────────────────────────────────────────────────────────────────

SPEAKERS_CSV_URL = os.environ.get("SPEAKERS_CSV_URL", "")
JSON_FILE = "speakers.json"

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

# ── Write JSON ────────────────────────────────────────────────────────────────

def write_speakers(json_path, speakers):
    # Sort alphabetically by last name
    speakers.sort(key=lambda p: p["name"].split()[-1].lower())
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(speakers, f, ensure_ascii=False, indent=2)
    print(f"OK: {len(speakers)} speakers written to {json_path}")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fetching speakers from Google Sheet...")
    people = fetch_speakers(SPEAKERS_CSV_URL)
    print(f"  Found {len(people)} entries.")
    write_speakers(JSON_FILE, people)
    print("Done.")
