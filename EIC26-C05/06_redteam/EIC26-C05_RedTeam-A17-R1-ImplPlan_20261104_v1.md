# Red-team review of the A17-R1 Implementation Plan

Reviewed: `EIC26-C05-A17-R1_Implementation_Plan_EN.md/.docx/.pdf` (10 pages, official template) and the CN notes. Line numbers refer to the MD file. All replacement text is final wording.

## Verdict

The plan is complete and consistent with Part B R5:
- tables 3.1a–3.1j are all present;
- PM, costs, months and asset figures close exactly;
- task percentages, roles and quantities match the template's request for activities, effort split and who does the work.

Evaluators score this annex mainly on whether resources match tasks, whether milestones are verifiable and whether risks are credibly managed. Six changes would lift it from "adequate" to "very good". None of them changes a number in the budget.

1. **Remove about 20 defensive or internal sentences.** They explain what the plan is not ("not a second service", "not total company sales", "does not certify later work"). They are listed below with replacements.
2. **Give milestones numeric pass criteria.** The figures already exist in the plan (1,600 field hours, ≥60% electricity, ≥40% water, six batches, 1,200 independent hours). At the moment the milestones read as "records support…".
3. **Differentiate the risk ratings.** Seven of eight risks are "L: Medium; S: High". After the mitigations described, several are Low likelihood or Medium severity. Uniform ratings read as templated and suggest a high-risk project.
4. **Make the Gantt visual.** Shade active cells instead of typing month numbers, and merge the five "same unit / fixture" resource rows into the task rows.
5. **Use a named person as WP4 lead.** WP4 starts at M6, but its stated lead (the field engineer) is hired at M7. Make Qin Yu the lead, with the field engineer executing.
6. **State concrete TRL targets per WP and two IP filing milestones.** These are decisive statements in place of "towards 8" and "applications remain pending".

## 1. Opening summary (replace l.7–9)

> Savery Tech will turn its TRL6 AirTransformer machine into a manufacturable, serviceable product qualified at TRL8 by M24 (March 2029). The action delivers six qualified CAU contactor batches, 4,000 hours of internal and 1,200 hours of independent endurance testing, five climate/load campaigns, a conformity file and 1,600 hours of field operation at the HPE site. Acceptance requires at least 60% less electricity and 40% less external make-up water than compression cooling at matched service.
>
> WP1 fixes the engineering and verification baseline; WP2 qualifies manufacture and batch quality; WP3 validates reliability, industrial controls and conformity; WP4 qualifies the product in climate tests and field operation; WP5 manages delivery, data, IP and exploitation. WP6, funded by the EIC investment and Seed, builds manufacturing and service capacity from M12 to M36 for deployment towards TRL9. M1 is planned for April 2027.

## 2. Gantt (l.11–38)

- Shade active cells with one colour per WP (WP1–WP5 grant, WP6 investment in a distinct colour) and leave them empty of text. Keep the month ranges in the first column, which already lists them.
- Merge the five resource rows into their tasks:
  - "Same industrial unit" (three rows) goes into T4.2 and T4.3.
  - "Separate internal fixture" goes into T3.2.
  - "Independent fixture" goes into T3.2.
  - This saves about six rows.
- Add one diamond row for milestones (MS1–MS5, IM1–IM2) instead of the two text rows.
- Replace the note at l.38 with: "Shaded cells show active months. One industrial unit completes five 12-day climate campaigns (M10–M14) before field installation at M16; the internal and independent endurance fixtures run in parallel."

## 3. Tables 3.1a / 3.1aa

| Line | Replace | With |
|---|---|---|
| l.44 Targeted TRL | "TRL6 baseline; route to 8" | "6 (baseline)" |
| l.45 | "Manufacturing evidence towards 8" | "7" |
| l.46 | "Reliability and conformity towards 8" | "7" |
| l.47 | "Target TRL8" | "8" |
| l.48 | "Supports TRL6-8" | "n/a" |
| l.54 | "Released-product path to TRL9" | "9" |
| l.56 | "TRLs describe planned configuration-specific targets, not maturity already achieved." | delete. Keep "Grant total: 258 PM, M1–M24; WP6 resources and costs are outside the grant." |
| l.58 last sentence | "Task percentages below represent each WP's company effort, sum to 100%, and do not redistribute the fixed role PM or costs." | "Task percentages give each task's share of WP effort." |

The TRL 7 rationale for WP2/WP3: by M18–M21 the manufactured configuration has run climate campaigns and entered field operation (M17), which is a system prototype in an operational environment. If you prefer to be conservative, write "6–7".

## 4. Work package descriptions (3.1b)

**WP2**
- T2.2: keep "Route-specific rights review and disposition precede each affected transfer"; delete ", including transfers before M12".
- T2.4: delete the last sentence ("Rights disposition is checked before affected transfer or release."), which repeats T2.2.

**WP3**
- T3.2: replace "Failed/excluded periods, uncertainty and extrapolation limits remain in the record. The M18 dataset is cumulative/interim; subsequent corrective tests and assessment enter the M21 dossier." with "Results feed the M18 reliability record and the M21 conformity dossier."
- Last paragraph: delete "Test-running hours, fixture occupancy and paid attendance are scheduled separately; their totals are not a single-machine lifetime or technician-hours claim."

