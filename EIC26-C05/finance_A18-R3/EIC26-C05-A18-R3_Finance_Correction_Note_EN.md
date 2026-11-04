# A18-R3 Financial Information: correction note

4 November 2026. This note replaces the A18-R2 annex. The corrected template is `EIC26-C05-A18-R3_Financial_Information_EN.xlsx`. The PDF is a LibreOffice preview; re-export it from Excel before upload.

## What was wrong in R2

**1. The EIC action was added on top of the business plan.**

R2 added €1.10m of R&D and €0.57m of capex over 2027–2029 that the business plan (G3.1, 21 Oct 2026) does not contain:

| Cost line | 2027 | 2028 | 2029 |
|---|---|---|---|
| R&D, R2 | €1.55m | €3.12m | €3.36m |
| R&D, business plan | €1.28m | €2.58m | €3.07m |
| Capex, R2 | €0.79m | €5.13m | €3.35m |
| Capex, business plan | €0.70m | €4.80m | €3.20m |

The business plan's budget already contains the action in every year:

| | EIC action (direct) | Business-plan budget |
|---|---|---|
| Running costs, Apr–Dec 2027 | €0.92m | R&D €1.02m |
| Running costs, 2028 | €1.61m | R&D €2.58m |
| Running costs, Q1 2029 | €0.20m | R&D €0.77m |
| Assets | €0.53m | €0.70m Seed test-and-preparation investment (fixtures, test instruments, small-batch preparation) |
| Action payroll (14 roles) | — | Business-plan R&D, factory, field and administration headcount: 18 by end 2027 |
| 25% indirect costs | — | Business-plan SG&A |

The grant therefore co-finances costs the business plan already contains; it does not create new costs.

**2. The Seed date was moved from March 2027 (business plan) to November 2027, while the plan's spending was kept from March 2027.**

This was the main cause of the negative cash.
- With company costs exactly as in the business plan, a November Seed still drives cash to −€1.02m in October 2027.
- With the business plan's March Seed, cash stays positive.
- EIC costs were a minor contributor.

**3. Opening cash was €300k (actual, 3 Nov 2026) against the business plan's €0.5m.** The R2 forecast does not cover this €128k shortfall before the Seed. The R3 cure is to start the business plan's January 2027 R&D step-up (€24k a month) with the Seed close in March instead. The 2027 annual total is unchanged.

## Corrected model (R3)

- **Company costs:** P&L, cash flow, working capital and capex are exactly the business plan's. EBITDA equals the business plan's EBITDA in every year.
- **Added only:**
  - grant receipts of €1.491m (April 2027), €0.621m (April 2028) and €0.373m (June 2029), with grant income recognised as eligible costs are incurred (€0.81m, €1.48m and €0.20m);
  - opening cash of €300k;
  - removal of the legacy €250k loan, consistent with management's statement that there is no debt.
- **Equity, nominal EUR:**
  - Seed €8m: €6m from other investors at first close in March 2027 (the business plan's date) and €2m EIC investment after EIC due diligence (November 2027);
  - Series A €25m in April 2028;
  - Series B €70m in January 2030;
  - business-plan fees.
  - Five-year net equity of €101.13m (EIC €2m, others €99.13m) is unchanged from R2.
- **Balance sheet:** balances in all five years (template check row = 0). The business plan's non-working-capital accruals (capitalised financing fees, restricted cash, interest accruals) are derived from its own cash flows, not plugged.

| k€ | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---:|---:|---:|---:|---:|
| Revenue | 480 | 1,562 | 8,535 | 26,718 | 75,244 |
| EBITDA (= business plan) | −2,263 | −6,617 | −8,062 | −14,027 | −7,640 |
| Grant income | 814 | 1,476 | 196 | 0 | 0 |
| Net result | −1,530 | −5,566 | −9,212 | −16,225 | −12,171 |
| Operating cash flow | −2,280 | −7,910 | −12,296 | −15,483 | −19,590 |
| Capex (= business plan) | −700 | −4,800 | −3,200 | −8,400 | −16,400 |
| Year-end cash | 6,530 | 25,872 | 13,050 | 67,807 | 36,907 |
| Year-end cash, business plan | 4,176 | 20,624 | 7,429 | 55,823 | 24,922 |

**Monthly cash is never negative.**
- Lowest point: +€26k in February 2027, before the Seed first close.
- After that: €4.84m in October 2027 and €5.59m in March 2028, before Series A.
- Full path: `EIC26-C05-A18-R3_Monthly_Cash_2027-2031.csv`.

**Table 2 fields completed:**
- C80: €66k/month (business-plan November 2026 burn; the October actual is still to be reconciled).
- C82: €95.88m cash needed to reach operating break-even (R2 showed €97.34m, which included the additive EIC costs).
- C83: 02/27 (current cash runs to the Seed first close).

## Text changes needed elsewhere (Seed timing)

**Part B §3.2:**
- l.426: replace "The round is planned to launch in September 2027 and close in November 2027." with "Other investors provide €6 million at a first close planned for March 2027; the EIC investment joins after EIC due diligence, expected in November 2027."
- l.442: replace "The €8 million Seed round is planned for a September 2027 launch and November 2027 close, including €2 million sought from the EIC." with "The €8 million Seed round closes in two steps: €6 million from other investors in March 2027 and €2 million from the EIC in November 2027. The first close and grant pre-financing fund the action from April 2027."
- Financing table, Seed row, planned timing: "First close March 2027; EIC tranche November 2027".

**Implementation Plan, WP6 description:** replace "planned September 2027 launch and November 2027 close" with "first close March 2027 with €6m from other investors; EIC €2m expected November 2027".

**Pitch deck and Part A:** apply the same two-step Seed wording.

## If the Seed must stay in September/November 2027

That choice is incompatible with the business plan as it stands: cash falls to about −€1.0m in October 2027 even with no EIC additions. One of the following would be needed:
- a pre-Seed bridge of about €1.1m (for example BSA-AIR) in Q1 2027; or
- rephasing the business plan's March 2027 hires and the €0.7m test facility to after the Seed close, which also moves the 2027–2028 reference deliveries and revenue.

Both options change the business plan, so R3 keeps the business plan's timing.
