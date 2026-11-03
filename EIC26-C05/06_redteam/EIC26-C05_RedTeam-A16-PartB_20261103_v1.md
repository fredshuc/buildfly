# Red-team review of EIC26-C05 A16-R1 Part B

Reviewed: `EIC26-C05-A16-R1_PartB_EN.md` and `.pdf` (19 pp, A4, Times New Roman), together with the FTO status note, ESR source review, L1 order, KBIS, cap-table declaration, MARKET_MODEL, PAYBACK_CASE and COMPANY_FORECAST_BASIS. Date: 3 Nov 2026.

## Verdict

A16 is clean. The internal markers are gone, the arithmetic checks (grant = 70.000% of eligible cost; WP and role person-months both sum to 258; cash bridge €3,908,916.67), and the structure follows the template. **As written, though, it is unlikely to get GO from all three evaluators on any of the three criteria.** Three issues explain this, and each can be fixed before 14:00 tomorrow:

1. **The proposal claims TRL 6 but contains no measured data.** Every performance number is labelled a "target", "planning basis" or "illustrative". The only evidence cited for TRL 6 is "management confirmation, 3 November 2026" [T01], and one sentence reads as if the TRL was set for this application. Feasibility was the strongest sub-criterion in 2025. Here it is exposed.
2. **The IP rests on a patent family whose status and chain of title are never stated.** Savery was registered on 23 Sep 2024. The 2019 family (EP3825627A1 / WO2021099546A1) therefore reached Savery by assignment, and the proposal does not say so. If an evaluator checks Espacenet and finds the EP application deemed withdrawn, or the PCT never entered national phases, or a different applicant, the 2025 criticism (ownership unclear) comes back in a stronger form.
3. **The economics and the revenue story don't hold together under scrutiny.** The 24–36-month payback only works at an electricity tariff of €0.26–0.29/kWh or more (the example uses €0.35) and assumes an EER-3 baseline for 8,000 h a year. The C05 revenue (€1.8m in 2031 = 10% of an €18m SAM) contradicts the company forecast (€75.2m in 2031, plus revenue in 2027–28 before the product is qualified in 2029).

**10:00 gate (your rule: submit only if the current TRL and a positive IP position can be stated truthfully).** Neither condition can be confirmed from the package. Both can be checked in under an hour. The first needs the TRL 6 machine's test record (date, site, conditions, measured outputs). The second needs the EPO Register / Espacenet legal status of EP19306516.6 and PCT/EP2020/082838, plus the assignment deed and its recordal. If both hold, submit with the fixes below. If the family has lapsed, the IP section has to be rebuilt around know-how and new filings, and your rule then points to deferral. Note: the L1 order forbids recommending deferral. Your gate rule is the stricter instruction, so I apply it here.

Confidence: high that findings 1–3 would be noticed by at least one evaluator; medium on how each would score.

## Findings, ranked by effect on the score

### Excellence (2025: 2/3, the only "average" was IP)

**X1. Back TRL 6 with evidence, or the "very good" on feasibility is at risk.**
- §1.2 says the machine combines staged MOF exchange, switching, IEC and controls, but gives no test date, site, inlet conditions, measured supply-air state, measured EER or operating hours.
- The cited evidence is [T01] (management confirmation dated the day before submission), [T02] (another grant application, cited by its internal filename "FC01_FC08_FINAL") and [T06] (an internal evidence map).
- One sentence must go: "Subsequent current company confirmation establishes the completed-machine TRL6 status used in this application".
- Fix: add one paragraph and a small table of measured results from the test report (rating points: inlet T/x, supply T/x, airflow, electrical input, regeneration-heat temperature and flow). Cite the report ID, lab and calibration, and add a photo of the machine. If the 2025 figures (16–20 °C at 9–11 g/kg, 60–70% electricity, 40–60% water) were measured, say "measured" and give the conditions. A16 downgraded all of them to targets only because L2 never had the raw report (TECH01).

