"""
ECT 2566 Election Data Extractor
Fetches MP candidate vote data from https://ectreport66.ect.go.th

Endpoints discovered from index-87630a5f.js:
  - /data/refs/info_province.json       → province metadata
  - /data/refs/info_constituency.json   → constituency metadata
  - /data/refs/info_mp_candidate.json   → MP candidate info (name, party, number)
  - /data/stats/stats_cons.json         → per-constituency vote stats (valid/invalid votes, etc.)
  - /data/refs/info_party_overview.json → party list metadata
  - /data/stats/stats_party.json        → party list vote stats
  - /data/excel/2566_election_result.xlsx → full results as Excel (bulk download)

Run: python fetch_ect_data.py
Output: ect_mp_votes.csv, ect_mp_votes.json
"""

import requests
import json
import csv
import os

BASE_URL = "https://ectreport66.ect.go.th"

ENDPOINTS = {
    "province":      "/data/refs/info_province.json",
    "constituency":  "/data/refs/info_constituency.json",
    "mp_candidate":  "/data/refs/info_mp_candidate.json",
    "stats_cons":    "/data/stats/stats_cons.json",
}

EXCEL_URL = BASE_URL + "/data/excel/2566_election_result.xlsx"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://ectreport66.ect.go.th/",
    "Origin": "https://ectreport66.ect.go.th",
})


def fetch(key, path):
    url = BASE_URL + path
    print(f"Fetching {key} from {url} ...")
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    # ── Fetch all reference data ─────────────────────────────────────────────
    data = {k: fetch(k, v) for k, v in ENDPOINTS.items()}

    # ── Build lookup dictionaries ────────────────────────────────────────────
    # Province: province_id → province_name (Thai + Eng if available)
    province_map = {}
    for p in data["province"]:
        province_map[p["province_id"]] = p.get("province_name", p.get("name_th", ""))

    # Constituency: constituency_id / zone_id → metadata
    # Print first item to understand schema
    print("\n── Sample constituency record ──")
    if data["constituency"]:
        print(json.dumps(data["constituency"][0], ensure_ascii=False, indent=2))

    # MP candidate: candidate_id → candidate info
    print("\n── Sample MP candidate record ──")
    if data["mp_candidate"]:
        print(json.dumps(data["mp_candidate"][0], ensure_ascii=False, indent=2))

    # Stats cons: constituency-level vote summary
    print("\n── Sample stats_cons record ──")
    if data["stats_cons"]:
        print(json.dumps(data["stats_cons"][0], ensure_ascii=False, indent=2))

    # ── Build constituency lookup ────────────────────────────────────────────
    cons_map = {}
    for c in data["constituency"]:
        cid = c.get("constituency_id") or c.get("zone_id")
        cons_map[cid] = c

    # ── Build stats_cons lookup ──────────────────────────────────────────────
    stats_map = {}
    for s in data["stats_cons"]:
        cid = s.get("constituency_id") or s.get("zone_id")
        stats_map[cid] = s

    # ── Merge: one row per MP candidate ─────────────────────────────────────
    rows = []
    for cand in data["mp_candidate"]:
        cid = cand.get("constituency_id") or cand.get("zone_id")
        cons = cons_map.get(cid, {})
        stats = stats_map.get(cid, {})

        row = {
            # Candidate fields
            "candidate_id":        cand.get("candidate_id"),
            "candidate_number":    cand.get("candidate_number") or cand.get("no"),
            "name_th":             cand.get("name_th") or cand.get("full_name_th"),
            "name_en":             cand.get("name_en") or cand.get("full_name_en"),
            "party_id":            cand.get("party_id"),
            "party_name":          cand.get("party_name") or cand.get("party_name_th"),
            "is_elected":          cand.get("is_elected") or cand.get("elected"),
            "votes":               cand.get("votes") or cand.get("candidate_votes"),
            "percent_votes":       cand.get("percent_votes"),

            # Constituency fields
            "constituency_id":     cid,
            "zone_no":             cons.get("zone_no") or cons.get("zone_number"),
            "province_id":         cons.get("province_id"),
            "province_name":       province_map.get(cons.get("province_id"), ""),

            # Constituency-level vote stats
            "valid_votes":         stats.get("valid_votes"),
            "invalid_votes":       stats.get("invalid_votes"),
            "percent_valid_votes": stats.get("percent_valid_votes"),
            "percent_invalid_votes": stats.get("percent_invalid_votes"),
            "total_rights":        stats.get("total_rights") or stats.get("eligible_voters"),
            "total_turnout":       stats.get("total_turnout") or stats.get("turnout"),
        }
        rows.append(row)

    print(f"\n── Total candidate rows: {len(rows)} ──")

    # ── Write CSV ────────────────────────────────────────────────────────────
    if rows:
        csv_path = "ect_mp_votes.csv"
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved: {csv_path}")

    # ── Write JSON ───────────────────────────────────────────────────────────
    json_path = "ect_mp_votes.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Saved: {json_path}")

    # ── Optional: also download the bulk Excel ───────────────────────────────
    print(f"\nTo download the full Excel file:\n  curl -L '{EXCEL_URL}' -o 2566_election_result.xlsx")


if __name__ == "__main__":
    main()
