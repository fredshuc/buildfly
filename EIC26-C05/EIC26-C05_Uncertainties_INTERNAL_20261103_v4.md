# EIC26-C05 internal uncertainty register (not for submission)

3 Nov 2026, v2 (after A16-R3). Every limitation, condition and open check removed from the proposal text is kept here. Nothing in this file goes into Part B, the pitch or the Portal. Each item states the risk, what the proposal now says, and the action needed, if any. Items marked **Before submit** should be closed by 10:00 on 4 Nov if possible. All other items can wait for the interview or the grant agreement.

## Technology and performance

1. **COP 20 test basis.**
   - Proposal: "sensible-cooling COP of 20, measured under EN conditions with 60 °C waste heat (Annex)".
   - Open: the exact EN standard number and the annex title/ID. The 2025 ESR cited EN 13141-7 and ASHRAE 143, so check which applies to this test.
   - Boundary: circulation pumps sit outside the test boundary because the heat loops are connected at static pressure. The proposal states this in one sentence.
   - **Before submit:** insert the annex name in packages B and D.
2. **Installed COP 8–20.** Applicant statement. The lower end depends on site pumping and adjacent components. All headroom (208–283 kW/MW) and electricity-reduction (62–85% against EER 3) figures follow from this range. Against an EER 4 reference, the reduction is 50–80%.
3. **Sorbent in the 2025 tested machine.** Not stated in the proposal. If it was not CAU, the CAU contactor is a qualified upgrade, which the TRL text already reflects. Expect the question at interview.
4. **Heating COP 6–10 (2026 machine).** The proposal says "reaches". If this is a design or model value rather than a measurement, change it to "is designed for a heating COP of 6 to 10". **Before submit:** confirm.
5. **Supply air 16–20 °C at 9–11 g/kg; make-up water 40–60% lower.** These figures were carried from 2025 and are stated as product rating and water reduction. Open: the reference configuration for the water figure (evaporative cooling tower assumed) and the rating-point inlet conditions.
6. **"No fluorinated refrigerant".** Stated for the cooling cycle, where water is the working fluid. Confirm there is no F-gas anywhere in the product or on the auxiliary circuits.
7. **Heat availability.** If the regeneration heat came from the condenser of a compressor that AirTransformer displaces, that heat would disappear. Liquid-cooled racks and independent industrial waste heat avoid this. Site screening must confirm heat availability during cooling hours.
8. **Annual savings vs. heatwave hours.** In northern Europe free cooling covers many hours, so annual savings depend on how many hours compression is actually displaced. The proposal states the 8,000 h data-centre case. Expect this question from data-centre experts.

## Product definition and market

9. **Unit in the forecast.** Superseded by item 33. (Original note: the proposal defined a forecast unit as a 100 kW package of five 20 kW modules.) This is inferred from €110k equipment at €1,100/kW. If the BP counts something else (a module, a container), the €/kW, MW-per-year and SOM-in-MW statements change. **Before submit:** check the BP unit definition.
10. **TAM.** Applicant: "hundreds of billions of euros". Copy the BP figure and source into package F.
11. **SAM €15 bn for data-centre cooling.** Applicant figure; add the source from the BP. Open: whether it is global or Europe + North America. If it is global, the SOM shares are slightly understated relative to Savery's territory, which is acceptable.
12. **Expansion segments** (industrial waste heat at 40–50 °C, urban critical facilities) are named but not sized, by choice.
13. **150 MW/yr in 2032 = €900/kW volume.** This is a consistency used in the proposal. It holds only if a unit is 100 kW (item 9).

## Customer economics

14. **Data-centre payback.**
    - Proposal figures: 31–36 months at €0.20/kWh and 25–29 months at €0.25/kWh (€1,200/kW installed); 26–30 months at €900/kW hardware, €0.20/kWh.
    - Assumptions: 8,000 h/yr displaced; rack heat free; COP 12–20 against EER 3; water €4/m³ with 50% saving on a 1.5 L/kWh reference (€0.30/h); service €2,000/yr; 100 kW package.
    - At COP 8 and €0.20/kWh: 43 months. At €0.15/kWh: 42–47 months (COP 12–20).