**X2. Say which sorbent is in the TRL 6 machine.**
- The A16 TRL table lists the CAU contactor as "current CAU-series route and coated-exchanger development". That implies the validated machine may not run on CAU. If it ran on MIL-160 or Al-fumarate, switching the sorbent after validation lowers the maturity of the contactor, and an evaluator will ask.
- Fix: state the sorbent in the tested machine.
- If it was not CAU, add one sentence: MIL-160 is isostructural with CAU-10-H (Cadiau et al., Adv. Mater. 2015), so the move to CAU-series stays within one Al-chain framework family. Then cite any CAU-coated exchanger data (Henninger et al. 2023 [T03] covers CAU-10-H coatings).
- Also add one sentence telling the 2025 story positively: moving to CAU removed the licence dependency the 2025 IP evaluator criticised.

**X3. IP: state the status, chain of title and sorbent-material position.**
- §1.3 says "Savery owns the system patent". The documents are A1 and WO publications, and no grant is shown.
- Fix: give a status table per jurisdiction (pending / granted / lapsed) and the assignment date and recordal. Use "patent application" unless something has been granted.
- The FTO map now covers BASF, NuMat, Framergy and AirJoule, which is good and answers E1 directly. It misses the most obvious question for a CAU product: who holds composition or use patents on the CAU material itself (Kiel University / Fraunhofer ISE coating processes)? With MIL-160 being isostructural, the CNRS MIL-160 family also needs checking.
- With Norbert Stock on the board, an evaluator will ask whether Savery needs a CAU licence. Fix: one sentence giving the answer (unpatented / expired / not in force in the target countries / licensed), backed by counsel, and add those families to the FTO note's table.

**X4. Give the novelty one quantified edge.**
- After correctly conceding that AirJoule also uses low-temperature heat, A16's advantage is "the combination of low-temperature thermal input, controlled air-side cooling and lower external water demand in a retrofit arrangement". That is a description, not a breakthrough.
- AirJoule's own disclosures show sealed/vacuum chambers: its product guide applies vacuum for regeneration, and claim 1 of US20250043971A1 recites chambers with sealed and unsealed states. Its product is water, at 0.50 kWh/L with a heat pump.
- If AirTransformer regenerates at ambient pressure and its product is conditioned air at a measured electrical EER, say so in one sentence with the number. Also note the 2019 priority date.

**X5. Tone.**
- Excellence reads like a QA manual: water ledgers, comparison boundaries, "does not mean", "is not presented as".
- About 64 sentences carry a negation or hedge. "Target" appears 19 times; "demonstrated" appears once.
- Fix: cut about 25% of the methodology prose in "How the system delivers cooling", "A quantified product specification" and "From TRL6 to a qualified product", and use the space for measured results and the photo.
- Sentences to delete outright:
  - "This calculation explains the target; it is not presented as an already measured field reduction."
  - "We do not infer a released physical machine rating from a 100 kW commercial planning equivalent."
  - "These are scoped commercial assumptions rather than existing machine ratings or orders."
  - "The action makes no fixed daily water-output promise…"

### Impact (2025: 3/3, now at risk)

**I1. The payback depends on a tariff and a baseline that data-centre experts will challenge.** Calculation on A16's own inputs (100 kW, 8,000 h, €120k installed, heat at €0.01/kWh, water and service as stated):

| Electricity tariff (€/kWh) | 0.12 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 |
|---|---|---|---|---|---|---|
| Payback, EER 8–10 (months) | 97–116 | 71–83 | 48–56 | 37–42 | 30–34 | 25–28 |

