# Red-team review of the full Part B, "Adsorption cooling / AWH" version (v6)

Reviewed: `EIC26-C05_PartB_Adsorption_AWH_20261104_EN.md/.pdf` (20 pages), its figures, and the A17-R2 Implementation Plan for cross-document consistency. Line numbers refer to the MD. Submission is today, so the items are ordered by effect on the score, and each has final wording.

## Verdict

This is the strongest version so far. New strengths:
- the MOF/CAU deep-tech section, with the Kiel University source;
- per-MW impact figures in §2.3;
- a much stronger team (two engineers, an interim CFO, a board with Corps des Mines engineers and a data-centre executive, three scientific advisers);
- the investor-leverage sentence;
- a simpler Figure 1.

Five items should be fixed before upload; together they take about 45 minutes. A list of residual sentences to delete follows. The document is at exactly 20 pages, and page 1 is half empty, so there is room for the summary addition without repagination.

## Must fix before upload

**1. The concept illustration shows a refrigerant compressor (p.3).** The cutaway in `ilab_p19_pilot_integration_concept.jpeg` shows a semi-hermetic reciprocating compressor with copper refrigerant lines and a finned coil, which is a conventional chiller layout. The proposal's headline is "cooling without vapour compression", and an HVAC evaluator will see the contradiction. Do one of the following:
- crop the image to the container exterior and the pipework, removing the cutaway; or
- delete it, which also frees about a quarter page.

If you keep it, number it (it is currently unnumbered while Figures 1 and 2 are numbered).

**2. "Adsorption cooling" invites the adsorption-chiller comparison, which §2.1 does not answer.** In HVAC, "adsorption cooling" usually means closed-cycle silica-gel or zeolite adsorption chillers driven by waste heat, which are already sold for data centres. With the new headline, an expert evaluator will ask how AirTransformer differs. Add one row to the Alternatives table (l.250–254):

> | Closed-cycle adsorption chillers (silica gel or zeolite) | Vacuum vessels and an evaporator–condenser cycle produce chilled water, which then needs air handling | Open-cycle staged MOF contactors treat the air directly at atmospheric pressure and deliver conditioned supply air |

**3. HPE's role differs between Part B and the Implementation Plan.**
- Part B (l.149) now describes CETP as an academic research programme with HPE Labs contributing integration expertise. It no longer names a field site (l.496: "Qin and the field lead will establish the installation scope…").
- The Implementation Plan (T4.1) still says "HPE is the confirmed CETP site", followed by EIC access to it.

Evaluators read both documents, so they must say the same thing. Choose one:
- **If HPE hosts the field qualification:** add to Part B l.496: "Field qualification takes place at the HPE site used in the CETP programme, under incremental EIC access arrangements."
- **If it does not:** in the Implementation Plan T4.1, replace "HPE is the confirmed CETP site." with "The field site is selected among the 2027 reference customers and CETP partners before the M12 review." Make the same change in risk row 3.1e "Field access".

**4. The evidence-gate table (l.478–486) is weaker than the Implementation Plan's milestones.** Use the same numeric criteria in both documents:

> | Engineering and verification baseline | M6 | Product specification, verification protocol and test plan approved (comparator, boundaries, uncertainty rule) |
> | Manufacturing configuration | M12 | Drawings and process window released; batches M4–M10 assessed; rights disposition recorded |
> | Batch and reliability qualification | M18 | Six batches qualified (12 contactors, 18 witnesses); 1,200 independent fixture-hours |
> | Product conformity release | M21 | 4,000 internal endurance hours; conformity file approved; safety-critical findings closed; software released |
> | Product qualification and acceptance | M24 | 1,600 field hours; ≥60% less electricity and ≥40% less make-up water at matched service; TRL8 decision |
> | Commercial production readiness | M26 | Serial tooling commissioned; manufacturing partner qualified; production release |
> | Initial commercial-deployment capability | M36 | Five installation/service packages delivered; application engineer and two technicians in post |

**5. The executive summary contains no proof point (your call; I recommend one sentence).** The summary is the first thing every evaluator reads, and at the moment it contains no number, TRL or ask. Page 1 has room. Insert before "Savery's ambition…":

> Savery's complete machine is at TRL6: in its 2025 EN test it delivered sensible cooling at an electrical COP of 20 with 60 °C waste heat, against about 3 for compression cooling in a heatwave. The EIC action qualifies a pre-series product at TRL8 by March 2029.

If you also want the ask, append: "We request a €2.49 m grant and €2 m EIC investment within an €8 m Seed round."

