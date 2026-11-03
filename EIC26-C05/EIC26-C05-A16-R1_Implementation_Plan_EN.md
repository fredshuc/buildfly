# AirTransformer Resilience Implementation Plan

Savery Tech proposes a 24-month programme to qualify a manufacturable and serviceable AirTransformer product from its existing TRL6 complete machine. The action concentrates on manufacturing transfer, batch consistency, reliability, product conformity and reproducible customer acceptance. The planned calendar is April 2027 to March 2029. The applicable grant agreement will determine the contractual start.

The requested blended financing combines a €2,485,583.33 grant with €2,000,000 EIC investment. Grant activities cost €3,550,833.33 and require €1,065,250.00 in co-financing. The investment sits within the €8m Seed target. Commercial production, sales and working capital have a separate investment work package.

## Table 3.1a Work package overview

| WP | Work package | Lead responsibility | Months | PM | Eligible EUR |
| --- | --- | --- | --- | --- | --- |
| 1 | Product requirements and engineering baseline | Frédéric / Qin | 1–6 | 23.000 | 282,250.00 |
| 2 | Manufacturing transfer and batch qualification | Qin / process engineer | 1–18 | 71.250 | 911,125.00 |
| 3 | Reliability controls and conformity validation | Qin / reliability engineer | 3–21 | 73.375 | 1,210,989.58 |
| 4 | Product qualification and reproducible deployment | Field engineer / Ina | 6–24 | 76.875 | 1,006,781.25 |
| 5 | Project management data IP and exploitation | Frédéric / data officer | 1–24 | 13.500 | 139,687.50 |
| Total | Five grant work packages | Savery Tech | 1–24 | 258.000 | 3,550,833.33 |

The product sequence releases an engineering baseline at M6, the manufacturing configuration at M12, qualified process batches and reliability results at M18, the conformity dossier at M21 and the TRL8 qualification package at M24. Recruitment and purchase decisions follow this sequence. The existing machine supports early work while the industrial qualification unit is prepared; the latter completes climate campaigns before field deployment.

CETP already supports the 2026–2029 research and HPE demonstration pathway towards TRL7. EIC uses its available results as technical inputs and funds distinct product qualification outputs. Independent EIC test access provides a completion path through March 2029 without relying on CETP deliverables scheduled later in 2029.


<!-- pagebreak -->

# Table 3.1b Work package descriptions

## WP1 Product requirements and engineering baseline

**Lead:** Frédéric, supported by Qin, Ina, thermal validation and reliability engineers. **Duration:** M1–M6. **Effort:** 23 PM. **Cost:** €282,250.

WP1 converts the demonstrated complete machine into a controlled product specification for heat-exposed urban facilities. Existing measured data and CETP research outputs establish the starting point. The work defines the duty, source and sink interfaces, maintainability and verification requirements for a repeatable product.

**T1.1 Requirements and interfaces, M1–M3, 40% of WP effort.** Ina and Qin specify the assigned cooling load, air conditions, regeneration source, heat rejection, power and water interfaces, installation limits and maintenance access. Comparison requirements use equal cooling service and include all auxiliaries and incumbent supplementation. Water performance prioritises external make-up saved; any recovered water use has a defined demand and qualification route.

**T1.2 Product baseline and measurement, M1–M6, 35%.** Frédéric and the thermal/test staff establish the current configuration, component versions and baseline control implementation. They define uncertainty, boundary tolerances, calibration and service acceptance methods. The independent metrology specialist reviews the protocol and the applicability of the methods to the machine. Existing TRL6 results remain distinct from the improvements tested in this action.

**T1.3 Product conformity and reliability requirements, M2–M6, 25%.** The reliability engineer and planned quality engineer identify applicable product requirements with the independent test body, define failure modes, safe states, environmental and contamination exposure and the required release evidence. The M6 review approves the test architecture before major qualification campaigns.

## WP2 Manufacturing transfer and batch qualification