- Hitting 36 months needs at least €0.26–0.29/kWh. Large European data-centre tariffs are typically well below €0.35 (my estimate; check Eurostat nrg_pc_205, bands IF/IG).
- In Frankfurt, London, Amsterdam and Dublin, free cooling covers most hours, so an EER-3 baseline for 8,000 h overstates annual savings (medium confidence).
- For hospitals or public buildings at about 2,500 h, payback exceeds 15 years. So **do not pivot the customer to hospitals**.
- Fix: keep data centres as the customer but move the value to where it is real, which is also the C05 argument. During heatwave hours compressor EER falls to about 3, grid headroom disappears, and AirTransformer frees **about 210–230 kW of grid capacity per MW of cooling** (333 → 100–125 kW). In grid-constrained FLAP-D markets that capacity is worth more than the energy.
- Show payback as a tariff range with a cited tariff, and drop the single €0.35 case.

**I2. There are two revenue stories.**
- §2.1/2.2: C05 sales are €0 in 2027–28 and €0.6/1.2/1.8m in 2029–31; "commercial entry follows product qualification in 2029".
- §2.2 and the FP: €0.48m and four accepted reference units in 2027, then €1.56m, €8.5m, €26.7m, €75.2m and €180.9m (2028–2032).
- Company revenue in 2031 is 4.2× the stated SAM, and units are accepted two years before qualification. The disclaimer ("broader product and geographic mix") doesn't name what the other products are.
- Fix: one TAM → SAM → SOM chain consistent with the FP. Say what the 2027–28 revenue is (paid pilots or reference units?), define SAM at a size that can carry the FP (Europe plus North America, new build plus retrofit), and drop the 10% × 25% double haircut or source it.

**I3. Strengthen the challenge fit (scored Positive/Negative; a Negative is fatal).**
- §1.1 opens with "first commercial focus is data-centre infrastructure", the SAM is 100% colocation, and §2.4 calls hospitals "prospective".
- Fix: add the urban-heat mechanism with numbers: peak grid relief during heatwaves, and less anthropogenic heat (when regenerated with heat the site already rejects, heat released to the city falls by the compressor work avoided, about 210–230 kW per MW of cooling).
- Cite real grid constraints on urban data centres (for example Dublin connection restrictions and Amsterdam-region limits) with sources.
- Drop-in text is in Appendix B.

### Implementation (2025: 2/3, the only "average" was team / gender)

**M1. Gender.** The organisation-wide measures are process-only, with no numbers or dates. E3 marked 2025 down for lacking organisation-wide coverage; A16 fixes the coverage but drops the targets. Add measurable targets across all role families with an owner and review dates. For example: balanced shortlists for each of the 11 hires, with a target share of women among new technical and non-technical hires by M24. The current baseline is 1 of 3 core staff. Choose numbers you can stand behind.

**M2. Team capacity.**
- Three people, CEO at 50%, and 69% of the 258 PM (179 PM) sit with 11 unnamed hires entering M1–M7.
- Fix: one sentence saying where the CEO's other 50% goes (CETP leadership and fundraising, still full-time at Savery); explain 5 FTE in 2025 → 3 now; name any identified candidates or contracted partners for the process and reliability roles.

**M3. Overlap with CETP (double-funding risk).**
- The L1 order's own reading of the CETP/AIRCAS workplan lists materials/kinetics, heat and mass transfer, cycle maps, digital twin/RL and HPE integration.
- The EIC budget funds a thermal-modelling specialist (18 PM) and a supervisory-controls specialist including RL (18 PM), which is the same subject matter.
- The EIC action also reaches TRL 8 by March 2029 while CETP targets TRL 7 by 2029.
- Fix: move RL and model development to CETP background, repurpose those 36 PM to embedded productisation and DfM, and give the date of the CETP TRL 7 milestone. Name the EIC field site for the TRL 8 qualification, or the alternative test route.
- This also shortens the AI robustness answer.

**M4. Financing evidence.**
- "Existing investor letters of intent can support the account of interest according to their actual terms and dates" is an internal note.
- Fix: name the LOIs (investor, amount, date, conditions) or delete. Give the BSA-AIR total raised to date as track record. The €240m / €500m / €1bn pre-money figures are already gone from the A16 Part B; they survive only in the historical 31 Oct draft.

