#!/usr/bin/env python3
"""Build the Clear Conscience Consulting grant pipeline workbook."""

import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

FONT = "Arial"

BLUE = "0000FF"      # hardcoded inputs / editable assumptions
BLACK = "000000"     # formulas
YELLOW = "FFFF00"    # cells the user should fill in

HDR_FILL = PatternFill("solid", fgColor="1F3864")
TIER_FILLS = {
    "A": PatternFill("solid", fgColor="C6E0B4"),
    "B": PatternFill("solid", fgColor="D9E1F2"),
    "C": PatternFill("solid", fgColor="FFF2CC"),
    "D": PatternFill("solid", fgColor="F8CBAD"),
    "E": PatternFill("solid", fgColor="E7E6E6"),
}
YELLOW_FILL = PatternFill("solid", fgColor=YELLOW)

THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

CUR = '$#,##0;($#,##0);-'
PCT = '0%;-0%;-'

# rank, name, funder, type, deadline(date|None), dl_type, low, high, prob, tier, note
ROWS = [
    (1, "JOIN! Grants", "OceanFirst Foundation", "Private foundation",
     None, "Rolling", None, 2500, 0.50, "A",
     "NJ funder, minimal application, no cycle risk. Fastest possible first win."),
    (2, "Neighborhood Partners Program", "PSEG Foundation", "Private foundation",
     dt.date(2027, 6, 30), "Full", 500, 15000, 0.40, "A",
     "Utility foundation; service territory covers the priority counties."),
    (3, "Empowerment Grant", "Provident Bank Foundation", "Private foundation",
     dt.date(2027, 4, 30), "Full", 5000, 25000, 0.35, "A",
     "CRA-driven giving favors local community orgs. Award size fits budget."),
    (4, "Project ATLAS", "NJ Dept. of State, Office of Faith Based Initiatives",
     "State / regional", dt.date(2027, 2, 26), "Full", None, 10000, 0.35, "A",
     "State office that exists to fund grassroots community work."),

    (5, "General Operating and Project Grants", "Partners For Health Foundation",
     "Private foundation", dt.date(2027, 2, 23), "Pre-proposal", None, None, 0.30, "B",
     "Essex County health funder. GENERAL OPERATING support - rare and worth more "
     "per dollar than restricted money. Amount unpublished; confirm range. Verify "
     "the org sits inside its service footprint."),
    (6, "Standard Grants", "Healthcare Foundation of New Jersey", "Private foundation",
     dt.date(2026, 11, 19), "Full", 35000, None, 0.25, "B",
     "3 of 4 priority counties in footprint; reported behavioral health emphasis. "
     "OPEN QUESTION: does a non-Federation-affiliated org qualify under the "
     "'vulnerable populations elsewhere in Essex, Morris, Union' clause?"),
    (7, "Empower New Jersey Grant", "Community Foundation of New Jersey",
     "Private foundation", dt.date(2026, 9, 30), "Full", 50000, 100000, 0.20, "B",
     "Best effort-to-return balance on the list. If only one thing gets written "
     "this fall, this is it."),
    (8, "VAWA Competitive Grant Program", "NJ Dept. of Law & Public Safety",
     "State / regional", dt.date(2027, 6, 15), "Full", None, 75000, 0.20, "B",
     "Maps onto stated DV prevention work. Will want demonstrated DV programming, "
     "not just adjacent capacity."),
    (9, "Awards for Advancing Minority Mental Health",
     "American Psychiatric Association Foundation", "Private foundation",
     dt.date(2027, 1, 31), "Full", 5000, 5000, 0.20, "B",
     "National pool but tiny award. Real value is the credential, not the cash."),

    (10, "Pathways to Recovery - Round 2 NGO", "NJ Dept. of Labor & Workforce Dev.",
     "State / regional", dt.date(2027, 3, 26), "LOI", None, 1000000, 0.15, "C",
     "HIGHEST EXPECTED VALUE on the list. NJ-only pool, NGO-specific track, "
     "opioid focus matches directly. Ask well under the cap."),
    (11, "Pathways to Recovery (general)", "NJ Dept. of Labor & Workforce Dev.",
     "State / regional", dt.date(2027, 3, 5), "LOI", None, 1000000, 0.12, "C",
     "Same program, broader applicant pool than the NGO track."),
    (12, "Champions in Action", "Citizens Charitable Foundation", "Private foundation",
     dt.date(2026, 9, 30), "Full", 50000, 50000, 0.12, "C",
     "Selects very few recipients per cycle, usually themed. Check this round's theme."),
    (13, "Specific Population Community Grant", "NJ Dept. of Health",
     "State / regional", dt.date(2027, 5, 18), "LOI", None, 500000, 0.12, "C",
     "Justice-involved qualifies as a specific population. Award size demands "
     "strong fiscal infrastructure."),
    (14, "Job Opportunities for Building Success", "NJ Dept. of Labor & Workforce Dev.",
     "State / regional", dt.date(2027, 3, 4), "LOI", None, 1000000, 0.10, "C",
     "Reentry employment framing works, but competitors are established workforce "
     "development agencies."),

    (15, "Second Chance Act - Family-Based SUD Treatment", "US DOJ, BJA", "Federal",
     dt.date(2026, 9, 24), "Full", None, 1000000, 0.06, "D",
     "BEST MISSION FIT on the entire list. Barriers: national competition, "
     "3x-budget award, and the 'treatment provider' question (org refers out to "
     "IOP rather than treating directly). Pursue as partner/sub-awardee."),
    (16, "Second Chance Act - Reentry Education & Employment", "US DOJ, BJA", "Federal",
     dt.date(2026, 9, 24), "Full", None, 1000000, 0.05, "D",
     "Federal reentry competitions draw established national providers with prior "
     "DOJ awards. Pursue as partner/sub-awardee."),
    (17, "Project Grant", "State Justice Institute", "Federal",
     dt.date(2026, 11, 1), "Full", None, 300000, 0.05, "D",
     "SJI funds court systems. Realistic path is as named program partner on a "
     "court-led application - the recovery court relationship could support that."),
    (18, "Family foundations (Scripps, Kim/Kayasa, Bernau, Scaife)", "Various",
     "Private foundation", None, "Rolling / 2027", None, None, 0.10, "D",
     "Priorities unpublished; many small family foundations are effectively "
     "invitation-only. Pull Form 990s before writing - 15 min each tells you "
     "whether they accept unsolicited requests at all."),

    (0, "Therapeutic Giving: Neuroscience - Local & Regional",
     "Johnson & Johnson Innovative Medicine", "Private foundation",
     dt.date(2027, 5, 31), "Full", None, None, 0.12, "C",
     "Corporate giving with a local/regional track; mental health sits under its "
     "neuroscience umbrella. Pharma giving tends to favor established orgs and "
     "clinically-adjacent work, which caps the odds. Amount unpublished."),
    (0, "Citizens Philanthropic Foundation: Workforce Development",
     "Citizens Philanthropic Foundation", "Private foundation",
     dt.date(2027, 5, 22), "Full", None, None, 0.12, "C",
     "Reentry employment is a workable framing. Note this is the same corporate "
     "family as Champions in Action - a relationship built through one may help "
     "the other. Amount unpublished."),
    (0, "Get Out and Get Active Grant", "Anxiety & Depression Initiative",
     "Private foundation", dt.date(2027, 4, 27), "Full", None, 10000, 0.10, "C",
     "PARTIAL FIT: this funder targets physical activity as an intervention for "
     "anxiety and depression. The org does psychoeducation and emotional wellness, "
     "not movement programming - a competitive application would need a genuine "
     "activity-based component, not a relabelling of existing workshops."),
    (0, "JAMS Foundation NAFCM Mini-Grant Program", "JAMS Foundation",
     "Private foundation", dt.date(2027, 2, 23), "LOI", None, 15000, 0.08, "D",
     "ELIGIBILITY RISK: administered with the National Association for Community "
     "Mediation and generally aimed at NAFCM member community mediation centers. "
     "The org is not a mediation center. Anger management and healthy communication "
     "workshops map to the subject matter, but confirm whether non-member "
     "organizations can apply at all before spending time here."),
    (0, "Citizens Philanthropic Foundation: Financial Empowerment",
     "Citizens Philanthropic Foundation", "Private foundation",
     dt.date(2026, 12, 1), "Pre-proposal", None, None, 0.08, "D",
     "Weakest fit of the five: this track funds financial literacy and coaching, "
     "which the org does not currently deliver. Nearest deadline of the group, but "
     "would require standing up a service line rather than describing one."),

    (0, "SNAP STEPS", "NJ Dept. of Labor & Workforce Dev.", "State / regional",
     dt.date(2026, 9, 12), "LOI", None, 500000, None, "E",
     "VERIFY FIRST: near-term LOI. Overlap with reentry population is real but "
     "the org would need a workforce services track record."),
    (20, "Preventive Health Services Grant Program", "NJ Dept. of Health",
     "State / regional", dt.date(2026, 11, 17), "Full", None, 535000, None, "E",
     "VERIFY FIRST: confirm community nonprofits are eligible applicants rather "
     "than local health departments."),
    (21, "Omnibus Eviction and Homelessness Prevention", "NJ Dept. of Community Affairs",
     "State / regional", dt.date(2026, 12, 2), "Full", None, None, None, "E",
     "VERIFY FIRST: housing stability is adjacent to reentry wraparound; founder's "
     "lived experience with homelessness is relevant framing. Second RFP 2026-12-09."),
    (22, "Chronic Disease Prevention Grant", "NJ Dept. of Health", "State / regional",
     dt.date(2026, 12, 23), "LOI", None, 150000, None, "E",
     "VERIFY FIRST: often targeted at diabetes/cardiovascular - confirm behavioral "
     "health is in scope this cycle."),
]