**Lead:** Qin and the planned manufacturing process engineer. **Duration:** M1–M18. **Effort:** 71.25 PM. **Cost:** €911,125.00.

**T2.1 Design for manufacture and assembly, M1–M9, 35%.** The mechanical and process engineers turn the existing design into controlled drawings, BOM, assembly tolerances, leak checks, service access and supplier specifications. Reusable assembly/release jigs support repeatable builds. Critical parts receive an alternative-source review and incoming inspection criteria.

**T2.2 CAU processing and transfer, M3–M14, 30%.** The team qualifies the selected CAU variant's preparation, coating/shaping, conditioning and contactor interfaces. Six process batches test practical operating windows and repeatability. External specialists support transfer at five defined review blocks. The work preserves shaped-material transport and cyclic performance while replacing laboratory handling with reproducible instructions.

**T2.3 Batch qualification, M6–M18, 25%.** Six batches supply twelve reusable qualification contactors and eighteen sacrificial witnesses. Seventy-two external sorption/thermal sessions and eighteen destructive examinations support acceptance of each batch. Batches arriving in M4, M6, M8, M10, M12 and M14 are separately identified. Incoming, in-process and final criteria track dimensions, coating integrity, adsorption/transport response and traceability.

**T2.4 Manufacturing release, M9–M18, 10%.** Qin and quality staff close non-conformities and compile process windows, inspection methods, rework limits and release records. The independent assessor reviews three manufacturing releases and their evidence. Production tooling for later serial supply belongs to WP6.


<!-- pagebreak -->

# WP3 Reliability controls and conformity validation

**Lead:** Qin, the reliability engineer and planned quality/compliance engineer. **Duration:** M3–M21. **Effort:** 73.375 PM. **Cost:** €1,210,989.58.

WP3 qualifies product behaviour and failure management across the intended service envelope. It reuses the physical models, parameters and control knowledge available from Savery and CETP. EIC pays the work needed to release industrial software, validate reliability and complete product-specific conformity evidence.

**T3.1 Industrial control and software release, M3–M15, 25% of WP effort.** The embedded software engineer implements industrial interfaces, configuration control, diagnostics, logging, update mechanisms and deterministic operating/fallback states. The supervisory controls engineer specifies permitted setpoints and cycle decisions. Independent interlocks enforce temperature, pressure, air/water quality and actuator limits. Current implemented baseline control remains the reference.

**T3.2 Reliability and degradation, M5–M20, 35%.** The reliability engineer runs a planned 4,000-hour internal endurance programme using the dedicated fixture, with service-boundary variation, contamination and ageing exposures. Twelve independent 100-hour bay blocks provide a further 1,200 fixture-hours across qualification contactors. These are planned test hours, with failed periods and excluded metrology recorded. The tests assess leakage, pressure drop, coating integrity, cyclic capacity, switching, thermal interfaces, component drift, maintenance intervals and recovery after faults. The team reports uncertainty and extrapolation limits rather than converting hours automatically into lifetime years.

**T3.3 Independent conformity and product testing, M6–M21, 25%.** Five independent test blocks address the applicable electrical, mechanical, EMC and other configuration-specific requirements established in WP1. External testing includes the specified apparatus and operator. Savery owns the design response and technical file. Three independent reliability assessments connect failure observations to corrective work. Completion requires closure of safety-critical findings and a documented placing-on-market/putting-into-service route for the final configuration.

**T3.4 Supervisory optimisation and fallback validation, M7–M20, 15%.** Model-based/MPC and any retained learning policy operate as bounded supervisory functions. The team tests robustness against held-out climate/load trajectories, actuator faults, sensor drift and confidence loss. Safe fallback and human override remain outside the learning policy. Training, calibration and final acceptance data are separated. An independent software specialist checks fault responses and release evidence in two ten-day blocks. This task validates a deployable upgrade; it does not repeat CETP's base digital-twin or research-policy development.

