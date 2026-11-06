#!/usr/bin/env python3
import json,pathlib,csv,hashlib,math,subprocess
from collections import Counter
R=pathlib.Path(__file__).resolve().parents[1];m=json.loads((R/'03_budget/implementation_model.json').read_text());s=json.loads((R/'03_budget/calculated_snapshot.json').read_text())
def tab(h,rows):return '| '+' | '.join(h)+' |\n| '+' | '.join(['---']*len(h))+' |\n'+'\n'.join('| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in rows)+'\n'
def f(x):return f'{x:,.0f}'
refs=R/'04_evidence';reviews=R/'05_reviews';refs.mkdir(exist_ok=True);reviews.mkdir(exist_ok=True)
assumptions=tab(['ID','项目','实际状态／读取等级','采用口径与待关闭事项'],m['assumptions'])
budget=tab(['伙伴','PM','人员费','直接费','间接费','推荐总额','相对起点'],[[b['partner'],b['pm'],f(b['personnel']),f(b['direct']),f(b['indirect']),f(b['total']),f(b['change'])] for b in s['partners']])
roles=tab(['伙伴／岗位','PM','平均FTE','峰值FTE','预留FTE上限','最少人数'],[[r['partner']+' / '+r['role'],r['pm'],f"{r['average_fte']:.2f}",f"{r['peak_fte']:.2f}",r['planned_fte_capacity'],r['minimum_people']] for r in s['roles']])
decision=f'''# MAT61 Section 3 设计决策与工作假设

任务 MAT61-L2-S3-T01-R1；2026年11月6日；当前为L2完整设计候选，等待L1审阅。以下是实施设计与计算，不是已完成的实验或伙伴承诺。

## 本轮收敛结果

固定五方、七WP、22任务、224 PM、36个月。单Module按用户后续明确要求采用 **10 kW**，替代本轮早期的小功率草算；交付源文件、Word、Excel、CSV和校核均采用10 kW。推荐预算 **€{f(s['total_budget'])}**，上限下尚余 **€{f(m['ceiling_eur']-s['total_budget'])}**。原€2.40m为设计目标，规模修正增加€87,225；不把余额列成预备费。

技术责任链已在任务、接口及验收层面闭合。人员姓名、设备使用权、合成产线及实际报价的执行证据尚未齐全；本件不声称已完成这些机构性确认，也不因其缺失而停在WP标题层。

## 主要设计选择

1. **主要热服务**：55 °C源、25 °C排热、65→70 °C热水升级，单个完整双床Module以10 kW为机械和有用热基准。源热需同时包括蒸发和再生，假设热比0.4时约25 kW；有用水路约1.72 m³/h。额外八次只做相邻供水温度的转移检验，不建另一种机器或现场demo。
2. **库存由问题推导**：20 kg活性干MOF（每床10 kg）、动态摆幅0.15 kg/kg、吸附焓2.8 MJ/kg-water、完整床循环600 s、可利用比例0.75，对应10.5 kW。半周期约300 s。摆幅0.08时仅5.6 kW，故10 kW是设计点，不是已证明的材料或整机性能。低容量配置仍报告可行域；5 kW共同服务只用于合格的部分负荷比较，不改机械基准。
3. **机械共用与独立重复分开**：一套10 kW平台，四对可复用载体／接口，十二套独立成型双床内部件；不是十二台整机。参考／新材料×颗粒／导热结构形成四物理配置，每配置三独立组。控制与历史在同一组内配对，不能当成额外材料独立重复。
4. **粉体与合成**：早期57次小／中批合成共6.12 kg；最终180次独立1 kg合成共180 kg新材料。六个不交叠的30 kg投料组，在85%有效回收率下各得25.5 kg活性MOF：20 kg装机、1.5 kg保留表征、4 kg归档／损失／返工。参考粉体共200 kg，含三个独立60 kg生产批和20 kg早期库存；从A批余量再拨4 kg，使早期成型进料达到24 kg，足够20.4 kg活性库存。最终参考两路线每批所需原料约47.1 kg，A批仍足够。
5. **先锁可生产配方再持续机制研究**：M9四组成下选，M12从确认候选中选择一个可生产配方；M13–M23完成最终粉体，M24成型和资格确认。三个1 kg生产单元每月各180机时，11个月共5,940机时，对5,760机时需求余180机时。该时间裕度很小，实际产能必须核实，不能用“现有量热仪”代替。样本组A/B/C按M19/M21/M23逐次放行。
6. **两条主要shaping路线**：颗粒／温和挤出和导热复合／整体结构；继承HESTIA的材料—传递—循环匹配。薄涂层只作为必要参考，不另开第三条开发路线，避免变成常规涂层优化项目。
7. **早期双线并行**：参考台架M1起建、M8合格；模型M1、控制M3、参考成型M2启动。M24联合冻结，M25–M32初始比较，M33–M34明确纠正与复测，M35–M36转移及证据包。总集成验证窗口12个月。CPM的两条门控主线均在M24汇合；两个月纠正是有任务和资源的管理缓冲，不是额外免费浮时。
8. **控制公平性**：固定周期充分离线优化；经济型MPC充分调参；RL实质控制热分配、切换、蒸汽输运及压力辅助。共用信息、动作约束、状态估计和允许的边界预测。每种策略每物理配置六个完整开发历史；控制CPU预算每策略最多1,500 h，余500 h用于集成，另计RL适用GPU。最终数据不能反向调参。
9. **实验量与能力边界**：最终4×3×4×3=144次完整运行，每次8 h含4 h服务、2 h复位和2 h准备／稳定。另32次驱动消融、72次控制开发、24次复测、8次转移；主台架共2,104 h。24个寿命试样×500循环在独立设备上，占1,000 chamber-hours。三独立组只能支持相应精度，不能保证小于10%的效应显著；正文给出n=3时t区间半宽约2.48×组间标准差。
10. **完整边界**：泵、阀、蒸汽循环、压缩、控制用电、再生／蒸发源热、复位与初末库存全部核算。实验室用于施加源热／排热边界的设备电耗另记，避免既把源热作为热输入又把其制备电耗重复算成机器电耗。预算仍支付真实实验室能源，41 MWh×€180/MWh=€7,380直接成本。

## 人员月与预算

{budget}

总人员费€1,458,000；设备使用€174,000；差旅€50,000；其他货物服务€307,780；直接费€1,989,780；间接费€497,445。无分包、无第三方补助、无预备费。人员费率是含雇主成本的假设，不是个人工资。设备采用租赁或经核实的折旧／项目使用比例，不自动按购置全额计费；设施机时与付费人员工时不等同。

与初始分配相比，Savery增加€71,725，IRCELYON增加€38,000，IKTS增加€17,500，UPorto减少€55,000，HPE增加€15,000。增加项源于10 kW下的粉体、内部件、热源／蒸汽设备及实验能源；保留44 PM建模和26 PM控制。

人工费率普涨5%时总额€2,578,350；再叠加设备／设施／算力基数€274,000涨10%时为€2,612,600，超上限€112,600。参考粉体单独升至€200/kg时总额€2,499,725；新MOF生产耗材单独升至€300/kg时为€2,498,475；两者不能同时吸收。统一人员费率仅有约0.70%上调空间。推荐预算符合上限，但成本鲁棒性有限，不能标成已核价或伙伴已接受。

## 岗位负荷

{roles}

每个任务先按其活跃月份均匀摊PM，再聚合月度和六个月阶段FTE。岗位按伙伴PM比例作当前阶段分配，因此是讨论用负荷模型；实际具名人员排程仍需伙伴确认。一个岗位若峰值超过1 FTE则给出至少两个人的分担，不将其伪装成单人的可用时间。未将DOE人员的真实工资或Aline在另一项目的角色自动移植至IRCELYON。

## 能力、法人及设施状态

Savery：技术职责和候选协调人Frédéric Cui明确；实验室宿主、压力／真空责任、具体人员及10 kW设备租用／所有权未落实。IRCELYON：机构公开资料支持吸附量热及材料表征，不等于已落实多组分MOF合成、三套1 kg产线或6,372合成总机时。IKTS：用户确认on board；公开材料支持MOF造粒、挤出与结构化，不推定本项目设备预约或性能已达标。UPorto：公开周期吸附及模型／优化／控制能力有依据；团队姓名和44 PM排程未获确认。HPE Galway：Galway研发据点有公开依据；本项目具名MPC／RL／HIL人员和算力须确认。

IRCELYON科研单位不直接当作申报法人；CNRS或UCBL签约及PIC单独核对。IKTS科研所与Fraunhofer申报法人、PIC分开。HPE Galway是团队／地点，不能直接冒充法人。没有因此添加第六方。

## 统一内部确认表

{assumptions}

这些事项集中用于L1及后续伙伴资源核实；本轮不发送邮件、不采购、不预约、不承诺经费、不登录Portal。机构性未确认项不会被自动改写为已落实事实。

## 文件与模板边界

用户原RTF实际为V5.1，2026-01-22；不是任务书所述通用V5.0。保留原始字节及SHA-256。适用表3.1a–h已逐字段对照；3.1h仅要求设备成本超过该伙伴人员费15%时说明，Savery为€128,000/€396,000=32.32%。Word正文和表格均≥11 pt，A4、四边16 mm；图注及图中文字单独可读。后续仍需与登录后的本call提交会话表单、标签和最终Part A核对，不能称Portal-final。

Section 3保留完整实施细节，当前版面页数见QA结果；全Part B的40页预算仍由L1统一分配。模板给3.1/3.2的页数仅是建议，不用缩小字体实现压页。来源读取等级与旧稿继承范围见Source_and_Reuse_Log.md。
'''
(reviews/'Design_Decisions_and_Assumptions_CN.md').write_text(decision)

source='''# Source and reuse log

Task MAT61-L2-S3-T01-R1, read and prepared on 6 November 2026. This log describes actual access, not inferred possession of a document. It is a controlled internal record.

## Reading grades

A: original file or authoritative decision document, with relevant content read. A-scoped: official primary source, specified sections read. B: scientific extract/readback rather than the complete final original. C: reconstruction or continuity summary. U: direct current user instruction. A decision document proves the decision it records; it does not turn an inaccessible underlying proposal into a fully read original.

| ID | Source and actual version | Access and grade | Reuse and boundary |
| --- | --- | --- | --- |
| U1 | Current L1 brief MAT61-L2-S3-T01-R1, 2026-11-06 | Current message, full, U | Five participants, whole scientific chain, seven-WP start, 36-month choice, EUR2.40m target/EUR2.50m ceiling, permissions and deliverables. |
| U2 | User amendment during execution | Current message, U | Single Module uses 10 kW because 1 kW mechanical components are unsuitable. Re-sized inventory, flow, production, equipment and budget; no earlier sub-kW recommendation survives. |
| U3 | User confirms Git connection and authorises repository operations | Current message, U | Repository writes/push authorised within original confidentiality restrictions. No permission inferred to publish unpublished IP or private sources. |
| S1 | User-provided Tpl_Application Form (Part B) (HE RIA and IA).rtf | Original local bytes, A; V5.1 dated 22 January 2026 | Full text extracted using Pandoc; headings and fields 3.1a-h, equipment threshold, body/table minimum 11 pt, A4 and margins checked. Original kept unmodified. Authenticated call-session form and tags not accessed. |
| S2 | EC WP 2026–2027 Part 7, C(2026) 6687/2 of 29 September 2026 | A-scoped, call overview p21 and MAT61 pp74–75 | Contribution up to EUR2.50m, maximum six independent eligible entities, up to TRL4 and SRIA contribution. No topic-specific mandatory 36-month duration or lump-sum exception claimed. |
| S3 | IAM4EU SRIA, November 2024 | A-scoped, P#11/#12/#14, printed pp47–49, and context | Maps traceability, predictive material performance and sustainability to real tasks; does not claim that the project covers all partnership priorities. |
| S4 | EC WP General Annexes A and G, 2026–2027 | A-scoped | Submission-session form priority; 40-page general full-RIA limit absent an override; actual-cost RIA planning basis, 100% and 25% with exclusions. Portal/Part A must still be checked. |
| H1 | ERC_COG_2026_B1.pdf, 10 pages | Library original parsed in full, A; libfile_48db1699ea748191bd95aadb902a466b | Material energetics, mixed-linker/mixed-metal levers, reproducible production, three shaping classes, coupled transport/cycle/control and trajectory losses. Two main shaping routes funded here; third coating class remains a diagnostic reference. Original targets are not achieved results. |
| H2 | HESTIA_ESR_2026.pdf, five-page available extract | Library original parsed in full, A; libfile_2393d9a6bd1081919a6583b41a800486 | Addresses unclear breakthrough attribution, data demand and critical synthesis role through discriminating experiments, explicit workload and real capacity gaps. No copied claims of achievement. |
| G1 | Pasted markdown(1).md, 508 parsed lines | Full available scientific extract, B; libfile_b17bd6def43481918c0f8a427266b63a | GRACE sections 1.2/1.3 describe vapour transport, branch compression, bypass comparisons, H1–H3, state estimation and RL. Not the complete signed/submitted GRACE Part B; version identity not independently established. |
| G2 | 101351924_GRACE_ESR.pdf, seven available PDF pages | Library original parsed in full, A; libfile_7862a638a4cc8191a16c3b97289442a9 | Explicitly fixes evaluator criticism of sequential implementation and insufficient buffers; retains physical/digital coupling and adds economic/resource risks. ESR evaluates that proposal, not this new consortium. |
| G3 | 01_GRACE_ENPULSE_PRECURSOR_EVIDENCE.md, 867 lines | Entire file read in two windows, C; libfile_10d01ff910a8819182d3c0457fe4e5f7 | Useful hidden-state, intervention and data-provenance synthesis. Its own warning says official source proposals were unavailable to its author; never used as proof of measured GRACE results. |
| F1 | DOE27_T04_ACCEPT_WITH_ACTIONS_T05_T06_R1_20261014.zip | Original ZIP downloaded, extracted and relevant L1 review/source log read, A decision; libfile_218dc1e0fbd08191ada01f8739cac6f4 | Fair M0/Mc/Mz observation mappings; local chemical work versus adsorption heat/whole-system exergy; timing/temperature sensitivity and receiver/reset boundary. Underlying T04 L2 original not reconstructed as read. |
| F2 | DOE27_T07_ACCEPT_WITH_ACTIONS_T09_R1_20261014.zip | Original ZIP and complete included English science readback read, A decision / B science; libfile_5429aa3e3b4481919b28df3818673e11 | Competing transport/population/internal-state models, same-state opposite-history tests, fixed mappings, complete-history holdouts and independent resets. T07 text is not labelled latest final science. |
| F3 | DOE27_T10B_ACCEPT_T11_INPUT_GATED_20261018.zip | Original acceptance ZIP and full L1 final review read, A decision; libfile_4c167c4a4ad88191ae645d2fd59c85ae | Confirms science acceptance and its boundaries; preserves distinction between support for an extra state and frozen-parameter transfer. Accepted scientific DOCX/PDF are not present in this review ZIP. |
| F4 | DOE27_R10prime_L1_FINAL_SUBMISSION_AUDIT_20261029.zip | Latest accessible original audit ZIP and full L1 audit read, A decision; libfile_a53d66c7ab0481919b19a913839d6fba | Later material-selection rule: thermodynamic/measurement qualification before dynamic model selection, then freeze with declared calibration and unseen challenges. Latest R10prime science main file itself was not obtained. Do not retain T07's single-material restriction as current MAT61 scope. |
| S5 | IRCELYON ATARI and chemical/textural facility pages | Official pages opened and relevant sections read, A-scoped | Supports calorimetry/material characterisation; not named synthesis personnel, three 1 kg trains, booked access or project cost. |
| S6 | Fraunhofer IKTS Shaping of MOFs page | Official page opened and relevant section read, A-scoped | Direct MOF shaping capabilities, including granulation/extrusion/monoliths. No project booking or guarantee of retained uptake. |
| S7 | UPorto LSRE-LCM Cyclic Adsorption Processes | Official page opened, A-scoped | Modelling, simulation, optimisation and control background, not this project's named team or reserved effort. |
| S8 | HPE Galway R&D announcement dated 2 October 2023 | Official page opened, A-scoped | Establishes historical Galway R&D presence, not project-specific RL staffing, a data-centre demo or free compute. |
| S9 | NIST Chemistry WebBook water Antoine coefficients, 304–333 K | Primary NIST source retrieved, A-scoped | A=5.20389, B=1733.926, C=-39.485 with P in bar and T in K; combined with ideal-gas water-vapour density for approximate design-flow verification, not a compressor performance map. |

## Source access limitations and unsuccessful routes

The authorised desktop inventory showed DESKTOP-39O8NE4 offline. The Windows paths recorded in DOE audit files therefore do not establish that this session read the latest scientific main file. Library title/content searches resolved the above materials; no complete final GRACE Part B was found. Patent drafts returned by search were not opened or copied into this work.

The CNRS-hosted Auroux CV URL returned 404 on direct open, and the FEUP thesis record returned 403. Neither failed fetch is used as the sole final evidence. The final document uses the accessible IRCELYON institutional pages and LSRE-LCM page. An ALiCE page timed out; it is not needed for the final factual claim. Public institutional capability never substitutes for a project access agreement.

## URLs

S2 https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026-2027/wp-7-digital-industry-and-space_horizon-2026-2027_en.pdf

S3 https://www.iam-i.eu/wp-content/uploads/2025/02/SRIA-Innovative-Advanced-Materials-for-Europe.pdf

S4 https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026-2027/wp-15-general-annexes_horizon-2026-2027_en.pdf

S5 https://www.ircelyon.univ-lyon1.fr/team/atari/ and https://www.ircelyon.univ-lyon1.fr/facility/analyse-chimique-texture/

S6 https://www.ikts.fraunhofer.de/en/departments/structural_ceramics/processes_and_components/shaping/cr_shaping_of_MOFS.html

S7 https://lsre-lcm.fe.up.pt/areas/1

S8 https://www.hpe.com/us/en/newsroom/press-release/2023/10/hewlett-packard-enterprise-creates-more-than-150-roles-at-new-cloud-rd-center-in-galway-ireland.html

S9 https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=20D

## Reuse decisions

Adopt the provided official table schema, standard mass/energy balances, reference water-stable MOFs and existing low-temperature shaping knowledge. Wrap measured actuator and sensor behaviour in a common simulator and HIL interface. Build the discriminating experiment, inter-partner data contract and common resource ledger specific to this project. Do not copy another action's WP budget, TRL result, apparatus dimensions, personnel salary or access entitlement.

HESTIA's proposed efficiency targets and GRACE's first-of-kind/pilot claims are not imported as achieved results or novelty proof. DOE's local chemical-work argument is not promoted to whole-machine savings; later qualification/freeze rules take precedence over the older readback. The user fixed the current scientific chain and five-participant scope; no earlier alternative consortium is revived.

The original template SHA-256 is 507cc6ad2831936b3b41e2bed6ec784cb1c50ba61b1e8dd80590639565575977. The original uploaded archive SHA-256 is e38469b3b65ffa8625b31c150f8acfe650dbdbaf5f7738d2d708d7541e849281. Parsed temporary source extracts remain outside the repository. No private payroll, unpublished formula or patent body is embedded in the public index.
'''
(refs/'Source_and_Reuse_Log.md').write_text(source)

contract={'version':'MAT61-IF-R1','status':'DESIGN_NOT_MEASURED','units':'SI, absolute pressure, water loading per active dry MOF','release_control':'M24 freeze; later versioned corrections preserve original prospective results','fields':[
 ['sample_id','string','n.a.','Immutable planned/actual specimen identifier'],['synthesis_batch_id','string','n.a.','One separately prepared synthesis, not a sampled time point'],['forming_lot_id','string','n.a.','Separately manufactured lot'],['assembly_group_id','string','n.a.','Independent material/assembly block A B or C'],['nominal_composition','component fractions','mol/mol','Feed composition; distinct from measured product'],['measured_composition','component fractions','mol/mol','Measured composition and phase identification'],['active_dry_mof_mass','number','kg','Dry active MOF only'],['shaped_dry_mass','number','kg','MOF plus binder/conductive phase'],['substrate_mass','number','kg','Separate hardware/substrate mass'],['water_loading','number','kg-water/kg-dry-MOF','Dry and wet bases never mixed'],['adsorption_enthalpy','loading-dependent array','J/mol-water','Uncertainty and uptake coordinate required'],['conductivity','tensor or scalar','W/(m K)','Orientation and validity range'],['permeability','tensor or scalar','m2','Geometry/process-specific'],['contact_resistance','number','m2 K/W','Measured thermal interface'],['time','array','s','Native timestamps and clock/lag calibration'],['temperature','array','K','Boundary and sample coordinates distinguished'],['vapour_pressure','array','Pa absolute','Never gauge pressure'],['volumetric_flow','array','m3/s','Measured state p/T recorded; not unlabelled normal flow'],['heat_flow','array by channel','W','Source evaporation/regeneration, useful, rejected and leak estimates'],['electrical_power','array by feeder','W','Pump valve vapour mover compressor electronics and fixture separately'],['liquid_water_inventory','array','kg','Measured reservoir inventory with uncertainty'],['state_definition','versioned list','mixed SI','Candidate bed/wall temperatures, loadings, vapour/liquid inventories and any qualified internal state'],['observation_mapping','versioned callable','n.a.','All candidate model classes predict common measurements, including structure where qualified'],['action_definition','versioned list','mixed SI','Heat allocation, timing, vapour conductance and branch pressure assistance'],['constraint_contract','versioned object','SI','Equipment maps and permitted domain confirmed before deployment'],['model_estimator_policy_hash','string','n.a.','Exact executable version and tuning manifest'],['forecast_contract','versioned object','SI and s','Same permitted exogenous information for all controllers'],['fallback_event','timestamped log','s','Command, realised action, interlock cause and recovery'],['run_split','enum','DEV / CALIBRATION / FINAL / CORRECTION','Whole history/block split; no random point split'],['initial_final_inventory','structured values','kg and J','Closure against 2% working-transfer/stored-energy rule'],['uncertainty','covariance and calibration records','corresponding SI','Expanded and model uncertainty distinguished']],
 'handoffs':m['interfaces'],'prospective_holdout':'Group C, complete C09-C12 waveforms and endpoint responses are not fitting data. Routine QC is permitted under frozen rules. Final waveform draws remain sealed until the M24 manifest.'}
(refs/'Interface_Data_Contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')

matrix=[]
for material in ['REFERENCE','NEW']:
 for route in ['GRANULE','CONDUCTIVE']:
  for group in ['A','B','C']:
   for condition in ['C09','C10','C11','C12']:
    for policy in ['FIXED','MPC','RL']:
     matrix.append(dict(planned_run_id=f'PLAN-{material}-{route}-{group}-{condition}-{policy}',material=material,route=route,group=group,condition=condition,policy=policy,active_dry_mof_kg=20,module_nominal_kW=m['service']['nominal_kw'],target_duty_kW=next(c[5] for c in m['conditions'] if c[0]==condition),service_hours=4,reset_hours=2,setup_hours=2,total_hours=8,status='PLANNED_NOT_RUN'))
with (R/'03_budget/CSV/Validation_Matrix.csv').open('w',newline='',encoding='utf-8-sig') as f0:
 w=csv.DictWriter(f0,fieldnames=matrix[0].keys());w.writeheader();w.writerows(matrix)

task_contract='''# 已领取任务与规模修正

2026年11月6日领取MAT61-L2-S3-T01-R1，完成Section 3.1/3.2、官方适用表、任务、人员月、预算、甘特及依赖、源记录、QA和集中回件。固定Savery、IRCELYON、Fraunhofer IKTS、UPorto、HPE Galway，36个月工作假设，规划上限€2.50m。完整科学链、TRL4实验室边界及保密/权限限制沿用用户本轮任务书。

执行期间用户追加：单Module以10 kW为基准，1 kW找不到对应机械组件。该指令已成为最终硬件与热服务基准，旧小功率草算撤销。随后用户确认Git连接应恢复并授权操作repo。该授权适用于任务内的仓库读写及安全推送，不取消不公开未发布知识产权、私人工资或伙伴商业数据的限制。

输出以同一mat-prod受控根目录为准，不增第六方，不外发邮件、不采购付费、不预订、不作伙伴承诺、不提交Portal。
'''
(reviews/'Accepted_Task_and_10kW_Amendment_CN.md').write_text(task_contract)
print('Review documents, interface contract and 144 planned validation rows generated')
