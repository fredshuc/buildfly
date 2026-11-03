# EIC AirTransformer 2025 ESR: independent source review

Review date: 2026-11-03. Internal analysis for the L1 strategy and L2 order.

## Source and reading scope

- Actual supplied file: `/workspace/scratch/520abd837c5f/upload/101297706_AirTransformer_ESR(1).pdf`.
- 391,535 bytes; 12 physical pages: 11 report pages plus the digital seal page.
- SHA256: `9ba5fb41542e840d06cd7e0fa07c309044f86b0990a51ec566a85605921afb21`.
- Proposal 101297706; call HORIZON-EIC-2025-ACCELERATOR-02; AirTransformer; Savery Tech; report dated 14 December 2025; Ref. Ares(2025)11130502.
- Every page was extracted with Poppler and/or pypdf; all 12 rendered original pages were visually viewed.
- Page references below are physical PDF page numbers; pages 1-11 match the report's printed page numbers.
- Reviewer labels E1/E2/E3 mean the three paragraphs in the recurring order in each criterion. The ESR does not expose personal reviewer identities.

## 1. Main diagnosis

The red team's central diagnosis is correct. Excellence has 2/3 GO votes; Impact 3/3; Level of risk, implementation and need for Union support 2/3. Novelty, timing and technological feasibility are each rated **very good by all three reviewers**. The only **average** rating in Excellence is the first IP assessment (p4). The only other **average** rating in the report is the third Team assessment (p8).

This establishes a strong basis for prioritising IP/FTO ownership and scope, organisation-wide gender representation, and a clear operating-company team. It does not support diagnosing last year's refusal as insufficient scientific depth.

The report's overall result is formally **0/9**, not 7/9. The 2+3+2 breakdown is diagnostic. Under the recorded 2025 procedure, GO required all three criteria at 3/3. The final page also states that the proposal did not qualify for a consensus meeting, whose trigger required at least two reviewers to award GO across all evaluation elements (pp2,11).

## 2. Full rating and source map

| Criterion/subcriterion | E1 | E2 | E3 | Physical page |
|---|---|---|---|---|
| Excellence overall | \- | 2/3 overall | \- | 2 |
| 1 Novelty and breakthrough | Very good | Very good | Very good | 2 |
| 1.1 Challenge fit | Positive | Positive | Positive | 2 |
| 2 Timing | Very good | Very good | Very good | 3 |
| 3 Technological feasibility / TRL5 completion | Very good | Very good | Very good | 3 |
| 4 IP strategy and FTO | **Average** | Very good | Very good | 4 |
| Impact overall | \- | 3/3 overall | \- | 4 |
| 5 Customer demand | Very good | Very good | Very good | 4 |
| 6 Market development | Very good | Very good | Very good | 5 |
| 7 Commercialisation strategy | Very good | Very good | Very good | 5 |
| 8 Scale-up potential | Very good | Very good | Very good | 6 |
| 8.1 Grant-only resources | Not applicable: grant-only No | \- | \- | 6 |
| 9 Broader impact | Very good | Very good | Very good | 6 |
| 9.1 Challenge/STEP outcomes | Positive | Positive | Positive | 7 |
| Implementation/risk/Union support overall | \- | 2/3 overall | \- | 7 |
| 10 Team | Very good | Very good, minor shortcoming | **Average** | 8 |
| 11 Investment need | Very good | Very good | Very good | 9 |
| 12 Risk mitigation | Very good | Very good | Very good | 9 |
| 13 Implementation plan | Very good | Very good | Very good | 10 |

## 3. What the two negative assessments actually concern

### 3.1 IP/FTO, E1, p4

The reviewer credits the general IP structure but identifies:

- FTO limited to preliminary screening.
- No sufficiently thorough map against comparable MOF-based systems, naming BASF, NuMat and Framergy; US and Asian markets singled out.
- Ownership, licence scope and incorporation of new applications into commercialisation not sufficiently clear.
- CNRS licence agreement absent from the appendix; scope consequently unconvincing.
- Need for a current patent map and non-European protection strategy.

E2 says Savery owns machine, cycle and controls, with adsorbent chemistry held by academic partners; it refers to three PCT patents, trade marks, firmware/HMI copyright and future continuation/divisional filings. E1 instead refers to two international applications. These inconsistent counts cannot establish the current portfolio.