The industrial qualification unit is ready for use at M10. Five twelve-day climate/load campaigns occupy M10–M14, before transfer and installation at the field site. The dedicated laboratory fixture remains available during field operation. A critical failure returns the affected version to correction and regression testing; the release gate applies to the revised configuration and evidence set.


<!-- pagebreak -->

# WP4 Product qualification and reproducible deployment

**Lead:** planned field deployment engineer, with Qin and Ina. **Duration:** M6–M24. **Effort:** 76.875 PM. **Cost:** €1,006,781.25.

WP4 establishes whether a defined product configuration can deliver the intended cooling service with an auditable operating and maintenance basis. HPE's CETP site provides a genuine integration pathway. The EIC programme identifies the incremental interfaces, tests and data needed for product qualification, with separate cost and test records. A controlled independent test configuration provides an alternative for product requirements that cannot be exercised at the site within the EIC calendar.

**T4.1 Application engineering and site readiness, M6–M16, 25% of WP effort.** Ina, the field engineer and Qin define the assigned noncritical cooling branch, available source/sink conditions, utility capacities, access, safety responsibilities, data permissions and acceptance protocol. Existing cooling remains available for continuity. Incremental interfaces are prepared in M13–M16. The M12 readiness review checks that the selected installation can supply the required test coverage; unresolved weather coverage is addressed through the independent climate facility rather than claimed as observed onsite.

**T4.2 Independent product qualification, M10–M19, 20%.** The same industrial qualification unit completes five climate/load campaigns in M10–M14. Requirements cover delivered air temperature and humidity ratio, cooling duty, electricity, thermal input and external make-up water under declared boundaries. Equal-service comparisons include all auxiliaries and retained-plant contributions. Product requirements established at M6 determine acceptance limits and the comparative test matrix. The team preserves complete raw data, uncertainty, operating modes and failed tests.

**T4.3 Incremental field qualification, M17–M24, 40%.** After transport and installation in M16, the product operates through eight months of monitored qualification. The plan provides 1,600 operating hours across M17–M23, including matched baseline/upgrade comparisons where demand and measured boundaries permit them. M24 allows analysis, corrective retest and acceptance. The field engineer coordinates access and maintenance; the reliability engineer and technician support diagnosis. External facility cover and remote shutdown do not substitute for Savery's scientific and release responsibilities.

Eight water campaigns supply 48 samples, including raw, treated, stored and duplicate samples. The initial recovered-water application is isolated, treated, non-aerosol equipment cleaning where a qualified demand exists. The installation water balance separately records external make-up, atmospheric capture, recovered liquid, inventory, discarded water, treatment and internal use. Water savings compare equal cooling service; future make-up applications require their own use qualification.

**T4.4 Acceptance and replication package, M19–M24, 15%.** Savery compiles commissioning instructions, service limits, maintenance/spare-part requirements, training and acceptance results. The final dossier combines manufacturing conformity, independent tests, field/equivalent-service evidence and customer requirements. The M24 decision targets TRL8 product qualification. It records remaining application limits and the corrective route alongside the demonstrated service.


<!-- pagebreak -->

# WP5 Management data IP and exploitation

**Lead:** Frédéric and the project data/coordination officer. **Duration:** M1–M24. **Effort:** 13.5 PM. **Cost:** €139,687.50.

**T5.1 Coordination and delivery, M1–M24, 40% of WP effort.** Frédéric owns product decisions, milestone acceptance, resources and the funding interface. The officer maintains task, procurement and role-month records. Monthly reviews check recruiting, supplier readiness, expenditure, risks and CETP allocation. Quarterly steering reviews approve design or schedule changes and ensure they preserve a credible route to M24 qualification.

**T5.2 Data and product IP, M1–M24, 35%.** The officer maintains a controlled repository, access rights, configuration/sample identities and preservation of raw measurements. A data management plan is due at M6 and updated with material changes. Frédéric and specialist advisers manage Savery-owned system IP, process know-how, software and contractor rights. Product/territory claim mapping and professional FTO review precede affected commercial commitments. CETP data reuse follows the relevant consortium and background-access conditions, with separate EIC cost records.

