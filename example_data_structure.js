/**
 * Example CONST_RAW and PARTYLIST_RAW Data Structure
 * 
 * This file shows the exact format expected for both datasets.
 * Use this as a reference when building your data.
 */

// ════════════════════════════════════════════════════════════════════════════
// CONSTITUENCY MP (ส.ส. เขต) DATA - 400 constituencies
// ════════════════════════════════════════════════════════════════════════════
// 
// Data from: constituencies (green ballots - เลือกตั้งแบบปกติ)
// Comparison: Invalid ballots % 2566 → 2569

const CONST_RAW_EXAMPLE = [
  {
    // Identification fields
    "cons_id": "NWT_3",
    "prov_id": "NWT",
    "province_thai": "นราธิวาส",
    "province_eng": "NARATHIWAT",
    "cons_no": 3,

    // 2566 (2023) Constituency Data - Invalid Ballots
    "invalid_votes": 6778,           // Green ballot invalid count
    "percent_invalid": 8.42909,      // Green ballot invalid %
    "turn_out": 80412,               // Green ballot voter turnout

    // 2569 (2026) Constituency Data - Invalid Ballots
    "invalid_2026": 2416,            // Green ballot invalid count 2026
    "turnout_2026": 82910,           // Green ballot turnout 2026
    "pct_turnout_2026": 73.14708,    // Green ballot turnout %
    "invalid_pct_2026": 2.914,       // Green ballot invalid % 2026

    // Changes 2566 → 2569
    "invalid_change": -4362,         // Absolute change
    "invalid_pct_change": -5.515,    // Percentage point change

    // 2566 Winner Information
    "winner_party": "พลังประชารัฐ",   // Green ballot winner 2566
    "margin_votes": 4460,            // Margin between top 2 parties
    "winner_votes": 34411,           // Green ballot winner votes 2566
    "runnerup_votes": 29951,         // Green ballot 2nd place votes 2566

    // 2569 Winner Information
    "winner_party_2569": "กล้าธรรม",  // Green ballot winner 2569
    "winner_votes_2569": 36053,      // Green ballot winner votes 2569
    "margin_2569": 1640,             // Margin between top 2 in 2569
    "runnerUp_party": "ประชาชน",     // Green ballot 2nd place 2569
    "runnerUp_votes": 34413          // Green ballot 2nd place votes 2569
  },
  {
    "cons_id": "BKK_1",
    "prov_id": "BKK",
    "province_thai": "กรุงเทพมหานคร",
    "province_eng": "BANGKOK",
    "cons_no": 1,
    "invalid_votes": 1234,
    "percent_invalid": 5.32,
    "turn_out": 123456,
    "invalid_2026": 987,
    "turnout_2026": 125000,
    "pct_turnout_2026": 71.50,
    "invalid_pct_2026": 4.12,
    "invalid_change": -247,
    "invalid_pct_change": -1.20,
    "winner_party": "เพื่อไทย",
    "margin_votes": 8900,
    "winner_votes": 45000,
    "runnerup_votes": 36100,
    "winner_party_2569": "เพื่อไทย",
    "winner_votes_2569": 48000,
    "margin_2569": 12000,
    "runnerUp_party": "ประชาธิปัตย์",
    "runnerUp_votes": 36000
  }
  // ... 398 more records
];


// ════════════════════════════════════════════════════════════════════════════
// PARTY LIST MP (บส. รายชื่อ) DATA - 77 party list regions
// ════════════════════════════════════════════════════════════════════════════
// 
// Data from: party_list elections (pink ballots - เลือกตั้งแบบสัดส่วน)
// Comparison: Invalid ballots % 2566 → 2569
//
// Note: Thailand has 77 party list regions (one per province)
// So PARTYLIST_RAW will have fewer records than CONST_RAW (77 vs 400)