15. **Other domains.**

    | Case | Tariff | Price | Payback |
    |---|---|---|---|
    | Industrial, 6,000 h, free heat, COP 12–20 | €0.20/kWh | €1,200/kW | 43–48 months |
    | Industrial, 6,000 h, free heat, COP 12–20 | €0.25/kWh | €1,200/kW | 34–39 months |
    | 4,000 h, COP 12–20 | €0.20/kWh | €1,200/kW | 66–75 months |

    The proposal shows only the data-centre case and refers to the BP for other domains.
16. **ROI and ROIC.** Copy from the BP into package F. **Before submit.**
17. **Grid-capacity value.** The proposal states the kW freed but puts no euro value on it, so no colocation price source is needed.

## IP and FTO

18. **FR2508386 / PCT.** The filing identity comes from the attorney invoice F26_24238PL. Check the official receipts. The PCT number is probably PCT/FR2026/010348; use the receipt form in the FTO note. FR2508386 is unpublished until about January 2027.
19. **EP3825627A1 (2019).** The public index shows it as pending, applicant Savery Tech. Still to check: the EPO Register examination status and whether national phases of WO2021099546 were entered.
20. **EP3350151B1 / US10696704B2 (Kiel/Fraunhofer, MOF production methods).** As quoted, the US claim covers aqueous synthesis with an isophthalate linker below 1.5 bar, which is CAU-10-H chemistry. The proposal commits WP2 to clearing the route through licensed supply or a non-infringing process before M12. Counsel must confirm the route and which countries the patents are in force in. Norbert Stock's board seat makes a licence discussion natural, but the proposal must not imply one exists.
21. **CNRS MIL-160 family.** No longer cited. It is relevant only if the 2025 tested machine used MIL-160 (item 3).
22. **BASF, NuMat, Framergy, Montana/AirJoule.** These remain screening leads. No professional FTO opinion exists yet for the CAU product.

## Implementation, team, finance

23. **Seed timing (see also item 30).** BP: launch September 2027, close November 2027. EIC investment normally follows EIC due diligence after the award, so the €2m EIC tranche may close later than the private Seed.
24. **Bridge from April to November 2027.**
    - Proposal: "Grant pre-financing and current cash fund the action from April 2027 until the Seed closes in November 2027."
    - Basis: the FP 60/25/15 grant timing gives about €1.49m pre-financing, against about €1.14m action cash over 7 months.
    - Risks: the action start date may slip with grant-agreement preparation, and €300k of current cash will partly be spent before April 2027.
25. **Series A in April 2028**, five months after the Seed closes, with €25m. Investors may question that gap. It comes from the BP and is not changed.
26. **CETP/EIC separation.**
    - The 36 PM of thermal-validation and supervisory-control work sit next to CETP's digital-twin/RL research. Reconcile against the signed CETP workplan before charging costs.
    - "Incremental EIC access" to the HPE site: confirm the agreement exists or will be concluded.
    - The TRL8 field site for the M16 installation is unnamed. The 2027 reference customers are candidates.
27. **Team.** Current total headcount is not stated in the proposal. 82.6% of PM (213) sit with eleven roles still to recruit. The founder's commitment is 50%; the proposal says the remainder goes to leadership, financing, partnerships and CETP.
28. **Investor evidence.** No LOI is named. The BSA-AIR total raised is not stated. Both would help §3.2 if available.
29. **Gender target.** At least 40% women among new hires by M24 is a commitment and must be tracked.

## Added after A16-R3 (v2)

30. **Seed date version conflict.**
    - Current BP G3.1 (financing table): Seed March 2027, USD 8m (A April 2028, B January 2030, C January 2032).
    - BP assumptions of 10 Sep 2026: launch September 2027, receipt 15 November 2027.
    - Applicant, 3 Nov 2026: launch September 2027, close November 2027. The proposal follows the applicant.
    - Both dates fall in the 2027 annual column, so FP/DB figures are unchanged.
    - Action: update the BP G3.1 table text so the annex and Part B match.
31. **Funding targets USD to EUR.** The BP rounds are in USD; the proposal uses the same numbers as nominal EUR, by applicant decision. No FX conversion. Expect an investor question only if the BP annex is read side by side with Part B.
32. **SAM source and scope.**
    - GMI GMI423 (Sept 2026): USD 20.5 bn, worldwide, 2025, covering equipment, integrated systems and services.
    - Converted at about 1.13 USD/EUR (2025 average, approximate), that is about €18 bn. The applicant's "about €15 bn" is the same order.
    - SOM shares (about 1% in 2032, about 0.4% in 2031) use the 2025 market as denominator. The market will grow, so the true share is lower; this is conservative for credibility.
    - GMI is worldwide, while Savery's territory is Europe + North America.