**T5.3 Communication and exploitation, M1–M24, 25%.** Ina supplies application requirements and the post-qualification adoption route. The M6 dissemination, exploitation and communication plan identifies audiences, protected results, cleared technical outputs and measurable follow-up. Three public technical outputs are planned after IP review. Ordinary sales campaigns and commercial deployment expenditure belong to WP6.

## WP6 Manufacturing deployment and commercial service launch

**Funding:** investment and other Seed sources, outside the grant cost total. **Duration:** M12–M36. **Planned uses:** €2,112,500. A planned HVAC/data-centre business-development lead joins at M12, with a service application engineer at M19 and two service technicians from M25.

| Use | EUR | Window |
| --- | --- | --- |
| Serial-production tooling after qualification design freeze | 300,000.00 | M19–M26 |
| Manufacturing-partner production readiness and capacity | 350,000.00 | M19–M30 |
| HVAC and data-centre business-development lead | 212,500.00 | M12–M36 |
| Service application engineer | 135,000.00 | M19–M36 |
| Two service technicians | 120,000.00 | M25–M36 |
| First five commercial installation and service packages | 175,000.00 | M25–M36 |
| Channel development and customer acquisition | 120,000.00 | M19–M30 |
| Peak initial manufactured inventory | 550,000.00 | M25–M36 |
| Receivables working-capital envelope | 150,000.00 | M25–M36 |

The requested investment allocates €1.9m to WP6 and €100,000 to grant-action co-financing. Other Seed sources finance the €212,500 business-development post and the remaining action cash contribution. Manufacturing readiness supports one nominal 100kW-equivalent delivery slot per month during 2029, rising to two per month in 2030. Planned sales of five, ten and fifteen equivalents in 2029–2031 leave installation and production buffers. These are capacity assumptions for the commercial plan, not the rating of the existing machine or booked orders.


<!-- pagebreak -->

# Tables 3.1c and 3.1d Deliverables and milestones

| ID | Deliverable | WP | Type | Level | Month |
| --- | --- | --- | --- | --- | --- |
| D1.1 | Product requirements and interface specification | 1 | R | SEN | 3 |
| D1.2 | Baseline configuration and product verification protocol | 1 | R | SEN | 6 |
| D2.1 | Design for manufacture and assembly package | 2 | OTHER | SEN | 6 |
| D2.2 | CAU process window and batch quality specification | 2 | R | SEN | 12 |
| D2.3 | Manufacturing batch qualification and release package | 2 | R | SEN | 18 |
| D3.1 | Reliability control and conformity test plan | 3 | R | SEN | 6 |
| D3.2 | Reliability results and corrective-action record | 3 | DATA | SEN | 18 |
| D3.3 | Industrial software and product conformity dossier | 3 | OTHER | SEN | 21 |
| D4.1 | Application engineering and acceptance plan | 4 | R | SEN | 12 |
| D4.2 | Incremental product and field qualification results | 4 | DATA | SEN | 20 |
| D4.3 | TRL8 product qualification and acceptance dossier | 4 | R | SEN | 24 |
| D4.4 | Installation maintenance and replication package | 4 | OTHER | SEN | 24 |
| D5.1 | Data management plan | 5 | DMP | SEN | 6 |
| D5.2 | Dissemination exploitation and communication plan | 5 | R | SEN | 6 |
| D5.3 | Product IP and rights management plan | 5 | R | SEN | 6 |
| D5.4 | Final data and exploitation handover | 5 | R | SEN | 24 |

R means report, DATA a dataset and OTHER software, design or technical documentation. Sensitive technical records use controlled access. Public technical communication follows IP review and the communication plan; sensitivity does not prevent the grant's reporting obligations.