# Rank is derived, never hand-maintained: sort by estimated win probability
# descending, with unscored "verify first" rows last, then renumber. This keeps
# the sheet consistent whenever a row is added or a score changes.
ROWS.sort(key=lambda r: (r[8] is None, -(r[8] or 0)))
ROWS = [(i, *row[1:]) for i, row in enumerate(ROWS, start=1)]

HEADERS = [
    ("Rank", 6), ("Opportunity", 42), ("Funder", 36), ("Type", 17),
    ("Deadline", 12), ("Stage", 13), ("Days Left", 10),
    ("Amount Low", 13), ("Amount High", 13), ("Planning Amount", 16),
    ("Est. Win %", 11), ("Expected Value", 15), ("Tier", 6),
    ("Status", 16), ("Owner", 14), ("Next Action", 22), ("Notes / Watch-outs", 80),
]

wb = Workbook()

# ---------------------------------------------------------------- Pipeline
ws = wb.active
ws.title = "Pipeline"

ws["A1"] = "Clear Conscience Consulting - Grant Pipeline"
ws["A1"].font = Font(name=FONT, size=15, bold=True, color="1F3864")
ws["A2"] = ("Ranked most to least likely to be awarded. Estimates are judgment, not "
            "measured win rates - see the Method tab. Yellow cells are yours to fill in; "
            "blue numbers are assumptions you can change.")