**WP4**
- Lead line (l.112): "Lead Qin Yu with the field deployment engineer (from M7) and Ina Wang".
- T4.2: delete ", not a second service or unit" and ", without recalling the onsite unit for overlapping climate tests".
- T4.3: replace "Matched baseline/upgrade comparisons retain measured boundaries, failed tests and actual coverage." with "Matched baseline and upgrade comparisons use the full measurement boundary."
- T4.3: replace "Initial water use is … separately balanced." with "Recovered water is treated for non-aerosol equipment cleaning; external make-up and recovered water are metered separately."
- T4.4: replace "The M20 results are interim; final hours, corrective work and acceptance enter the M24 dossier. Independent tests fill uncovered conditions alongside actual field operation." with "Interim results at M20 and the final field record at M24 feed the qualification decision; independent tests cover conditions the field season does not reach."
- Closing paragraph: "Qualification tests the targets of 60–70% less electricity and 40–60% less external make-up water at matched cooling service. The released operating domain states the conditions and uncertainty demonstrated." Delete the rest.

**WP5**
- Delete "Scientific-board advice carries no automatic project PM."
- T5.2: replace "The 2025/2026 applications remain pending; contractor/software/background rights are recorded." with "T5.2 decides foreign filings for the 2026 application by 9 October 2027 (M7), and national and regional phase entries of the 2025 PCT family by January 2028 (M10), covering Europe and North America. Contractor, software and background rights are recorded."
- T5.3: delete "Later CETP outputs are not M24 prerequisites."

**WP6**
- Delete "Mobilisation from April 2027 follows available cash and confirmed receipts." (it is covered by the risk table).
- T6.1: delete the last sentence ("Existing-platform reference deliveries…").
- T6.3: delete "These packages are not total company sales or uniform 100 kW machines."
- T6.4: delete "WP6 supports the wider company rollout within its defined scope."
- Check the DOCX for the apostrophe in "configuration's". The MD shows it as an HTML entity.

## 5. Milestones (3.1d): numeric pass criteria

| ID | Verification (replace column text) |
|---|---|
| MS1 | Product specification, baseline configuration, verification protocol and test plan approved (D1.1, D1.2, D3.1). |
| MS2 | Drawings and process window released; first four batches (M4–M10) assessed against the specification; route-specific rights disposition recorded. |
| MS3 | Six batches qualified and twelve contactors released; 1,200 independent fixture-hours completed; corrective actions recorded. |
| MS4 | Conformity file complete and all safety-critical findings closed; industrial software released after regression testing. |
| MS5 | 1,600 field operating hours logged; at least 60% less electricity and 40% less external make-up water at matched cooling service; TRL8 qualification decision signed. |
| IM1 | Serial tooling commissioned, manufacturing partner qualified, production release issued. |
| IM2 | Five installation/service packages delivered; application engineer and two technicians in post. |

Below the table, delete "A gate does not certify later work as complete. IM1/IM2 are investment milestones; initial company deliveries use their own released versions." Keep "Frédéric signs each gate with the responsible WP lead."

## 6. Risks (3.1e): differentiated residual ratings

| Risk | Residual L / S |
|---|---|
| Recruitment/supply delay | Medium / High |
| CAU inconsistency/degradation | Medium / High |
| Rating/endurance not reproduced | Medium / Medium |
| Control or sensor failure | Low / Medium (independent limits and deterministic fallback) |
| Field access/coverage shortfall | Low / High (HPE site confirmed; independent tests as backup) |
| Rights/conformity require changes | Low / High |
| Delayed funding/receipts | Medium / High |
| CETP overlap/unavailable input | Low / Medium |

In the field-access row, replace "Retain actual installation/operation; supplement missing conditions independently and retest gaps." with "Independent climate tests cover conditions the field season does not reach." In the CETP row, delete "Later CETP outputs stay outside the M24 critical path."

## 7. Cost tables (3.1g, 3.1h): small wording fixes

- l.215: keep "Documented offer comparisons and conflict-of-interest checks establish best value for money. Savery retains architecture, core design, integration, interpretation and release responsibility." Shorten the last sentence to "Facility access, routine assays and calibration are purchased services (3.1h)."
- l.226: replace "no duplicated CETP rent" with "dedicated to EIC tasks".
- l.234: replace "existing instruments are not repurchased" with "complements existing instruments".
- l.236: replace "avoids a new general synthesis laboratory" with "uses existing laboratory capacity".

## 8. Deliverables (3.1c), optional

All sixteen deliverables are SEN. Making D5.2 (dissemination, exploitation and communication plan) PU signals openness at no IP cost. Optionally, add a public summary of the qualification results at M24 under WP5, if the page budget allows.

## Page budget

The edits above remove about 260 words and add about 170, mostly in the opening summary, the T5.2 filing dates and the milestone criteria. The Gantt merge frees about six table rows. The document stays within 10 pages.
