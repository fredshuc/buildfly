# 2. Impact

## 2.1 Project’s pathways towards impact

### From materials design to industrial qualification

European developers of water-based adsorption equipment need a reproducible route from multicomponent sorbents to manufacturable adsorbers. A favourable powder isotherm can indicate regenerability. Useful duty depends on how the shaped material exchanges heat and water vapour, how its properties vary across lots, and how the assembly performs through cycling and reset. The project will establish which combinations of composition, production process, shaping and control can meet a given service. A positive proof of principle provides the foundation for a class of modular adsorption heat transformers that use variable low-grade waste heat to supply controllable hot water.

The project links four decisions in one design process. Multicomponent metal–organic frameworks (MOFs) tune the water uptake window. Cycle-relevant fingerprints quantify usable working capacity, loading-dependent energetics, rates and ageing. Permeable granules and conductive structures change vapour access and thermal resistance in distinct ways. Non-equilibrium models and state estimates connect the resulting properties to useful power, regeneration and switching. Constrained reinforcement learning (RL) then allocates energy flows through thermal inputs, vapour circulation, selective pressure assistance and timing. Its contribution is assessed against an optimised fixed cycle and economic model predictive control (MPC) at matched service, with common constraints and metered losses. The resulting design rules show which combinations expand useful operating range, which incur excessive losses, and where a simpler control policy suffices.

**Results at month 36.** Savery will carry out synthesis from exploratory batches to research production on a single 5 kg line, with 36 planned production lots at nominal batch size. IRCELYON will coordinate materials research and independently characterise thermodynamics, kinetics and ageing. Fraunhofer IKTS will establish two forming windows and qualify reproducible cartridge sets. The University of Porto (UPorto) and HPE Galway will deliver models, estimation and comparative control evidence. One nominal 10 kW mechanical module will validate the combined design in the laboratory, with technology readiness level (TRL) 4 as the endpoint. The 144 planned prospective runs, organised across three independent assembly blocks, will give users a bounded map of repeatability, service feasibility and losses. In cases where pressure assistance or learned control adds little net benefit, the map will identify the conditions under which designers should use the passive path or a simpler policy.

**Outcomes after the project.** Materials laboratories can reuse the characterisation methods and reference cases. Equipment designers and controls integrators can test thermal interfaces and control strategies against bounded models before committing to hardware. Heat users and integrators can use the measured operating envelope to specify the evidence required for a relevant-environment trial.

### Contribution to IAM4EU and European industrial competitiveness

The action addresses the topic's two expected outcomes [1]. The **open-ended industrial breakthrough** is a predictive route from materials chemistry and production to component performance under real cycle constraints, tested at TRL 4. The **knowledge pipeline** will include material fingerprints, forming windows, validated design rules and matched benchmarks. Researchers and engineers can use these outputs to select and qualify future materials and components, including when a particular formulation or control strategy proves unsuitable.

