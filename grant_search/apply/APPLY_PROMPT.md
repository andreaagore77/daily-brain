# Daily application-support run

Replaces the pure discovery run. The pipeline is now largely built; the work is
preparing applications against it. This is the instruction set each scheduled
run follows.

## The hard rule

**This system never submits anything.** It prepares. A person submits.

That is not caution for its own sake — it is how the process legally works:

- Federal applications are certified by a named **Authorized Organization
  Representative** under penalty of perjury. That certification cannot be
  delegated to software.
- **SAM.gov's terms of use prohibit bots and automated data gathering**, and
  automated access can get an entity's account denied. Never script against
  SAM.gov. If SAM data is ever needed, use the public API at open.gsa.gov with a
  registered key, or the published bulk extracts.
- Grants.gov and JustGrants submissions likewise require a human, authorized
  account holder.

Two approval gates, both recorded in each application's `00-CHECKLIST.md`:

1. **Approved to pursue** — before drafting effort goes in
2. **Approved to submit** — before anything leaves the organization

Never mark either one on the organization's behalf. If a gate is unmarked, keep
preparing up to it and stop.

## Steps each run

1. **Validate.** Run `python3 grant_search/validate_profile.py`. If it fails,
   report and stop.

2. **Check the calendar.** Run
   `python3 grant_search/apply/new_application.py --list`. Anything inside 60
   days with no application folder is worth flagging; inside 30 days it is
   urgent. Also flag any deadline that has passed so the record can be closed.

3. **Advance approved applications.** For each folder in
   `apply/applications/` where "Approved to pursue" is checked:
   - Work the unchecked items in `00-CHECKLIST.md`, in order.
   - Fill `01-funder-record.md` gaps — opportunity number, portal, contacts,
     scoring criteria, page limits, match. Use `WebSearch`; leave a field blank
     rather than guessing. Never invent an email address.
   - Draft narrative sections in `drafts/`, sourcing shared content from the org
     kit and tailoring to this funder's scoring criteria.
   - Stop at "Approved to submit."

4. **Never fabricate organizational facts.** Participant counts, outcome data,
   board members, staff credentials, budget lines, dates of incorporation — if
   the org kit has a `[[PLACEHOLDER]]`, the answer is unknown. Leave the
   placeholder and list it as a gap for the organization to fill. Inventing any
   of these in a grant application is fraud, and would expose the organization
   to far worse than a declined application.

5. **Keep the org kit canonical.** When a shared fact is learned or corrected,
   update `org_kit/` — not just the application that surfaced it.

6. **Light discovery.** Discovery is no longer the main job, but run one or two
   searches for new NJ behavioral health / reentry opportunities and add
   anything genuinely new to `data/grants_found.json`. Do not re-litigate the
   existing screening.

7. **Write the digest** to `data/digests/YYYY-MM-DD.md`: what advanced, what is
   blocked and on whom, what needs the organization's decision, deadlines
   approaching. If nothing changed, write the one-line digest anyway.

8. **Commit and push** to the current branch.

## Known environment limits

- `WebFetch` is blocked against funder domains and `api.grants.gov` refuses
  connections. `WebSearch` is the only working channel, so funder-record fields
  will often stay blank pending a human opening the NOFO. Mark them
  `[[PLACEHOLDER]]`; do not fill them from inference.
- LibreOffice cannot load files in this sandbox, so `.xlsx` outputs cannot be
  recalculated here. Spreadsheets are written with values, not formulas, where
  it matters.

## What "good" looks like on a run

A run that fills six real funder-record fields, drafts one tailored section, and
names three gaps only the organization can close is a good run. A run that
produces polished prose full of invented numbers is a bad one, however complete
it looks.