### Cross-cutting cleanup

- References: replace [T01] (management confirmation) with documents, and [T02] (LIFE Part B, internal filename) and [T06] with test-report IDs; [M9] "Growth Business Plan G3.1" becomes "Savery business plan, Oct 2026".
- Sentences that answer an internal reviewer rather than an evaluator: §1.2 "Subsequent current company confirmation…"; §2.1 "We do not infer…"; §3.3 "These are scoped commercial assumptions…"; §2.2 "This avoids attributing several revenue models to one asset before the commercial structure exists."
- Figures: one schematic only. Add a photo of the TRL 6 machine and one measured performance chart.
- Cover block: write amounts without cents in prose, and keep exact figures in the Portal only.

## Inputs needed from you by 10:00 (nothing else blocks)

1. TRL 6 test record: machine configuration and sorbent, test dates, site/lab, rating points with measured outputs, report ID. A photo.
2. EPO Register / Espacenet status of EP19306516.6 and PCT/EP2020/082838 (national phases entered?), original applicant, assignment date to Savery and recordal.
3. Counsel's one-line position on CAU material patents (and CNRS MIL-160 if the 2025 machine used it).
4. Investor LOIs (names, amounts, dates) and the BSA-AIR total raised.
5. What the 2027–28 revenue in the FP actually is.

## Appendix A: replacement executive summary (half page; fill the «» from item 1 or 2 above)

Heatwaves now coincide with grid and water constraints in Europe's largest cities. Facilities that cannot shut down, data centres first among them, must keep cooling when compressor efficiency is at its lowest and the grid is most stressed. AirTransformer is a heat-driven cooling unit. A CAU-series metal-organic framework (MOF) removes moisture and is regenerated with 50–70 °C heat the site already rejects; the dried air is then cooled by indirect evaporation. Electricity drives only the fans, pumps and controls.

Savery's complete machine is at TRL 6. «Configuration, site and dates.» It delivered 16–20 °C supply air at 9–11 g/kg «at stated inlet conditions» with an electrical EER of «measured value». At equal cooling, this corresponds to 60–70% less electricity and 40–60% less external make-up water than a compressor reference at EER 3. During heatwave hours, each MW of cooling moved onto AirTransformer frees about 210–230 kW of grid capacity.

Savery owns the 2019 cascaded-sorption patent family (EP3825627A1, WO2021099546A1; «status») and its product know-how. Its scientific board includes Norbert Stock, whose Kiel group developed the CAU materials, and Aline Auroux. A CETP grant (2026–2029) is taking the system to TRL 7 at an HPE data-centre site. The EIC action does what CETP does not: it freezes a manufacturable design, qualifies CAU contactor batches, proves reliability and conformity, and completes TRL 8 qualification for repeat deployment by March 2029.

We request a €2,485,583 grant (70% of €3,550,833 eligible cost) and €2m EIC investment within an €8m Seed round, to build production and service capacity.

## Appendix B: challenge-fit paragraph for §2.4 (replaces the first paragraph)

Extreme heat strains cities through three coupled channels: more cooling demand, lower efficiency of the compressor plant that meets it, and grid and water limits that bind on the same days. AirTransformer acts on all three for a defined cooling duty. For 1 MW of cooling regenerated with heat the site already rejects, electrical demand falls from about 333 kW (EER 3, typical of compressor plant at heatwave temperatures) to 100–125 kW. That frees about 210–230 kW of grid capacity in the hottest hours, and the city stops receiving the same amount of heat from compressor work. It also cuts external make-up water by 40–60% when water restrictions are most likely. Data centres are the first customers because they combine continuous load, surplus heat and grid constraints in dense urban areas. The same qualified product can then be offered to other heat-rich critical facilities through the Adaptation Mission network.
