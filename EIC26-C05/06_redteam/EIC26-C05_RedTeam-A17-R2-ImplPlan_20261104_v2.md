# Red-team review of the A17-R2 Implementation Plan (v2)

Reviewed: `EIC26-C05-A17-R2_Implementation_Plan_EN.md/.pdf` (10 pages) and the L1 disposition. Line numbers refer to the R2 MD.

## Verdict

**The plan is ready to submit.** Four of the six v1 changes are in, and one is in after L1 corrected a date:
- the opening paragraph now states quantified outputs and the acceptance thresholds;
- every milestone has numeric pass criteria;
- the Gantt is shaded, with a milestone row;
- Qin Yu leads WP4;
- the TRL column reads 6 / 7 / 7 / 8 / n/a / 9;
- WP5 names the IP filing windows.

L1's correction is right: the 2025 PCT family's US national phase falls at 30 months (21 Jan 2028, M10) and its EP regional phase at 31 months (21 Feb 2028, M11). R2's "January–February 2028 entry windows" is correct, and v1's single "January 2028" date was not.

**Risk ratings.** I accept L1's decision to keep the ratings. A planned fallback does not make sensor failure unlikely, and HPE being the CETP site does not yet document EIC access. The ratings are defensible as they stand.

**Layout.** The page-8 margin problem is fixed and the document holds at 10 pages.

Nothing below is a blocker. If time is short, items 1 and 2 are the only ones worth making.

## Remaining edits (optional, under 15 minutes)

1. **l.11:** delete "the grant agreement determines the contractual start" and "Existing-platform reference deliveries in 2027 follow their configuration releases." Both are internal remarks and add nothing for the evaluator.
2. **WP4 closing paragraph:** replace "The released operating domain records demonstrated performance and coverage gaps. The industrial unit and laboratory fixtures have separate operating logs." with "The released operating domain states the performance demonstrated."
3. **WP3 closing paragraph:** delete "Separate schedules record test-running hours, fixture occupancy and paid attendance."
4. **Gantt:** several WP3, WP4 and WP6 cells are merged vertically across rows, so one shaded block covers two tasks with different windows. Unmerge them so each row shows only its own months. This is cosmetic; it adds no rows or pages.

## Consistency with Part B (do at merge)

- **Part B §3.3 evidence-gate table:** copy the numeric criteria from Implementation Plan table 3.1d in short form so both documents use the same thresholds.
  - MS3: six batches qualified; 1,200 independent fixture-hours.
  - MS4: 4,000 internal endurance hours; safety-critical findings closed.
  - MS5: 1,600 field hours; at least 60% less electricity and 40% less make-up water at matched service.
- **Part B §1.3:** optionally add one sentence: "National and regional phase entries of the 2025 PCT family fall in January–February 2028 and are decided in WP5."
- **Already consistent:** WP4 lead Qin, with the field engineer from M7, matches the Part B recruitment table (no change needed).
