#!/usr/bin/env python3
"""
sync_participants.py
--------------------
Reads confirmed participants from a public Google Sheet (CSV export)
and writes them to participants.json (used by the GitHub Actions deploy
workflow to serve the list without committing personal data to git).

The Google Sheet must have two column headers: name, affiliation
The sheet must be published as CSV via:
  File -> Share -> Publish to web -> Sheet1 -> CSV -> Publish

Usage (local):
    SHEET_CSV_URL=<url> python sync_participants.py

In GitHub Actions, SHEET_CSV_URL is read from repository secrets.
Output: participants.json (sorted alphabetically by last name)
"""

import csv
import json
import os
import sys

import requests

# ── Config ────────────────────────────────────────────────────────────────────

SHEET_CSV_URL = os.environ.get("SHEET_CSV_URL", "")
JSON_FILE = "participants.json"

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

# ── Write JSON ────────────────────────────────────────────────────────────────

def write_participants(json_path, participants):
    # Sort alphabetically by last name
    participants.sort(key=lambda p: p["name"].split()[-1].lower())
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(participants, f, ensure_ascii=False, indent=2)
    print(f"OK: {len(participants)} participants written to {json_path}")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fetching participants from Google Sheet...")
    people = fetch_participants(SHEET_CSV_URL)
    print(f"  Found {len(people)} entries.")
    write_participants(JSON_FILE, people)
    print("Done.")
