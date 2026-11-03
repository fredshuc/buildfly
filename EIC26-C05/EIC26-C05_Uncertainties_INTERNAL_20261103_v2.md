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
