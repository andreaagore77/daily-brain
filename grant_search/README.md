# Grant Search

Automated daily discovery of open grant opportunities (government/federal,
state/regional, and private foundation/corporate) matching one company's
profile.

## How it works

There's no scraper or paid grant-database API key here — discovery is done
via live web search each run, executed by a scheduled Claude session
following `SEARCH_PROMPT.md`. Results accumulate in
`data/grants_found.json`, and each run drops a same-day summary in
`data/digests/`.

## Setup

1. Edit `company_profile.json` — replace every `REPLACE_...` placeholder
   with the real company/org details (name, mission, focus areas,
   location, budget, grant types wanted). The search quality depends
   entirely on this being accurate.
2. A daily Routine is configured to fire `SEARCH_PROMPT.md`'s instructions
   into a fresh session, which searches, updates `data/grants_found.json`,
   writes a digest, and pushes the changes.

## Files

- `company_profile.json` — the org profile driving relevance filtering.
- `data/grants_found.json` — cumulative store of matched grants (open +
  historical, deduped by URL).
- `data/digests/YYYY-MM-DD.md` — what changed on each run.
- `SEARCH_PROMPT.md` — the exact instructions each scheduled run follows.

## Running manually

Ask Claude Code (in this repo) to "run today's grant search" — it will
follow `SEARCH_PROMPT.md` directly.