| ID | Milestone | Month | Verification |
| --- | --- | --- | --- |
| MS1 | Engineering and verification baseline | 6 | Approved duty/interfaces, baseline machine configuration, methods, uncertainty and safety/reliability plan |
| MS2 | Manufacturing configuration release | 12 | Controlled design, qualified process window, initial independent batch results and industrial-unit climate evidence |
| MS3 | Batch and reliability qualification | 18 | Six batch records, independent tests, reliability evidence and closure plan for non-conformities |
| MS4 | Product conformity release | 21 | Closed safety-critical findings, industrial software regression and complete applicable conformity evidence |
| MS5 | Product qualification and acceptance | 24 | Traceable manufacturing, reliability, independent and field/equivalent-service results support TRL8 decision |
| IM1 | Commercial production readiness | 26 | Production release, supplier capacity and service organisation support initial deliveries |
| IM2 | Initial commercial deployment | 36 | First five nominal 100kW-equivalent installation/service packages and operating support capacity |

The investment milestones follow product qualification and are excluded from grant deliverables and grant costs. Frédéric signs the technical milestone decision with the responsible work-package lead. Independent tests inform the decision without transferring Savery's product responsibility.


<!-- pagebreak -->

# Table 3.1e Personnel and monthly capacity

| Role | Responsible person or recruitment | Function | Start–end | PM | EUR per PM |
| --- | --- | --- | --- | --- | --- |
| R01 | Frédéric | System/product direction | M1–M24 | 12.000 | 9,000 |
| R02 | Qin | Engineering/integration | M1–M24 | 21.000 | 7,000 |
| R03 | Ina | Application requirements/acceptance | M1–M24 | 12.000 | 6,500 |
| R04 | Planned | Thermal validation | M1–M18 | 18.000 | 7,500 |
| R05 | Planned | Supervisory controls | M3–M20 | 18.000 | 7,500 |
| R06 | Planned | Manufacturing process | M1–M24 | 24.000 | 6,500 |
| R07 | Planned | Reliability/test engineering | M1–M24 | 24.000 | 6,000 |
| R08 | Planned | Assembly/test technician | M1–M24 | 24.000 | 4,500 |
| R09 | Planned | Field engineering | M7–M24 | 18.000 | 6,500 |
| R10 | Planned | Project data/coordination | M1–M24 | 12.000 | 5,000 |
| R11 | Planned | Mechanical DfM | M1–M21 | 21.000 | 6,500 |
| R12 | Planned | Quality/compliance | M4–M21 | 18.000 | 6,500 |
| R13 | Planned | Manufacturing qualification technician | M4–M21 | 18.000 | 4,500 |
| R14 | Planned | Embedded industrial software | M4–M21 | 18.000 | 7,000 |

The programme allocates 258 PM, averaging 10.75 full-time equivalents over 24 months and peaking at 12.375 in the central engineering period. Each individual role stays at or below one full-time equivalent; Frédéric contributes 0.5, Qin 0.875, Ina 0.5 and the data officer 0.5 during their active months. A person-month represents 143.33 planning hours. The combined role-month allocation contains 36,980 hours, including 6,020 technician hours, with every active month assigned to a work package.

The new process, reliability, DfM, quality and industrial-software roles address distinct productisation responsibilities. Thermal and supervisory-control staff validate deployable performance rather than repeat CETP base research. Recruitment for M1 posts starts during grant preparation; M4 and M7 posts follow the staged work plan. Supplier-supported interfaces and the existing TRL6 platform protect early progress if a recruitment is delayed, while the steering review reschedules affected tests before committing to a release date.

Norbert Stock and Aline Auroux contribute as scientific board members on materials and adsorption/thermodynamic measurement. Scientific-board participation is separate from the paid project PM above. Frédéric chairs the product review; Qin owns engineering change and release. Ina connects actual use requirements, acceptance and the commercial team. The officer tracks allocation across projects so the same employee time is charged once.

The 42 technician PM and 24 reliability-engineer PM cover setup, operation, calibration support, interpretation and corrective testing. An independent facility supplies its own operator and emergency response where priced. Internal attention is scheduled alongside the external 1,200 fixture-hours and sixty climate days, with the laboratory fixture retained while the qualification unit operates onsite.