33. **Forecast unit vs product capacity.** L2 refused to infer 100 kW per forecast unit from €110k at €1,100/kW. The proposal therefore states the 20 kW module and 600 kW container, and keeps 100 kW only as the payback normalisation. The "150 MW in 2032" link is dropped. Interview question to prepare: "what capacity is one forecast unit?"
34. **Payback statement (v3 pack).**
    - Basis: rack heat at no cost; 8,000 h; €120k per 100 kW. At €0.25/kWh across COP 8–20: 25–34 months.
    - At €900/kW hardware (€100k installed) and €0.20/kWh: 26–36 months.
    - At €0.20/kWh and €120k: 31–43 months. This is not stated in the proposal.
    - The R3 version (EER 10 with €0.01/kWh heat) is superseded.
35. **Heating COP 6–10.** The applicant's wording is "can reach". The proposal uses "can reach" / "up to", so no measurement claim is made.
36. **Installed COP 8–20.** An applicant engineering range (adjacent components and site pumps), not a measured range. The proposal words it as a dependency on the site.
37. **Process.** The R3 internal notes (line 40) rejected applicant facts as red-team additions. L1 must issue the v3 fact sheet as direct applicant facts so that R4 does not repeat this.
38. **Team commitment %.** The template column "Commitment" means time committed to the company. The v3 pack shows 100% for all three leaders as the full-time default. Enter actual values. The 50 / 87.5 / 50% figures are EIC-action allocations, now in the Implementation Plan annex.
39. **Governance table.** CURMA SOLUTIONS 90% / pool 10% is a pre-conversion fully diluted view. Open:
    - Frédéric's ownership share of CURMA (the shareholder declaration notes that CURMA's own split is also required).
    - The BSA-AIR conversion effect, which is excluded.
    - Whether investors will take board seats at Seed. The governance sentence 6d is only a suggestion.
40. **Regulatory paragraph 6e to verify.**
    - F-gas Regulation (EU) 2024/573 scope, and no F-gas on any auxiliary circuit.
    - EED (EU) 2023/1791 and Delegated Reg. (EU) 2024/1364 KPIs, including water.
    - German EnEfG PUE limit for new data centres from July 2026 (about 1.2). Waste heat reused inside the site does not count toward the EnEfG energy-reuse factor, so no ERF claim is made.
    - Machinery Regulation (EU) 2023/1230 applies from 20 January 2027.
41. **"Aluminium-based CAU sorbents, no rare earths" (6b).** True for CAU-10 and CAU-23. Confirm for the selected variant.
42. **CV links and LOIs.**
    - CV URLs are needed for the CVs section.
    - LOIs are listed as a mandatory annex in the template. Candidates: the two 2027 reference customers, HPE (CETP site) and the 2025 investors.
    - If no LOI can be obtained, upload what exists. The template requires the guidance template format.
43. **Investor traction (template 3.2).** The BSA-AIR amount raised and the number of investors are needed for one sentence.

## Added after A16-R4 (v3)

44. **Figure 1 provenance.**
    - The "AI" container shows third-party logos. Keep only partners who have consented in writing.
    - SEM tile: the 10⁻⁵ m label conflicts with the 500 µm scale bar, and the data bar shows a literal "label" field. Confirm the image is a real Savery micrograph. If it is AI-generated or stock, it must not be presented as a micrograph.
    - The flame icon on the unit render suggests combustion.
    - The sorption curves show linkers from the earlier material family (furan / pyrrole-type dicarboxylates, isophthalate). The caption must not present them as CAU batch data.