E3 accepts a described exclusive EU CNRS field-of-use licence with sublicensing and diligence terms. E3 also accepts an FTO analysis distinguishing two-MOF HMX and closed-cycle adsorption claims, identifying geometric IEC/HMX and D2/D3 chemistry/substrate issues, and recommending design-arounds and safer claim lanes. Its conclusion is geographically bounded and conditional: the applicant should presently have freedom to operate in Europe under those recommendations.

**Implication for 2026:** user-confirmed current Savery ownership and CAU-family direction supersede the old CNRS-dependent narrative. The correct repair is a current ownership/protection and product-specific FTO account. It is not necessary to perpetuate the old MIL-160 licence discussion simply because the ESR evaluated it. Ownership of a patent and third-party FTO remain distinct matters, so the new text should name the actual current portfolio and the scope of the FTO work that exists.

### 3.2 Team, E3, p8

E3 finds team composition, motivation, capability, advisory ecosystem and skill-acquisition plan convincing. It records five FTE spanning MOF materials, HVAC/mechanical, controls, field operations and commercial work, and planned hires for Pilot-Site Manager, Controls/Software Lead, HVAC Engineering Lead and CFO.

Its adverse finding is specifically that gender plans addressed executives, the board and management but **did not address the organisation as a whole, including non-executive positions**. The cited targets were at least 50% women in executive roles by 2027, 33% on the board by 2026 and 40% across management by 2028, with balanced shortlists. Merely adding a gender column or naming female advisers does not by itself answer that organisation-wide point.

**Additional useful criticism omitted by the short red-team summary:** E2 (still very good) says the connection between missing skills and individual WP needs is insufficiently described. It calls this a minor shortcoming. The revised team section should therefore connect named accountable owners and recruitments to specific development, validation and commercialisation tasks.

The reviewers give inconsistent pictures of current representation: E1 says 40% female representation, E2 describes one female CEO on the board, and E3 discusses five FTE and targets. Those are historic evaluation statements, not safe current headcount facts. Current user-confirmed board membership should be used; no role, gender or employment status should be inferred merely from a name.

## 4. Technical and commercial evidence worth recovering

The ESR shows which quantitative and practical elements made the application convincing. It is an evaluation of the proposal's evidence, not the underlying test report or an independent certification.

| Element | ESR location | Correct use in the new draft |
|---|---|---|
| Low-grade waste heat regeneration at 50-70 °C | pp2-4,6 | Restore the relevant current operating envelope, with source/test or design conditions. E3 p5 separately mentions 40-60 °C; reconcile to the actual configuration rather than combining ranges indiscriminately. |
| Supply air at 16-20 °C and 9-11 g/kg | p3 E2 timing; p3 E3 feasibility | Restore as a specific integrated cartridge/platform performance record once its original conditions are recovered. **g/kg is humidity ratio, not a dew-point unit**; correct the ESR's loose phrase. |
| Integrated MOF contactor + dew-point IEC + regeneration loop | p3 E1 feasibility | Useful baseline description distinguishing proven core from the EIC industrialisation increments. |
| ASHRAE 143 and EN 13141-7 methods; ISO/IEC 17025 calibration traceability | p3 E1/E3 feasibility | Say protocols/traceable calibration at the actual level. The report does not show complete final third-party product certification; E1 says third-party tests ongoing. |
| Electricity reduction 60-70%; water reduction 40-60% | pp2,4,6 | Restore comparison quantities with actual baseline, duty, climate and evidence classification. Avoid turning an expected or conditional benefit into a new measured universal guarantee. |
| Payback 24-36 months | pp2,4 | Restore the economic case with its pricing/utilities/use assumptions. |
| €1,100/kW pilot hardware, trending to €900/kW at at least 150 MW/year | p5 E3 commercialisation | Recover original costing and identify stage/volume. It is not a current supplier quote. |
| More than 200 value-chain consultations | p2 E3; p3 timing praises survey | Useful traction/history if the original survey and dates support it. |
| 0.2-0.6% projected share over 36 months | p5 E3 | ESR uses awkward wording ('global SAM ... estimated at ...%'); recover the denominator and period from the old proposal before binding the new revenue forecast. |
| Two investor LOIs and conditional co-investment | p9 E3; E1/E2 same direction | Recover original documents, current applicability and amounts. The ESR itself prints 'circa €3' without 'million', so it alone cannot establish a €3m plan. |
| Credible implementation, resources, measurable milestones and deliverables | p10 all reviewers | Preserve the strengths: specific operating stages, qualification, certification and commercialisation. Avoid replacing these with an open-ended research programme. |

### TRL nuance

