#!/usr/bin/env python3
"""
ECT 2569 Election Data Fetcher
Fetches official MP election results from ectreport69.ect.go.th

Since the ECT site has Cloudflare protection, you need to provide
cf_clearance cookies from your browser session.

HOW TO USE:
1. Open https://ectreport69.ect.go.th/ in your browser
2. Pass the Cloudflare "Verify you are human" challenge
3. Open DevTools (F12) → Application → Cookies → ectreport69.ect.go.th
4. Copy the "cf_clearance" cookie value
5. Run:  python fetch_ect69_data.py --cf-clearance "YOUR_COOKIE_VALUE"

OR: Use the browser console method (see fetch_ect69_browser.js)

Endpoints (discovered from the ectreport69 frontend JS):
  Static refs:
    https://static-ectreport69.ect.go.th/data/data/refs/info_province.json
    https://static-ectreport69.ect.go.th/data/data/refs/info_constituency.json
    https://static-ectreport69.ect.go.th/data/data/refs/info_mp_candidate.json
    https://static-ectreport69.ect.go.th/data/data/refs/info_party_overview.json
    https://static-ectreport69.ect.go.th/data/data/refs/info_party_candidate.json
  Stats:
    https://stats-ectreport69.ect.go.th/data/records/stats_cons.json
    https://stats-ectreport69.ect.go.th/data/records/stats_party.json

Output: ../data/election69/ect69_stats_cons.json
        ../data/election69/ect69_stats_party.json
        ../data/election69/ect69_info_mp_candidate.json
        ../data/election69/ect69_info_province.json
        ../data/election69/ect69_info_constituency.json
        ../data/election69/ect69_info_party_overview.json
"""

import requests
import json
import os
import sys
import argparse
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "election69"

STATIC_BASE = "https://static-ectreport69.ect.go.th"
STATS_BASE = "https://stats-ectreport69.ect.go.th"

ENDPOINTS = {
    # Reference data (static)
    "info_province":       f"{STATIC_BASE}/data/data/refs/info_province.json",
    "info_constituency":   f"{STATIC_BASE}/data/data/refs/info_constituency.json",
    "info_mp_candidate":   f"{STATIC_BASE}/data/data/refs/info_mp_candidate.json",
    "info_party_overview": f"{STATIC_BASE}/data/data/refs/info_party_overview.json",
    "info_party_candidate": f"{STATIC_BASE}/data/data/refs/info_party_candidate.json",
    # Statistics
    "stats_cons":          f"{STATS_BASE}/data/records/stats_cons.json",
    "stats_party":         f"{STATS_BASE}/data/records/stats_party.json",
}


def create_session(cf_clearance: str = None) -> requests.Session:
    """Create a requests session with browser-like headers"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://ectreport69.ect.go.th/",
        "Origin": "https://ectreport69.ect.go.th",
    })
    
    if cf_clearance:
        # Set cookies for both subdomains
        for domain in [".ect.go.th", "stats-ectreport69.ect.go.th",
                       "static-ectreport69.ect.go.th", "ectreport69.ect.go.th"]:
            session.cookies.set("cf_clearance", cf_clearance, domain=domain)
    
    return session


def fetch_endpoint(session: requests.Session, name: str, url: str) -> dict:
    """Fetch a single JSON endpoint"""
    print(f"  Fetching {name}...")
    print(f"    URL: {url}")
    
    try:
        r = session.get(url, timeout=30)
        
        if r.status_code == 403:
            print(f"    ❌ 403 Forbidden — Cloudflare is blocking. "
                  "Please provide a valid cf_clearance cookie.")
            return None
        
        r.raise_for_status()
        
        data = r.json()
        size = len(r.content)
        
        if isinstance(data, list):
            print(f"    ✓ {len(data)} records ({size:,} bytes)")
        elif isinstance(data, dict):
            top_keys = list(data.keys())[:5]
            print(f"    ✓ dict with keys: {top_keys} ({size:,} bytes)")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"    ❌ Response is not valid JSON (likely a Cloudflare page)")
        return None


def save_json(data, filename: str):
    """Save data as JSON file"""
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    💾 Saved: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch official ECT election 2569 data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
HOW TO GET cf_clearance COOKIE:
  1. Open https://ectreport69.ect.go.th/ in your browser
  2. Pass the Cloudflare "Verify you are human" challenge
  3. Open DevTools (F12) → Application → Cookies
  4. Find "cf_clearance" and copy its value
  5. Pass it with --cf-clearance "VALUE"
        """
    )
    parser.add_argument(
        "--cf-clearance", "-c",
        help="Cloudflare cf_clearance cookie value from your browser"
    )
    parser.add_argument(
        "--endpoint", "-e",
        choices=list(ENDPOINTS.keys()),
        help="Fetch only a specific endpoint (default: fetch all)"
    )
    args = parser.parse_args()
    
    print("🔍 ECT 2569 Election Data Fetcher")
    print("═" * 50)
    
    if not args.cf_clearance:
        print("\n⚠️  No cf_clearance cookie provided.")
        print("   The ECT site has Cloudflare protection.")
        print("   Will attempt without cookies (may fail).\n")
        print("   To fix: pass --cf-clearance with your browser cookie.\n")
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    session = create_session(args.cf_clearance)
    
    # Determine which endpoints to fetch
    if args.endpoint:
        endpoints = {args.endpoint: ENDPOINTS[args.endpoint]}
    else:
        endpoints = ENDPOINTS
    
    results = {}
    success_count = 0
    fail_count = 0
    
    print("\n📥 Fetching ECT data...")
    for name, url in endpoints.items():
        data = fetch_endpoint(session, name, url)
        if data is not None:
            filename = f"ect69_{name}.json"
            save_json(data, filename)
            results[name] = data
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n{'═' * 50}")
    print(f"✅ Fetched: {success_count}/{len(endpoints)} endpoints")
    if fail_count > 0:
        print(f"❌ Failed:  {fail_count}/{len(endpoints)} endpoints")
        print("\nIf you got 403 errors, the Cloudflare cookie may be expired.")
        print("Please get a fresh cf_clearance cookie from your browser.")
    
    if results:
        print(f"\nData saved to: {OUTPUT_DIR}/")
        print("\nNext step: run build_official_data.py to generate election69_official.js")


if __name__ == "__main__":
    main()