<!-- pagebreak -->

# Budget and procurement

## Table 3.1f Cost summary

| Category | EUR | Calculation basis |
| --- | --- | --- |
| Personnel | 1,648,500.00 | 258 PM using role-specific monthly employer-cost estimates |
| Subcontracted tasks | 325,000.00 | Seven scoped independent technical tasks |
| Travel and subsistence | 51,750.00 | 64 person visits by WP |
| Equipment depreciation | 170,916.67 | Attributable active use of six asset groups |
| Goods and services | 709,500.00 | Physical quantities, facility use, assays and services |
| Indirect costs | 645,166.67 | 25% of personnel and purchases, excluding subcontracting |
| Total eligible cost | 3,550,833.33 | Unrounded calculation basis |
| Grant request | 2,485,583.33 | 70% of eligible cost |
| Non-grant contribution | 1,065,250.00 | 30% of eligible cost |

## Table 3.1g Subcontracting

| Task | WP | Driver | EUR |
| --- | --- | --- | --- |
| Independent metrology and uncertainty review | 1 | 20 days × €1,300 | 26,000.00 |
| Industrial CAU process transfer support | 2 | 50 days × €1,200 | 60,000.00 |
| Independent product safety and conformity test programme | 3 | 75 days × €1,400 | 105,000.00 |
| Independent reliability and failure assessment | 3 | 30 days × €1,300 | 39,000.00 |
| Independent site acceptance and water-use qualification | 4 | 30 days × €1,100 | 33,000.00 |
| Independent manufacturing qualification review | 2 | 30 days × €1,200 | 36,000.00 |
| Independent industrial software validation | 3 | 20 days × €1,300 | 26,000.00 |

Savery retains system architecture, core product design, interpretation, integration and release decisions. External suppliers deliver the stated independent specialist tasks. Routine apparatus access, assays and calibration are separately costed as purchased services. Selection compares technical competence, independence, scope, quality, schedule and price through a documented value-for-money process. Normal procurement and conflict-of-interest controls apply.

Estimates use the inherited company project-cost model and explicit 3 November 2026 task quantities. The employer-cost estimates range from €4,500 to €9,000 per PM. Future purchasing uses comparable prior engineering estimates and defined campaign quantities. Final implementation follows normal accounting, reasonable cost and applicable eligibility rules. Scope changes update quantities and allocations, rather than adding a balancing provision to reach the grant ceiling.


<!-- pagebreak -->

# Equipment services and funding

## Table 3.1h Purchases and asset treatment

| Asset group | Purchase EUR | Ready for use | Life months | Action depreciation EUR |
| --- | --- | --- | --- | --- |
| CAU coating conditioning and process fixtures | 75,000.00 | M4 | 60 | 26,250.00 |
| Product metrology and data acquisition set | 72,000.00 | M2 | 60 | 27,600.00 |
| Internal endurance and contamination fixture | 60,000.00 | M5 | 60 | 20,000.00 |
| Reusable qualification contactor charges | 60,000.00 | M4, 6, 8, 10, 12, 14 | 36 | 26,666.67 |
| Design for assembly and release jigs | 42,000.00 | M3 | 60 | 15,400.00 |
| Industrial qualification field unit excluding contactors | 220,000.00 | M10 | 60 | 55,000.00 |

Equipment acquisition totals €529,000; only €170,916.67 attributable depreciation enters eligible costs. Six separately commissioned contactor batches give a purchase-weighted sixteen-month use period. Existing TRL6 equipment and CETP-funded capability are reused without charging their acquisition again. Internal staff effort included as personnel is excluded from capitalised equipment price.

The chosen hybrid approach buys limited process-transfer, assembly, metrology and endurance fixtures while purchasing independent climate, assay, calibration and specialist capacity. Facility services include actual access, apparatus or metered services; reusable equipment is treated as an asset. Alternative purchase, service and compliant rental offers are compared against the same task, capacity, duration and accounting basis before commitment.

