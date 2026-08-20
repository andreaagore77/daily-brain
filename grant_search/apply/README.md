# Apply

Turns the grant pipeline into prepared applications. Discovery still runs, but
lightly — the pipeline is built; the work now is applying to it.

## What's here

```
apply/
  APPLY_PROMPT.md      instructions each scheduled run follows
  build_org_kit.py     regenerates org_kit/ from company_profile.json
  new_application.py   scaffolds a working folder for one grant
  org_kit/             the reusable core of every application
  applications/        one folder per grant being pursued
```

## The org kit

Grant applications repeat most of their content. The org kit holds that content
once — mission, boilerplate at four lengths, statement of need, program
descriptions, people, logic model and evaluation, budget templates, attachments
checklist, partnerships, sustainability and capacity.

A fact lives in exactly one place. Correct it there, not in each application.

**Before the first submission, fill in the placeholders.** There are ~106 of
them, deliberately: they are facts only the organization holds, and this system
will not guess at them. `org_kit/00-README.md` lists the highest-priority ones.

## Using it

```bash
# what's coming up
python3 grant_search/apply/new_application.py --list

# start a folder for one grant
python3 grant_search/apply/new_application.py "Empower New Jersey"

# regenerate the org kit after editing company_profile.json
python3 grant_search/apply/build_org_kit.py
```

Note that `build_org_kit.py` **overwrites** the org kit. Filled-in placeholders
would be lost — move durable edits into the script, or stop re-running it once
the kit is populated.

## Two approval gates

Each application's `00-CHECKLIST.md` carries them:

1. **Approved to pursue** — before drafting effort goes in
2. **Approved to submit** — before anything leaves the organization

Neither is ever marked on the organization's behalf. Creating a folder is not a
decision to apply.

## This system does not submit

Federal applications are certified by a named Authorized Organization
Representative under penalty of perjury, SAM.gov's terms prohibit automated
access, and Grants.gov requires an authorized human account holder. The system
prepares the packet; a person submits it.

It also does not invent organizational facts. Where the org kit shows
`[[PLACEHOLDER]]`, the answer is genuinely unknown and gets reported as a gap.