## Should fix (wording; about 20 minutes)

**Governance table (l.392–395).** "Allocation determined under the existing BSA-AIR conversion terms" reads as evasive, and "Total" in the Type column is odd. Replace with:

> | Name | Type (founder, investor, other) | % fully diluted |
> |---|---|---:|
> | CURMA SOLUTIONS, founder's holding company | Founder | 100% before conversion of BSA-AIR instruments |
> | TOTAL | | 100% |

**Team table.** Add Nicolas Paris (interim CFO, 30%), with his gender as recorded by the applicant. He is described in the text but missing from the template table.

**Scientific board.** Driss Stitou has no affiliation, unlike Stock and Auroux. Add it, for example "CNRS research scientist at PROMES". Verify the wording first.

**Terminology.** Part B uses "pre-series demonstrator" and "industrial unit" (l.143, l.476); the Implementation Plan uses "industrial qualification unit". At first mention in Part B, write "a dedicated pre-series demonstrator (the industrial qualification unit in the Implementation Plan)", then use one term throughout.

**Title.** "AirTransformer: Heat-Driven Cooling for Climate-Resilient Data Centres".

**§2.4: link water harvesting to drought adaptation.** Add after l.329: "In water-recovery mode, atmospheric water harvesting supplies treated water for on-site equipment cleaning, reducing withdrawals when drought restrictions apply."

**Residual defensive or bookkeeping sentences (delete).** These carried over from the R7 base and were already flagged in v5.

| Line | Delete |
|---|---|
| l.113 | "An identified parameter is used for control only when the available observations distinguish it sufficiently for the proposed decision." |
| l.117 | "This prevents a favourable operating fragment from moving restoration work outside the evaluation period." |
| l.143 | "This sequence preserves equipment availability for each planned activity." |
| l.145 | ", including unsuccessful runs and the effect of corrective work" |
| l.200 | "The inventory figures measure data-centre infrastructure capacity." |
| l.204 | "This independent sector benchmark retains its original geography, year and currency." |
| l.214 | "These percentages are planning comparisons with the company reference, rather than independently modelled shares of a 2032 regional SAM." |
| l.228 | Replace the whole paragraph with: "In grid-constrained sites, the released capacity can carry additional IT load. Site screening confirms that rack or industrial heat remains available while the machine cools." |
| l.240 | "These are effective displacement hours, not facility uptime; free cooling and the site's actual duty change the compression cooling displaced and therefore the return." and "Financing, taxes, degradation and major replacement are outside this simple cash comparison." |
| l.244 | "It leaves the company forecast's €110k equipment, €8k installation and €2k engineering package unchanged and does not assign a 100 kW rating to a forecast equipment unit." |
| l.248 | "The comparison must use the useful service the customer needs and the alternative it could actually install." |
| l.292 | "Procurement and production follow the unaccepted equipment pipeline rather than an unrestricted sales target." (or replace with "Procurement and production follow the order pipeline.") |
| l.306 | "The product is evaluated at a defined duty so that a machine result can be translated into an operational benefit." |
| l.310 | "; they are tracked separately from project effort and current headcount" |
| l.314 | "; compliance depends on the complete data-centre design and operation" |
| l.341 | "The Europe-and-North-America sales plan remains a company commercial plan; EU manufacturing, skills and installation outcomes are identified from the corresponding activities and deployments." |
| l.384 | "Professional support bridges its defined task without duplicating employee costs or assuming that the core can absorb every unfilled role." |
| l.399 | "Other members of the current team hold no options." (it answers the template's incentive question with a negative) |
| l.457 | "Early revenue and expenditure on upgraded-product qualification coexist in the plan." |
| l.488 | "Test operating hours and paid attendance are distinguished; internal technicians, engineers and priced facility operators cover their assigned preparation, operation, diagnosis and release duties." |
| l.516 | the whole paragraph (it repeats l.151) |

These deletions free about 450 words, roughly two thirds of a page. That absorbs the additions above and leaves margin under the 20-page limit.

## Already good (leave as is)

- The MOF/CAU section (l.35–41) with [R1] and [R32].
- The simplified Figure 1.
- The performance table and test-boundary note.
- §1.3 IP.
- The customer-value table.
- §2.3 impact figures.
- The expanded team and boards.
- The 40% gender target.
- The investor-leverage sentence (l.426).
- The sources-and-uses table.
- The risk table with the market rows.

On nationalities in §3.1: if they are included to pre-empt ownership or control questions, keep them. If space is tight, they can stay in the CVs only.