All three reviewers rate the validation pathway and completion of TRL5 very good (p3), but they do not use an identical starting-TRL statement:

- E1: the project can now be rated TRL6; independent ISO/IEC 17025 third-party testing still underway.
- E2: positive evaluation of six years of laboratory development, observed results, TRL pathway and robustness; no single numerical starting TRL asserted in this paragraph.
- E3: TRL5 fully completed; advancing toward TRL6 while a fully instrumented prototype undergoes independent validation.

User's current statement that the complete machine is TRL6 should now govern the application. The current machine evidence should be attached or cited directly. The ESR is useful context for the previous acceptance of the technology maturity pathway, not a substitute for current configuration evidence.

## 5. Other red-team points: corroboration and limits

- **AI:** p11 records No to use/development of AI systems and techniques. It then says Yes would require technical robustness evaluation under the appropriate criterion. A genuine RL workstream should be declared on its actual scope; changing the declaration is not itself an adverse finding. The ESR does not justify suppressing a real workstream or relabelling AI to keep No.
- **Grant-only:** p6 explicitly records No to grant-only, and does not assess the dedicated access-to-resources question. Therefore last year's Impact 3/3 does not establish that a new grant-only commercialisation financing plan has already passed. User now permits the €2m EIC investment request to return; p9 shows all three reviewers found the investment rationale very good.
- **Old challenge fit:** pp2,7,10 unanimously support the 2025 advanced-materials challenge fit and mark the application in scope. This does not establish fit with the differently defined 2026 C01. Current call text must decide C01/C05.
- **Video:** the ESR has no distinct video criticism or indication that film production quality caused refusal. Reusing a suitable old video therefore deserves priority over an elaborate new production within the submission window.
- **Submit tomorrow:** the ESR itself supplies no reason to countermand the user's committee-invited submission objective. The present task is to repair the application and return a complete pack for that deadline.

## 6. Do not mechanically restore every old number or description

Three inconsistencies show why the original proposal/evidence, rather than the ESR's paraphrases, must be the drafting source:

1. The p1 submitted abstract says 150 MW of deployed cooling saves 18 TWh electricity per year. 150 MW operated continuously yields only 1.314 TWh/year of thermal service. The stated annual electrical saving cannot simply be copied without its missing scale/denominator being corrected.
2. E1 p5 presents a licensing/revenue-sharing model; E3 p5 describes equipment plus services/software. E1 p10 describes four-to-five years, while E3 p10 describes a 24-month grant component and 36-month wider project. These are divergent paraphrases. Current product and finance architecture should be singular and explicit.
3. The p1 administration table displays both €2.5m total eligible costs and €2.5m requested grant. That display does not validate a 100% Accelerator funding rate or a new current budget. The detailed budget and applicable 2026 funding rules control.

These are bounded editorial corrections, not grounds to abandon the accepted commercial positioning. Recover the strong operational quantities, show their basis, and use a coherent current product baseline.

## 7. Direct instructions suggested for L2

1. Lead with the current TRL6 complete AirTransformer machine and its measured operating envelope. Present the EIC scope as product performance, reliability, industrialisation, qualification and deployment increments.
2. Rewrite §1.3 from current Savery ownership and actual CAU-family route. Retire the old CNRS/MIL-160 dependency narrative. Provide a compact rights map, filing/status table, current FTO scope and non-EU protection path.
3. Recover the core technical and commercial numerical case from the original proposal/test/economic sources. Fix units and ensure comparator conditions travel with the numbers.
4. Treat Norbert Stock and Aline Auroux as current scientific board members per user instruction; show their relevant contribution. Name the delivery owner of controls/dissipation work and map recruitment to WPs.
5. Include organisation-wide current composition and recruitment actions, with actual dated numbers; address non-executive roles as well as management. Do not use asterisks or generic non-assumption statements.
6. Use CETP 2026-2029, HPE site and TRL7 objective as real company progress and demonstration access per current user statement. Define the incremental EIC programme clearly alongside it; do not re-present already funded work as a new EIC-funded activity.
7. Preserve persuasive manufacturing/customer/finance specificity. Move internal source and uncertainty bookkeeping to the internal sidecar. A technical qualification that affects a claim belongs beside that claim; internal task IDs, open-item identifiers, 'L1 review', 'candidate' and drafting placeholders do not belong in an external proposal.
8. Prioritise a corrected full application pack and suitable reused video over a new animated production.

## Review status

Read-only source review completed. No proposal, financial workbook or original PDF was changed. No external messages sent.
