/**
 * ECT Report 69 — Browser Console Data Fetcher (CORS-safe version)
 *
 * CORS blocks fetch() across subdomains, so this script must be run
 * from the SAME origin as the data endpoint.
 *
 * ═══════════════════════════════════════════════════════════════
 * METHOD 1: Run from stats-ectreport69 domain (RECOMMENDED)
 * ═══════════════════════════════════════════════════════════════
 *  1. Open https://stats-ectreport69.ect.go.th/data/records/stats_cons.json
 *  2. Pass Cloudflare challenge
 *  3. You'll see JSON data in the browser — paste SCRIPT A below in console
 *
 * Then:
 *  4. Open https://static-ectreport69.ect.go.th/data/data/refs/info_province.json
 *  5. Pass Cloudflare challenge  
 *  6. Paste SCRIPT B below in console
 *
 * ═══════════════════════════════════════════════════════════════
 * METHOD 2: Manual save (simplest)
 * ═══════════════════════════════════════════════════════════════
 *  Open each URL below in your browser, pass Cloudflare, then Ctrl+S:
 *
 *  Stats (vote results):
 *    https://stats-ectreport69.ect.go.th/data/records/stats_cons.json
 *    https://stats-ectreport69.ect.go.th/data/records/stats_party.json
 *
 *  Reference data:
 *    https://static-ectreport69.ect.go.th/data/data/refs/info_province.json
 *    https://static-ectreport69.ect.go.th/data/data/refs/info_constituency.json
 *    https://static-ectreport69.ect.go.th/data/data/refs/info_mp_candidate.json
 *    https://static-ectreport69.ect.go.th/data/data/refs/info_party_overview.json
 *
 *  Save files as:
 *    ect69_stats_cons.json
 *    ect69_stats_party.json
 *    ect69_info_province.json
 *    ect69_info_constituency.json
 *    ect69_info_mp_candidate.json
 *    ect69_info_party_overview.json
 *
 *  Then move all files to: data/election69/
 */

// ═══════════════════════════════════════════════════════════════
// SCRIPT A: Run on stats-ectreport69.ect.go.th domain
// (after opening any stats URL and passing Cloudflare)
// ═══════════════════════════════════════════════════════════════
async function fetchStatsData() {
  const endpoints = {
    "ect69_stats_cons":  "/data/records/stats_cons.json",
    "ect69_stats_party": "/data/records/stats_party.json",
  };

  for (const [name, path] of Object.entries(endpoints)) {
    try {
      console.log(`📥 Fetching ${name}...`);
      const resp = await fetch(path);
      if (!resp.ok) { console.error(`❌ ${name}: HTTP ${resp.status}`); continue; }
      const data = await resp.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = name + '.json';
      a.click();
      URL.revokeObjectURL(a.href);
      console.log(`✅ ${name}: downloaded (${Array.isArray(data) ? data.length + ' records' : 'object'})`);
      await new Promise(r => setTimeout(r, 500));
    } catch(e) { console.error(`❌ ${name}: ${e.message}`); }
  }
  console.log("Done! Check Downloads folder.");
}
// Uncomment to run: fetchStatsData();

// ═══════════════════════════════════════════════════════════════
// SCRIPT B: Run on static-ectreport69.ect.go.th domain
// (after opening any static URL and passing Cloudflare)
// ═══════════════════════════════════════════════════════════════
async function fetchStaticData() {
  const endpoints = {
    "ect69_info_province":       "/data/data/refs/info_province.json",
    "ect69_info_constituency":   "/data/data/refs/info_constituency.json",
    "ect69_info_mp_candidate":   "/data/data/refs/info_mp_candidate.json",
    "ect69_info_party_overview": "/data/data/refs/info_party_overview.json",
    "ect69_info_party_candidate":"/data/data/refs/info_party_candidate.json",
  };

  for (const [name, path] of Object.entries(endpoints)) {
    try {
      console.log(`📥 Fetching ${name}...`);
      const resp = await fetch(path);
      if (!resp.ok) { console.error(`❌ ${name}: HTTP ${resp.status}`); continue; }
      const data = await resp.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = name + '.json';
      a.click();
      URL.revokeObjectURL(a.href);
      console.log(`✅ ${name}: downloaded (${Array.isArray(data) ? data.length + ' records' : 'object'})`);
      await new Promise(r => setTimeout(r, 500));
    } catch(e) { console.error(`❌ ${name}: ${e.message}`); }
  }
  console.log("Done! Check Downloads folder.");
}
// Uncomment to run: fetchStaticData();