**Predicting performance and lifecycle of materials (IAM4EU P#12).** This is the primary contribution [2]. Multiphysics, multiscale models link composition and loading-dependent energetics to transport in the shaped adsorber and performance in operation. Independent material characterisation and instrumented cycle histories connect chemistry and physics to production, processing and use. Predictions on withheld histories test whether the models can specify which material and forming tolerances will meet a given duty. Ageing evidence and uncertainty define where these predictions can support material selection and subsequent lifetime qualification. Evidence comes from D2.1–D2.2, D3.1–D3.2, D4.2 and D6.2.

**FAIR materials data, resource efficiency and Safe and Sustainable by Design.** Under P#11, common identifiers, units, test conditions and uncertainty metadata link the synthesis lot, formed component and complete test history. Cleared data and benchmark packages will follow the Findable, Accessible, Interoperable and Reusable (FAIR) principles. Under P#14, D7.2 links synthesis, solvent recovery, activation, forming yield, replacement and end-of-life assumptions to qualified performance. This supports early Safe and Sustainable by Design (SSbD) decisions and identifies where improved yield, durability or recovery could make production more resource efficient and support circularity. D3.1 also contributes to the thermal energy management application of P#6 through the engineered sorbent–carrier interfaces that govern thermal contact, vapour access and mechanical integrity [2].

**Pathway to industrial uptake.** The batch records and two forming windows allow European synthesis and component teams to set evidence-based acceptance criteria. The validated models let equipment manufacturers and integrators use these criteria to design, specify and qualify adsorbers for a given duty. The next step is pilot tooling and repeat manufacture at larger scale, followed by relevant-environment validation with an equipment integrator and a heat user. Through knowledge valorisation, European suppliers gain the capability to develop, manufacture and qualify innovative advanced materials for industrial equipment. This contributes to European competitiveness and autonomy in advanced materials. Digital qualification supports the green and digital transition, with resource-efficient materials production and industrial decarbonisation as longer-term benefits [1].

### Scale and significance of the energy application

Recoverable waste heat can become a local supply for a heat network or an industrial process. Suitable early applications include warm-liquid-cooled data centres and industrial facilities with variable low-grade heat and coincident demand. A representative application couples a 45 °C source to 70 °C supply. A sufficiently cool network return can accept lower-temperature heat before the final lift. Site qualification depends on source temperature and flow, the available heat sink, demand coincidence and safe integration without interrupting cooling. The laboratory module establishes materials-to-equipment evidence for this next stage of development.

An EU inventory estimated around 2,400 TWh/year of heat below 100 °C in 2018, with about 96% of it at 25–80 °C. Power generation dominated that inventory [3]. The scenarios below illustrate the scale and gross heat value that subsequent technology adoption could address under stated assumptions.

**Table 2-1. Illustrative European waste-heat recovery scenarios**

| Parameter | Conservative | Mid | Stretch |
| --- | ---: | ---: | ---: |
| **EU data centres** | | | |
| 2030 electricity input assumption (TWh/year) | 115 | 115 | 115 |
| Assumed useful heat recovery share | 10% | 20% | 30% |
| Illustrative useful heat (TWh/year) | 11.5 | 23.0 | 34.5 |
| Gross annual heat value at €25–40/MWh (€bn/year) | 0.3–0.5 | 0.6–0.9 | 0.9–1.4 |
| **EU industrial heat** | | | |
| Broad inventory below 100 °C (TWh/year) | ~2,400 | ~2,400 | ~2,400 |
| Assumed variable sub-segment below 60 °C (TWh/year) | ~1,200 | ~1,200 | ~1,200 |
| Assumed useful capture share of that sub-segment | 1% | 2.5% | 5% |
| Illustrative useful heat (TWh/year) | 12 | 30 | 60 |
| Gross annual heat value at €25–40/MWh (€bn/year) | 0.3–0.5 | 0.8–1.2 | 1.5–2.4 |

The table uses independent scenario denominators and assumed recovery shares. The 115 and ~1,200 TWh/year inputs are sector-scale assumptions. Site evidence is needed to estimate the addressable resource. The cases are separate and the values are gross, before integration and operating costs. As a separate environmental illustration, displacing 10 TWh/year of gas-fired useful heat at an assumed 0.20 t CO₂/MWh would avoid about 2 Mt CO₂/year gross. Net effects depend on the heat actually displaced, auxiliary energy and the lifecycle burden of manufacture and replacement. Site selection and offtake require evidence from a later demonstration.

## 2.2 Measures to maximise impact - Dissemination, exploitation and communication

### Exploitable results and intended users

| Result family and delivery | Proposed exploitation lead and contributors | Use, release and next evidence |
| --- | --- | --- |
| **1. Composition and production fingerprints** (D2.1, D2.2) | Savery for synthesis and production transfer. IRCELYON for thermodynamics, kinetics and independent characterisation. | Materials researchers and production engineers can select compositions and screen batch variation against cycle duty. Publish methods and cleared reference data. Keep sensitive recipe and process details under controlled access. Verify reproducibility and cost at larger batch size. |
| **2. Shaped adsorbers and manufacturing windows** (D3.1, D3.2) | Fraunhofer IKTS, with Savery and IRCELYON. | Process engineers can use qualified forming windows, tolerances and test methods. Equipment integrators can use the released interface. Protect proprietary forming and joining parameters where justified. Verify pilot tooling, yield, supplier variability and cartridge life. |
| **3. Models, state estimation and control** (D4.1, D4.2, D5.1) | UPorto for model and estimator reuse. HPE Galway for control qualification and deployment methods. | Thermal-system designers and controls engineers can size and test operating strategies using bounded models, benchmark datasets and stable interfaces. Release cleared methods and reproducible benchmarks. Review implementation code, data rights and dependencies before any software release. Test transfer, safety fallback and integration on a relevant installation. |
| **4. Integrated design rules and TRL 4 evidence** (D6.1, D6.2, D7.2, D7.3) | Savery with all partners. | Equipment and energy-service teams can use qualified operating envelopes, failure boundaries and lifecycle sensitivities for site and product design. Release comparative evidence and performance limits in redacted form. Verify scale, field reliability, economics and buyer requirements before equipment deployment. |

**From evidence to equipment.** Savery’s first commercial offering would be complete heat-recovery equipment. An integrated thermal system would follow once hydraulic, control and service responsibilities can be specified. Energy-as-a-service (EaaS) or cooling-as-a-service (CaaS) would require bankable metering, uptime and maintenance evidence and a contract that allocates performance and offtake risk. CaaS is a later system route. The laboratory service in this action is heat upgrading. Materials and control results support these equipment and system routes and can also be used in partner research or transfer work under agreed terms.

After laboratory validation, Savery and a prospective host would establish the source–sink profile, isolation and fail-safe conditions, footprint and qualified-duty metering for a relevant-environment prototype. IKTS and Savery would then use pilot tooling and multiple batches to verify cost, yield, durability and serviceability, while UPorto and HPE Galway would qualify model and controller transfer. At the next investment decision, a host or heat offtaker would review service evidence and operating responsibilities. Integrators would review the installation and maintenance scope. An investor or internal capital committee would receive cost, life, metered performance, rights and contract evidence to assess an initial equipment deployment. Follow-on engineering could use company and partner resources or a separately qualified collaborative R&I opportunity. The current action funds the evidence and roadmap.

### Protection, access and reproducibility

The consortium will identify relevant background and its legal owner before use, including pre-existing cycle and hardware know-how, materials and forming methods, data, and software. It will record the rights needed for project implementation and review the terms needed for subsequent equipment, manufacturing and software exploitation separately. Any transfer or exclusive licence will be checked against the grant terms, including the topic’s provision for objection by the granting authority up to four years after the action [1]. Existing patent application activity on heat-exchanger technology forms part of the background review. The parties will check ownership, territorial coverage, status, third-party claims and dependencies for the intended design and market. A product-specific freedom-to-operate assessment is a separate decision input before deployment.

The party generating a result records its origin and relevant contributions. Results jointly generated with inseparable contributions are addressed through the applicable grant and consortium agreements. Exploitation leadership assigns responsibility for taking a result forward. The results register identifies actual legal owners and agreed access conditions before release and informs the ownership list in the final report [4]. Before external disclosure, partners will identify foreground suitable for protection, check third-party restrictions and agree which methods, data and code can be released. Patents, confidential manufacturing know-how and software copyright or licensing will be considered according to the result. Public releases will retain the protocol, reference or redacted data, uncertainty and benchmark results needed to reproduce published claims. Sensitive recipes, site data and product code will remain under access controls where required.

### Dissemination, exploitation and communication plan

**Dissemination to research and engineering users.** Six research outputs are planned for submission. They cover composition and batch fingerprints, forming and transport, non-equilibrium mechanism tests, model and estimator transfer, comparative constrained control, and integrated heat-service validation. Authors will select materials, thermal engineering and control venues suited to each result. Each output will pair its main claim with an appropriate protocol, reference data and, where applicable, executable benchmarks. The project will record submissions and released evidence. Three technical exchanges on materials and manufacturing, modelling and control, and heat integration will use existing academic and industry channels where possible. The events will record audience and technical feedback and route it to the relevant result owner.

**Exploitation with prospective users.** Savery will coordinate six structured requirements interviews, with a planning split across cooling operators, heat users or network operators, and equipment or integration specialists. The interviews will capture source and sink ranges, operating hours, allowable downtime, footprint, maintenance and commercial screening conditions. Requirements will be logged by user group and compared with the measured operating envelope and the D7.2 assessment. This will give the subsequent developers a ranked set of evidence gaps and reject conditions. D7.3 will record routes for the four result families and distinguish public findings from rights-sensitive evidence for later diligence.

**Communication to wider audiences.** From project start, Savery and partner institutions will use their existing web and communication channels to explain why variable heat is difficult to recover and how advanced materials and controls can improve the design. Updates at planning, evidence review and close will distinguish laboratory findings from later site deployment. Public technical exchanges and cleared summaries can reach materials and manufacturing associations, industrial R&I networks and regional energy planners. Reporting guidance on useful heat and boundary conditions may be informed by the metering protocol and lessons from failed or marginal cases. Public materials will acknowledge EU support and use the visibility wording and emblem required by the grant.

WP7 leads and resources these measures through its 13 person-months and planned dissemination purchases. D7.1 establishes the dissemination, exploitation and communication plan at M6. The plan is updated at M18 and M36. D7.2 at M32 assesses environmental and economic boundaries using the evidence available at that stage. D7.3 at M36 checks the exploitation implications against final validation and consolidates the public evidence and protected roadmap. The M4 data management plan supports access, metadata and verification separately. Following the action, exploitation leads will maintain cleared releases and use the roadmap to assess transfer and funding opportunities as evidence and resources permit.

## 2.3 Summary

| Key element | Impact pathway |
| --- | --- |
| **Specific needs** | A reproducible route from advanced sorbent chemistry through production and shaping to predictable component performance and operating limits. |
| **D & E & C measures** | Six research submissions, three technical exchanges, six user requirements interviews, four result records, and public updates through existing channels. Release follows rights and evidence review. |
| **Expected results** | Composition and production fingerprints, two forming windows and qualified cartridges, predictive models and comparative controls, and TRL 4 design evidence from one nominal 10 kW laboratory module. |
| **Target groups** | Advanced-materials and process engineers, thermal equipment and controls integrators, data-centre cooling operators, industrial and network heat users, and researchers. |
| **Outcomes** | Adoption of reproducible batch and component qualification methods, predictive design and traceable materials data. Preparation for later pilot manufacture and relevant-environment validation. |
| **Impacts** | Stronger European capacity and competitiveness in innovative advanced materials and industrial equipment, supporting resource-efficient production, the green and digital transition and longer-term industrial decarbonisation. |

### References

[1] European Commission, *Horizon Europe Work Programme 2026–2027, Digital, Industry and Space*, Part 7, pp. 36–38 and 74–75, Decision C(2026) 6687/2 of 29 September 2026. [Work programme](https://research-and-innovation.ec.europa.eu/document/download/87a8c19b-2643-49ec-8d07-37781ceb516e_en).

[2] IAM4EU, *Strategic Research and Innovation Agenda*, November 2024, pp. 31–32 and 47–52. [SRIA](https://www.iam-i.eu/wp-content/uploads/2025/02/SRIA-Innovative-Advanced-Materials-for-Europe.pdf).

[3] Luberti, M., Gowans, R., Finn, P. and Santori, G., *An estimate of the ultralow waste heat available in the European Union*, Energy 238 (2022), 121967. [Original inventory](https://doi.org/10.1016/j.energy.2021.121967).

[4] European Commission, *EU Grants Annotated Grant Agreement*, Article 16 and Horizon Europe Annex 5. [Annotated Grant Agreement](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/common/guidance/aga_en.pdf).
