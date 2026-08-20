#!/usr/bin/env python3
"""Scaffold a working folder for one grant application.

    python3 grant_search/apply/new_application.py --list
    python3 grant_search/apply/new_application.py "Empower New Jersey"

Reads the grant's record from data/grants_found.json and creates
apply/applications/<slug>/ with a checklist, a funder record to fill in, and
draft stubs pointing at the org-kit sections that feed each one.

Creating a folder is not a decision to apply. Nothing here submits anything —
see APPLY_PROMPT.md for where the approval gate sits.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
DATA = HERE.parent / "data" / "grants_found.json"
APPS = HERE / "applications"

TIERS = [
    "tier_1_act_now",
    "tier_2_strong_fit_later_deadline",
    "tier_3_possible_needs_research",
]


def load_grants():
    d = json.loads(DATA.read_text())
    out = []
    for key in TIERS:
        for g in d.get(key, []):
            g = dict(g)
            g["_tier"] = key
            out.append(g)
    return out


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def find(grants, query):
    q = query.lower()
    hits = [g for g in grants if q in g["title"].lower() or q in g["funder"].lower()]
    if not hits:
        sys.exit(f"No grant matches {query!r}. Run with --list to see options.")
    if len(hits) > 1:
        lines = "\n".join(f"  - {g['title']} ({g['funder']})" for g in hits)
        sys.exit(f"{query!r} matches several grants — be more specific:\n{lines}")
    return hits[0]


def days_out(deadline):
    try:
        return (dt.date.fromisoformat(deadline) - dt.date.today()).days
    except (ValueError, TypeError):
        return None


def build(g):
    name = f"{g['funder']} — {g['title']}"
    d = g.get("deadline", "unknown")
    left = days_out(d)
    left_txt = f"{left} days from today" if left is not None else "no fixed date"
    stage = g.get("deadline_type", "full application")

    folder = APPS / slug(f"{g['funder']}-{g['title']}")
    if folder.exists():
        sys.exit(f"{folder} already exists — edit it rather than regenerating.")
    (folder / "drafts").mkdir(parents=True)
    (folder / "attachments").mkdir()

    (folder / "00-CHECKLIST.md").write_text(f"""# {name}

| | |
|---|---|
| Deadline | **{d}** ({left_txt}) |
| Stage | {stage} |
| Amount | {g.get('amount', 'unspecified')} |
| Type | {g.get('grant_type', '')} |
| Scaffolded | {dt.date.today()} |

## Status: NOT APPROVED TO SUBMIT

This folder exists so the work can be prepared. It is not a decision to apply.
Nothing gets submitted until the organization gives explicit approval, and a
person — not this system — performs the submission.

- [ ] **Approved to pursue** — by whom, date:
- [ ] **Approved to submit** — by whom, date:

## Before writing anything

- [ ] Read the actual NOFO/RFP — confirm eligibility in its own words
- [ ] Confirm the deadline at the source (records here can be stale)
- [ ] Confirm submission portal and whether registration is needed
- [ ] Note match requirement, if any
- [ ] Note page limits and formatting rules
- [ ] Fill in `01-funder-record.md`

## Narrative

- [ ] Statement of need — from `org_kit/03-statement-of-need.md`
- [ ] Program description — from `org_kit/04-program-descriptions.md`
- [ ] Logic model / evaluation — from `org_kit/06-logic-model-and-evaluation.md`
- [ ] Organizational capacity — from `org_kit/10-sustainability-and-capacity.md`
- [ ] Sustainability — from `org_kit/10-sustainability-and-capacity.md`

## Budget

- [ ] Project budget — from `org_kit/07-budget.md`
- [ ] Budget narrative with arithmetic shown
- [ ] Indirect rate elected (10% de minimis unless a NICRA exists)
- [ ] Cash-flow check if cost-reimbursement

## Attachments

- [ ] Pull standard set from `org_kit/08-attachments-checklist.md`
- [ ] **Letters of support requested — do this 3 weeks out**
- [ ] Any funder-specific forms

## Final

- [ ] Every claim traceable to a real source; no invented figures
- [ ] Page limits and formatting met
- [ ] Internal review by someone who did not draft it
- [ ] Submitted by [name], date, confirmation number:

## Notes from the pipeline record

{g.get('summary', '')}

{('**Watch out:** ' + g['watch_out']) if g.get('watch_out') else ''}
""")

    (folder / "01-funder-record.md").write_text(f"""# Funder record — {g['funder']}

Contact and submission detail. Fill from the funder's own site and the NOFO;
leave a field blank rather than guessing at it.

## Submission

| Field | Value |
|---|---|
| Opportunity number | [[PLACEHOLDER]] |
| Submission portal | [[PLACEHOLDER: Grants.gov / JustGrants / funder portal / email]] |
| Portal URL | [[PLACEHOLDER]] |
| Registration needed | [[PLACEHOLDER]] |
| Deadline (confirmed at source) | [[PLACEHOLDER]] |
| Deadline time + timezone | [[PLACEHOLDER: federal deadlines are usually 11:59pm or 8:59pm ET]] |
| Two-step deadline? | [[PLACEHOLDER: DOJ uses Grants.gov then JustGrants, days apart]] |

## Contacts

| Role | Name | Email | Phone |
|---|---|---|---|
| Program officer | [[PLACEHOLDER]] | | |
| Grants management / budget | [[PLACEHOLDER]] | | |
| Technical/portal help desk | [[PLACEHOLDER]] | | |

## Mailing address

[[PLACEHOLDER: only if hard copy is accepted or required]]

## Requirements extracted from the NOFO

| Item | Requirement |
|---|---|
| Eligible applicants (quote it) | [[PLACEHOLDER]] |
| Match / cost share | [[PLACEHOLDER]] |
| Project period | [[PLACEHOLDER]] |
| Award ceiling / floor | {g.get('amount', '[[PLACEHOLDER]]')} |
| Expected number of awards | [[PLACEHOLDER]] |
| Page limit | [[PLACEHOLDER]] |
| Format rules | [[PLACEHOLDER: font, margins, spacing]] |
| Required attachments | [[PLACEHOLDER]] |
| Scoring criteria and weights | [[PLACEHOLDER: write these out — they tell you where to spend words]] |

## Prior awardees

Worth 20 minutes: who won this last cycle, at what size, for what.

[[PLACEHOLDER]]

## Questions to ask the program officer

Most funders welcome a pre-application call, and it is the cheapest available
signal on whether an application is worth writing.

- [[PLACEHOLDER: e.g. does a referral-partner model satisfy the treatment requirement?]]
""")

    for fn, src in [
        ("need.md", "org_kit/03-statement-of-need.md"),
        ("program.md", "org_kit/04-program-descriptions.md"),
        ("evaluation.md", "org_kit/06-logic-model-and-evaluation.md"),
        ("budget-narrative.md", "org_kit/07-budget.md"),
    ]:
        (folder / "drafts" / fn).write_text(
            f"# {fn[:-3].replace('-', ' ').title()} — {name}\n\n"
            f"Source: `{src}`\n\n"
            f"Copy the relevant section, then tailor to this funder's scoring\n"
            f"criteria and page limit. Corrections to shared facts belong back\n"
            f"in the org kit, not only here.\n\n"
            f"[[DRAFT]]\n"
        )

    print(f"created {folder.relative_to(HERE.parent.parent)}")
    print(f"  deadline {d} ({left_txt})")
    print("  start with 00-CHECKLIST.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("grant", nargs="?", help="part of the grant or funder name")
    ap.add_argument("--list", action="store_true", help="list grants in the pipeline")
    a = ap.parse_args()

    grants = load_grants()
    if a.list or not a.grant:
        rows = []
        for g in grants:
            d = g.get("deadline", "")
            rows.append((days_out(d) if days_out(d) is not None else 99999, g))
        rows.sort(key=lambda r: r[0])
        print(f"{'DAYS':>6}  {'DEADLINE':<12} GRANT")
        for left, g in rows:
            lt = f"{left}" if left != 99999 else "-"
            print(f"{lt:>6}  {g.get('deadline',''):<12} {g['title'][:44]} ({g['funder'][:28]})")
        return
    build(find(grants, a.grant))


if __name__ == "__main__":
    main()