ws["A2"].font = Font(name=FONT, size=9, italic=True, color="595959")
ws.merge_cells("A2:Q2")
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[2].height = 26

HDR_ROW = 4
for idx, (title, width) in enumerate(HEADERS, start=1):
    c = ws.cell(row=HDR_ROW, column=idx, value=title)
    c.font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER
    ws.column_dimensions[get_column_letter(idx)].width = width
ws.row_dimensions[HDR_ROW].height = 30
ws.freeze_panes = "C5"

first = HDR_ROW + 1
for i, (rank, name, funder, gtype, dl, dlt, low, high, prob, tier, note) in enumerate(ROWS):
    r = first + i
    ws.cell(row=r, column=1, value=rank)
    ws.cell(row=r, column=2, value=name)
    ws.cell(row=r, column=3, value=funder)
    ws.cell(row=r, column=4, value=gtype)

    dcell = ws.cell(row=r, column=5, value=dl)
    if dl:
        dcell.number_format = "yyyy-mm-dd"
    ws.cell(row=r, column=6, value=dlt)

    # Days Left - guard the blank-deadline rows so they render clean, not #VALUE!
    ws.cell(row=r, column=7, value=f'=IF(E{r}="","",E{r}-TODAY())')

    ws.cell(row=r, column=8, value=low)
    ws.cell(row=r, column=9, value=high)

    # Planning amount: midpoint when both bounds known; half the cap for an
    # "up to X" ceiling, since a small org should not request the maximum.
    ws.cell(row=r, column=10, value=(
        f'=IF(AND(H{r}<>"",I{r}<>""),AVERAGE(H{r}:I{r}),'
        f'IF(I{r}<>"",I{r}*$C$3,IF(H{r}<>"",H{r},"")))'
    ))
    ws.cell(row=r, column=11, value=prob)
    ws.cell(row=r, column=12, value=f'=IF(OR(J{r}="",K{r}=""),"",J{r}*K{r})')
    ws.cell(row=r, column=13, value=tier)

    for col in (14, 15, 16):
        ws.cell(row=r, column=col).fill = YELLOW_FILL
    ws.cell(row=r, column=17, value=note)

    for col in range(1, 18):
        c = ws.cell(row=r, column=col)
        c.border = BORDER
        c.font = Font(name=FONT, size=10,
                      color=BLUE if col in (8, 9, 11) else BLACK)
        c.alignment = Alignment(
            vertical="top",
            wrap_text=col in (2, 3, 17),
            horizontal="center" if col in (1, 5, 6, 7, 13) else None,
        )
    for col in (8, 9, 10, 12):
        ws.cell(row=r, column=col).number_format = CUR
    ws.cell(row=r, column=11).number_format = PCT
    ws.cell(row=r, column=13).fill = TIER_FILLS[tier]
    ws.row_dimensions[r].height = 46