Goods/services total €709,500. The main packages are the dedicated engineering bay (€108,000), sixty climate/load days (€132,000), 1,200 independent fixture-hours (€108,000), process batches and qualification assays (€108,900), field interfaces/access/transport (€73,000), water media/analyses (€25,200) and the remaining calibration, process, software, IP and communication services. The detailed budget identifies each quantity and delivery month.

The action cash profile includes full asset payments: €3,908,916.67, compared with €3,550,833.33 eligible cost. The €358,083.33 purchase/depreciation difference joins the €1,065,250 non-grant eligible share, requiring €1,423,333.33 beyond the grant over the action. EIC investment is planned to cover €100,000 of this amount; other Seed sources cover €1,323,333.33. Grant payment timing affects liquidity separately.

The €8m Seed target includes the €2m EIC investment request and €6m from other sources. €1.9m of the investment supports WP6; the remaining €100,000 supports the innovation action. Other Seed sources also fund the €212,500 business-development role. These are financing targets with defined uses and milestones. Purchase and employment commitments follow demonstrated funding availability and delivery readiness.


<!-- pagebreak -->

# Delivery risk and CETP separation

## Table 3.1i Critical risks and measures

| Risk and likelihood | Effect | Owner and measures |
| --- | --- | --- |
| Recruitment or supplier delay. Medium. | Design/test readiness slips. | Qin stages M1/M4/M7 recruitment and quotes. Existing machine and supplier-supported interfaces preserve early work. Reschedule affected test slots before design freeze. |
| CAU shaping loses performance or consistency. Medium. | Batch or service requirements fail. | Process engineer uses six traceable batches, witness analyses and rework limits. Independent reviews at M9/M12/M18 support corrective process changes. |
| Ageing contamination or component failure. Medium. | Maintenance and lifetime targets fail. | Reliability engineer links 4,000 internal hours and 1,200 independent fixture-hours to fault analysis, replacement and regression tests. Commercial service limits follow results. |
| Software/sensor faults or unsafe optimisation. Medium. | Cooling interruption or unsafe state. | Qin and software staff retain deterministic interlocks, bounded supervisory control, diagnostics and fallback. Independent validation and versioned regression precede release. |
| Field access or useful weather coverage falls short. Medium. | Incomplete onsite service evidence. | Field engineer approves readiness by M12. Controlled climate campaigns finish before site transfer. Use equivalent tests for missing boundaries and report actual field coverage. |
| Finance or prefinancing arrives late. Medium. | Recruitment or procurement liquidity pressure. | Frédéric gates commitments on available funding, phases equipment and maintains an explicit receipt-delay cash case. Seed targets and investment requests do not become cash receipts. |
| CETP scope or use overlaps. Medium. | Double funding or unavailable inputs. | Data officer maintains task, employee-month, equipment-use and invoice separation. Reuse existing data under access terms; EIC uses independent product qualification if later CETP outputs slip. |
| Third-party rights or conformity findings. Medium. | A production or market route requires adjustment. | Frédéric commissions current product/territory claim analysis and quality engineer closes applicable product findings before affected commercial release. |

CETP's characterisation, kinetics, heat/mass-transfer models, cycle mapping, digital-twin/RL research and HPE integrated validation are the research background. EIC's controlled industrial design, process/batch specifications, reliability evidence, conformity file, service instructions and product acceptance are distinct foreground outputs. The data officer records the source and licence of reused information; the accountant and WP lead confirm exclusive time and usage allocation. CETP grant funds do not co-finance the same EIC cost.

The calendar provides a completion route through March 2029 using the existing TRL6 machine, the industrial qualification unit and independent facilities. Available CETP evidence improves design and context, while any result delivered later in 2029 sits outside the EIC critical path. Monthly steering reviews check this dependency explicitly. Final product acceptance combines completed engineering work, positive and negative test results, conformity evidence and defined application limits.