const PARTYLIST_RAW_EXAMPLE = [
  {
    // Identification fields
    // For party list, cons_no typically represents the region/province
    "cons_id": "NWT_PL",
    "prov_id": "NWT",
    "province_thai": "นราธิวาส",
    "province_eng": "NARATHIWAT",
    "cons_no": 1,  // Often just 1 for party list (whole province is one region)

    // 2566 (2023) Party List Data - Invalid Ballots
    "invalid_votes": 8234,           // Pink ballot invalid count
    "percent_invalid": 9.12,         // Pink ballot invalid %
    "turn_out": 90234,               // Pink ballot voter turnout

    // 2569 (2026) Party List Data - Invalid Ballots
    "invalid_2026": 3456,            // Pink ballot invalid count 2026
    "turnout_2026": 92010,           // Pink ballot turnout 2026
    "pct_turnout_2026": 74.25,       // Pink ballot turnout %
    "invalid_pct_2026": 3.75,        // Pink ballot invalid % 2026

    // Changes 2566 → 2569
    "invalid_change": -4778,         // Absolute change
    "invalid_pct_change": -5.37,     // Percentage point change

    // 2566 Winner Information
    "winner_party": "พลังประชารัฐ",   // Pink ballot winner 2566
    "margin_votes": 5600,            // Margin between top 2 parties
    "winner_votes": 42000,           // Pink ballot winner votes 2566
    "runnerup_votes": 36400,         // Pink ballot 2nd place votes 2566

    // 2569 Winner Information
    "winner_party_2569": "กล้าธรรม",  // Pink ballot winner 2569
    "winner_votes_2569": 45000,      // Pink ballot winner votes 2569
    "margin_2569": 8500,             // Margin between top 2 in 2569
    "runnerUp_party": "ประชาชน",     // Pink ballot 2nd place 2569
    "runnerUp_votes": 36500          // Pink ballot 2nd place votes 2569
  },
  {
    "cons_id": "BKK_PL",
    "prov_id": "BKK",
    "province_thai": "กรุงเทพมหานคร",
    "province_eng": "BANGKOK",
    "cons_no": 1,
    "invalid_votes": 5600,
    "percent_invalid": 4.85,
    "turn_out": 115456,
    "invalid_2026": 4500,
    "turnout_2026": 120000,
    "pct_turnout_2026": 70.25,
    "invalid_pct_2026": 3.75,
    "invalid_change": -1100,
    "invalid_pct_change": -1.10,
    "winner_party": "เพื่อไทย",
    "margin_votes": 12000,
    "winner_votes": 55000,
    "runnerup_votes": 43000,
    "winner_party_2569": "ประชาธิปัตย์",
    "winner_votes_2569": 56000,
    "margin_2569": 15000,
    "runnerUp_party": "เพื่อไทย",
    "runnerUp_votes": 41000
  }
  // ... 75 more records (one per province)
];


// ════════════════════════════════════════════════════════════════════════════
// KEY DIFFERENCES SUMMARY
// ════════════════════════════════════════════════════════════════════════════

/*
CONST_RAW (ส.ส. เขต - Constituency MP):
  - 400 constituencies (1-15 per province)
  - Green ballot (เลือกตั้งแบบปกติ) data for both 2566 and 2569
  - Invalid ballot comparison between two election rounds
  - Winner = direct constituency winner

PARTYLIST_RAW (บส. รายชื่อ - Party List MP):
  - ~77 regions (one per province)
  - Pink ballot (เลือกตั้งแบบสัดส่วน) data for both 2566 and 2569
  - Invalid ballot comparison between two election rounds
  - Winner = party with most votes in that province/region

DATA SOURCES:
  CONST_RAW 2566:     election66/th_election66_stats_cons.json
  CONST_RAW 2569:     election-69-OCR-result/data/matched/constituency/*.json
  
  PARTYLIST_RAW 2566: election66/th_election66_stats_party.json
  PARTYLIST_RAW 2569: election-69-OCR-result/data/matched/party_list/*.json


INVALID BALLOT CALCULATION:
  percent_invalid = (invalid_ballots / turn_out) * 100
  invalid_pct_change = pct_2569 - pct_2566
  invalid_change = invalid_2026 - invalid_votes


IMPORTANT FIELDS:
  ✓ All numeric values must be valid numbers (no null, no NaN)
  ✓ Party names must exactly match your PARTY_COLOR mapping in index.html
  ✓ Province names are in Thai (ภาษาไทย)
  ✓ Percentages should be 0-100, usually 2-15% for invalid ballots
  ✓ Margin should be positive (winner - runner-up)
*/

// ════════════════════════════════════════════════════════════════════════════
// VALIDATION CHECKLIST
// ════════════════════════════════════════════════════════════════════════════

/*
Before using your generated data, verify:

DATA INTEGRITY:
  □ CONST_RAW has exactly 400 records
  □ PARTYLIST_RAW has exactly 77 records
  □ All records have required fields (no undefined, no null)
  □ No NaN or Infinity values
  □ All numbers are actual numbers (not strings)

FIELD VALUES:
  □ Percentages are between 0-100
  □ Invalid ballot percentages typically 2-15%
  □ Percentage changes typically -10 to +10
  □ Margin values are positive (winner - runner-up)
  □ Voter turnout makes sense (usually 50-80%)

NAMING:
  □ Province names in Thai match exactly
  □ Party names match PARTY_COLOR keys in index.html
  □ cons_no values are 1-15 for normal constituency
  □ prov_id is 3-letter code

CONSISTENCY:
  □ Same cons_no between CONST_RAW and matching province
  □ Similar invalid ballot percentages for same province
  □ All 2569 records present
  □ 2566 data filled in (not placeholder zeros)

*/
