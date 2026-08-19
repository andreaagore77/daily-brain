# Daily grant search run

This is the instruction set a Claude session follows on each scheduled run.
It is also the text used as the Routine prompt.

## Steps

1. Run `python3 grant_search/validate_profile.py`. If it exits non-zero,
   stop and report exactly what it printed — do not guess company details
   or search against a broken profile. Then read
   `grant_search/company_profile.json` for the org's details.

2. Read `grant_search/data/grants_found.json` for grants already recorded
   (dedupe key: `url`, falling back to `title + funder`).

3. Search for currently open grant opportunities matching the profile's
   `focus_areas`, `home_base`, `service_areas`, `org_type`, and
   `grant_types`:
   - **Government/federal**: web-search
     `site:grants.gov <focus area> <org_type> grants 2026`, plus the
     SAMHSA grants dashboard and BJA/OJP funding pages by name.

     > **Known environment limit (confirmed 2026-08-19):** this sandbox's
     > egress proxy refuses `api.grants.gov` (403 on CONNECT) and blocks
     > `WebFetch` against samhsa.gov, njnonprofits.org, cfnj.org,
     > hfnj.org, and simpler.grants.gov. `WebSearch` is the only working
     > channel. Do not burn a run retrying the API. Because nothing can
     > be verified at source, mark every entry
     > `"confidence": "unverified_search_snippet"` and carry a
     > `verify_before_acting` note. If `WebFetch` ever starts working,
     > verify each entry and upgrade its confidence.
   - **State/regional**: for each entry in `service_areas` (state/regional
     grants generally require operating in-state, not just being
     headquartered there — `home_base` alone isn't enough), web-search
     `<service area> <focus area> nonprofit grant 2026 apply` and check
     that state/region's official economic/community development site.
     Also check the county-level entries' own sites (county human
     services, health, and youth-services departments often post grants
     that never reach statewide portals).

     The county entries are the org's priority footprint, but it is
     eligible **statewide** — so a New Jersey grant open to any NJ
     nonprofit qualifies and should be reported. Rank results with
     county-specific opportunities first, then statewide, and note in
     each entry's `summary` which footprint it falls under. Grants open
     to counties adjacent to the priority ones (e.g. Morris, Hudson,
     Middlesex, Passaic) also qualify — the org serves surrounding
     areas — but rank them below the named counties.
   - **Private foundation/corporate**: web-search
     `<focus area> foundation grant <org_type> 2026 application deadline`,
     and check whether each foundation's eligibility covers `home_base` or
     `service_areas` (many foundations restrict funding to specific
     geographies).
   Skip any grant type not listed in the profile's `grant_types`.

4. For each candidate, discard it if:
   - Deadline has already passed.
   - Amount is below `min_grant_amount_usd` (when known).
   - Title/description matches an `exclude_keywords` entry.
   - It's already in `grants_found.json` (by dedupe key) — unless its
     deadline or amount changed, in which case update the existing entry.

5. For each new/updated grant, record:
   `{ "title", "funder", "url", "grant_type", "amount", "deadline",
   "summary" (1-2 sentences on fit), "first_seen" (today's date, ISO),
   "status": "open" }`. Append/update in
   `grant_search/data/grants_found.json`, sorted by `deadline` ascending.

6. Write a same-day digest to
   `grant_search/data/digests/YYYY-MM-DD.md` listing only what's new or
   changed today (title, funder, amount, deadline, link, one-line fit
   summary). If nothing new, write a one-line "no new matches" digest —
   don't skip the file, it's the record that the run happened.

7. Commit `grant_search/data/grants_found.json` and the new digest file
   with a message like `Grant search: N new, M updated (YYYY-MM-DD)`, and
   push to the current branch.

## Notes for whoever edits this

- No paid grant database is wired in. All discovery is live web search, so
  results quality depends on search coverage that day — this is a
  best-effort feed, not a comprehensive database.
- If `company_profile.json` changes focus areas or location significantly,
  old entries in `grants_found.json` aren't automatically re-filtered;
  review the file if the org's focus changes materially.