45. **COP 20 test traceability.** The EIC annex list has no slot for a test report, and experts ignore hyperlinks. Cite title, laboratory and date in the references. Which EN standard the test followed is still unknown. L2 notes that ASHRAE 143 excludes units with dried air streams and that EN 13141-7 covers residential ventilation units. Expect the interview question "which standard, which laboratory?"
46. **Team employment status.** R4 S3 l.17 hinted that the full-time commitment is separate from current contract/payroll status. The v4 pack removes that sentence. If the three leaders are not currently employed full-time, prepare the interview answer: start dates, contracts at Seed.
47. **€15 bn vs USD 20.5 bn.** The company estimate (€15 bn) and the GMI worldwide figure (USD 20.5 bn ≈ €18 bn at about 1.13) are both shown. The SOM shares (0.5% / 1.2%) use the €15 bn. The scope of the €15 bn is not documented.
48. **Customer ROI vs company ROIC.** R4 shows customer cash ROI of 35–48% (at €0.25/kWh, 8,000 h, rack heat free). Company ROI/ROIC from the BP were not inserted. L2 found no computed basis and removed the placeholder.
49. **Page count.** About 10,000 words plus 20 tables plus a figure, before the executive summary and challenge statement. Check the merged DOCX; apply cut list v4-C if it runs over 20 pages.
50. **Metrics table (v4-A).** "934 units by 2031" is the cumulative sum of 2027–2031 planned acceptances from the G3.1 forecast.

## Added after A16-R5 (v4)

51. **CO₂ factor (v5-2c).** The figures use 0.2 kg CO₂/kWh as an approximate EU grid intensity. Check against the latest EEA figure (around 0.2–0.25 for 2023–2024) and adjust 330–450 t if needed. The per-MW electricity (1.67–2.27 GWh) and water (4,800–7,200 m³) figures are arithmetic on the S2 assumptions: 8,000 h, EER 3, 1.5 L/kWh, 40–60%.
52. **Comparison table claims (v5-2b).**
    - "Desiccant wheels need higher regeneration temperature": true for typical silica-gel/zeolite wheels. Low-temperature wheels exist, so the wording is "higher", with no number.
    - "Chiller EER about 3 in heatwave hours": typical for air-cooled chillers at 35–40 °C ambient.
    - "Pre-dried air lowers the wet-bulb limit": physics.
    - The make-up water reduction is not attributed to the evaporative-only comparison, because its baseline is undefined.
53. **Deep-tech paragraph (v5-2a).** The step-shaped water isotherm is true for CAU-10-H, CAU-23 and MIL-160. Zeolites need hot regeneration, and silica gel uptake is gradual. The patent claim "decreasing water-adsorption thresholds at 25 °C" matches the staging described.
54. **Board credentials (v5-2d).**
    - Norbert Stock: professor at Kiel University (Christian-Albrechts-Universität); his group originated the CAU frameworks.
    - Aline Auroux: CNRS (IRCELYON), adsorption microcalorimetry. Check whether her title is emerita.
    - Confirm both are happy to be described this way.
55. **Incentives (v5-2e).** The template asks how the team is incentivised. R5 removed the 10% pool after the applicant said current team members hold no options. A plan to set one up at Seed must be confirmed by the applicant before the sentence goes in.
56. **Figure 1 chip "40–60% less make-up water".** This is a qualification target, not a measured result; the caption says "target". "Electrical COP 8–20" is the company engineering range, with 20 measured.
57. **Figure 2.** Crop the SEM data bar (illegible; 500 µm bar against a 10⁻⁵ m tile label). The third-party logos on the "AI" container are kept by applicant decision; they are a residual risk if an evaluator reads them as partners.
58. **"EN standard test conditions" as the TRL6 relevant environment (v5 S1 l.87).** This is defensible for HVAC equipment rated under standard conditions. Expect the interview question on field operation, which is CETP/HPE (TRL7) and the EIC field programme (TRL8).

## Added after A17-R1 Implementation Plan (4 Nov)

59. **IP filing dates in T5.2.**
    - 2025 family: priority 21 Jul 2025. PCT national phase 30 months = 21 Jan 2028 (M10); EP regional phase 31 months = 21 Feb 2028 (M11).
    - EP26301484.7 (filed 9 Oct 2026): a 12-month Paris priority deadline of 9 Oct 2027 (M7) applies only if it is a first filing with no earlier priority claimed. Confirm.
    - Choose territories with counsel.
60. **WP TRL targets 7/7 for WP2/WP3.** Justified by field operation from M17. The conservative alternative is "6–7".
61. **Milestone criteria.** The MS5 pass criteria (≥60% electricity, ≥40% water) turn the qualification targets into acceptance thresholds. If field results fall short, MS5 is formally missed; that is the intended signal of a verifiable milestone.
62. **Residual risk re-rating.** These are planning judgements; adjust if the applicant sees it differently.