last = first + len(ROWS) - 1

tot = last + 2
ws.cell(row=tot, column=2, value="TOTAL PIPELINE").font = Font(name=FONT, size=11, bold=True)
ws.cell(row=tot, column=10, value=f"=SUM(J{first}:J{last})")
ws.cell(row=tot, column=12, value=f"=SUM(L{first}:L{last})")
for col in (10, 12):
    c = ws.cell(row=tot, column=col)
    c.number_format = CUR
    c.font = Font(name=FONT, size=11, bold=True)
    c.border = Border(top=Side(style="double", color="1F3864"))
ws.cell(row=tot, column=13, value="<- risk-weighted").font = Font(
    name=FONT, size=9, italic=True, color="595959")

note_r = tot + 2
ws.cell(row=note_r, column=2, value=(
    "Expected Value = Planning Amount x Est. Win %. It is the risk-weighted worth of "
    "pursuing an item, NOT a forecast of what you will receive. Sorting by it gives a "
    "different order than sorting by likelihood - both are worth looking at."))
ws.cell(row=note_r, column=2).font = Font(name=FONT, size=9, italic=True, color="595959")
ws.merge_cells(start_row=note_r, start_column=2, end_row=note_r, end_column=17)
ws.cell(row=note_r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[note_r].height = 28

# The "up to X" haircut lives in C3 so it is a lever, not a magic number.
ws["B3"] = "Planning haircut on 'up to' award caps:"
ws["B3"].font = Font(name=FONT, size=9, italic=True, color="595959")
ws["B3"].alignment = Alignment(horizontal="right")
ws["C3"] = 0.5
ws["C3"].font = Font(name=FONT, size=10, bold=True, color=BLUE)
ws["C3"].number_format = PCT
ws["C3"].fill = YELLOW_FILL
ws["C3"].border = BORDER
ws["D3"] = "of the cap, since a small org should not request the maximum"
ws["D3"].font = Font(name=FONT, size=9, italic=True, color="595959")

dv = DataValidation(
    type="list",
    formula1='"Not started,Researching,Drafting,Submitted,Awarded,Declined,Skipped"',
    allow_blank=True,
)
ws.add_data_validation(dv)
dv.add(f"N{first}:N{last}")

ws.auto_filter.ref = f"A{HDR_ROW}:Q{last}"

# ------------------------------------------------------------ Screened Out
ws2 = wb.create_sheet("Screened Out")
ws2["A1"] = "Screened out - and why"
ws2["A1"].font = Font(name=FONT, size=14, bold=True, color="1F3864")
ws2["A2"] = ("Roughly 26 of the ~80 listed opportunities were removed. Reasons are stated "
             "so any of them can be overruled.")
ws2["A2"].font = Font(name=FONT, size=9, italic=True, color="595959")

SCREENED = [
    ("Research institution required",
     "All NIH mechanisms (R61/R33, P50, P30, K12, R25, U01, NIDA Core Center, HEAL "
     "IMPOWR/BEACON, Pilot & Feasibility, Specialized Alcohol Research Centers, AIDS "
     "Research Center, TCORS); CDC research cooperative agreements (Improving Linkage "
     "to Care, Nonfatal Overdoses in EDs, Core SIPP, Alcohol Epidemiology, NNPTC); "
     "PCORI Engagement Award; BJS CHRARP; National Research Center for Promoting Work "
     "and Strong Families; Applied Drug Policy Research Experiences; NJ Commission on "
     "Brain Injury Research; DoD/Army TBI awards",
     "Require an academic or research institution, a named principal investigator, and "
     "IRB infrastructure the org does not have."),
    ("State or government applicant only",
     "Comprehensive Suicide Prevention Program for States; SSUS State STD Program; SSUS "
     "HIV Services; Public Health Emergency Preparedness LINCS; Public Health Leadership "
     "and Workforce Development; Comprehensive Cancer Control (both listings); Diabetes "
     "Capacity Building; Rural Health Transformation ($27.5M); 988 Lifeline Administrator "
     "($231M); Disaster Distress Helpline",
     "Applicant must be a state agency or a designated statewide administrator."),
    ("National TTA-provider scale",
     "FY2026 Drug Court Training and Technical Assistance ($6M); RSAT for State Prisoners "
     "TTA (both listings); CSBG Essentials for Improved Outcomes; CSBG Communities of "
     "Practice; Center for SUD Pharmacotherapeutics",
     "National training-and-TA contracts awarded to large established intermediaries. "
     "CSBG additionally routes through designated Community Action Agencies."),
    ("Geography or topic mismatch",
     "Rural Opioid Technical Assistance Centers; Rural Communities Opioid Response "
     "(Evaluation, and Community Systems Development); Consolidated ABS/IELCE; Community "
     "Library Adult Literacy; Affordable Housing and Supportive Services Demonstration; "
     "Comer Family Foundation Syringe Service Program",
     "The four priority counties are not rural; adult literacy and housing development "
     "are outside scope; syringe services are not a current program."),
    ("Not applicable",
     "HFNJ Renewal Grants (2026-11-19)",
     "Open only to existing HFNJ grantees. Becomes relevant after a first HFNJ award."),
]

for i, (h, w) in enumerate([("Reason", 30), ("Opportunities", 95), ("Explanation", 60)], 1):
    c = ws2.cell(row=4, column=i, value=h)
    c.font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
    c.fill = HDR_FILL
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = BORDER
    ws2.column_dimensions[get_column_letter(i)].width = w

for i, (reason, opps, why) in enumerate(SCREENED):
    r = 5 + i
    for col, val in ((1, reason), (2, opps), (3, why)):
        c = ws2.cell(row=r, column=col, value=val)
        c.font = Font(name=FONT, size=10, bold=(col == 1))
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = BORDER
    ws2.row_dimensions[r].height = 100

# ------------------------------------------------------------------ Method
ws3 = wb.create_sheet("Method")
ws3.column_dimensions["A"].width = 34
ws3.column_dimensions["B"].width = 92

blocks = [
    ("HEAD", "How these estimates were made", None),
    ("BODY", "What they are",
     "Judgment estimates, not calibrated statistics. No public dataset gives per-program "
     "win rates for an organization of this profile, and any number claiming otherwise is "
     "invented. They are a defensible ordering, useful for deciding what to write first - "
     "not probabilities to report to a board as fact."),
    ("BODY", "On the 10-15% figure",
     "That is a fair average across all grantseeking, but applied uniformly it misdirects "
     "effort. Real odds here span roughly 50% down to low single digits, and they run "
     "close to INVERSE to award size. A flat rate would point at the $1M federal awards, "
     "which is exactly where a $300k organization has the worst odds."),
    ("HEAD", "The seven factors behind each estimate", None),
    ("BODY", "1. Eligibility certainty",
     "Is the org clearly an eligible applicant, or is that an open question?"),
    ("BODY", "2. Geographic restriction",
     "The single biggest lever. A funder limited to Essex/Union/Somerset competes among "
     "dozens of applicants, not thousands."),
    ("BODY", "3. Award-to-budget ratio",
     "Requesting 3x annual budget triggers capacity scrutiny. Requesting 5-20% does not."),
    ("BODY", "4. Competitive pool", "Local foundation vs. national federal competition."),
    ("BODY", "5. Track-record requirements",
     "Prior federal awards, CPA audit, outcome data systems, years in operation."),
    ("BODY", "6. Application burden",
     "Staff time to produce a genuinely competitive submission."),
    ("BODY", "7. Mission fit", "How little translation the funder has to do to see it."),
    ("HEAD", "Two things the ranking does not show", None),
    ("BODY", "Expected value points elsewhere",
     "A 15% shot at $500k is worth more in expectation than a 50% shot at $2,500. "
     "Pathways to Recovery - Round 2 NGO is the highest-EV item on the list. Likelihood "
     "and value are different questions; the Expected Value column answers the second."),
    ("BODY", "Federal cash-flow risk",
     "Most federal grants reimburse after spending. A $300k organization winning $1M on a "
     "cost-reimbursement basis must front payroll for months before the first draw. "
     "Winning the Second Chance Act awards without a line of credit or bridge funding "
     "could create a worse problem than losing them."),
    ("HEAD", "Suggested sequencing", None),
    ("BODY", "Now - September",
     "Submit Tier A (#1-#4 are days of work, not weeks) plus CFNJ Empower NJ (#7). Puts "
     "real wins on the board fast."),
    ("BODY", "Fall", "HFNJ (#6) by Nov 19, after resolving the affiliation question."),
    ("BODY", "September 24 decision",
     "Pursue both Second Chance Act tracks as PARTNER or SUB-AWARDEE under a larger lead "
     "applicant rather than solo. Same mission value, far better odds, no cash-flow "
     "exposure - and the recovery court and IDRC relationships are exactly what a lead "
     "applicant needs."),
    ("BODY", "Winter into 2027",
     "The LOI cycle (#10, #13, #14). With two or three 2026 wins to cite as track record, "
     "these move up a tier. The compounding matters more than any single application - "
     "funders ask who else has funded you, and Tier A answers that cheaply."),
    ("HEAD", "Colour key", None),
    ("BODY", "Blue numbers",
     "Assumptions you can change - award bounds and win-probability estimates."),
    ("BODY", "Yellow cells",
     "Yours to fill in: Status, Owner, Next Action, and the planning haircut in C2 on the "
     "Pipeline tab."),
    ("BODY", "Black numbers", "Formulas. Changing them breaks the totals."),
    ("HEAD", "Source and caveats", None),
    ("BODY", "Where the list came from",
     "An Instrumentl opportunity-match export supplied by the org on 2026-08-19. "
     "Deadlines and amounts are as listed there. Deadlines without a year were read as "
     "2026. Tier/probability/fit assessments are this system's, not the funders'."),
    ("BODY", "Verify before writing",
     "An earlier web-search run recorded HFNJ Standard Grants as closing 2026-08-28; the "
     "export shows 2026-11-19. Confirm every deadline at the source before building an "
     "application plan around it."),
]

r = 1
for kind, a, b in blocks:
    if kind == "HEAD":
        c = ws3.cell(row=r, column=1, value=a)
        c.font = Font(name=FONT, size=12, bold=True, color="1F3864")
        ws3.row_dimensions[r].height = 24
        r += 1
    else:
        ca = ws3.cell(row=r, column=1, value=a)
        ca.font = Font(name=FONT, size=10, bold=True)
        ca.alignment = Alignment(wrap_text=True, vertical="top")
        cb = ws3.cell(row=r, column=2, value=b)
        cb.font = Font(name=FONT, size=10)
        cb.alignment = Alignment(wrap_text=True, vertical="top")
        ws3.row_dimensions[r].height = max(30, 13 * (len(b) // 92 + 1) + 14)
        r += 1
    r += 0

OUT = "/home/user/daily-brain/grant_search/data/grant_pipeline.xlsx"
wb.save(OUT)
print("wrote", OUT)
