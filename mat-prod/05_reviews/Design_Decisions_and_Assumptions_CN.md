# MAT61 Section 3 设计决策与工作假设

任务 MAT61-L2-S3-T01-R1；2026年11月6日；当前为L2完整设计候选，等待L1审阅。以下是实施设计与计算，不是已完成的实验或伙伴承诺。

## 本轮收敛结果

固定五方、七WP、22任务、224 PM、36个月。单Module按用户后续明确要求采用 **10 kW**，替代本轮早期的小功率草算；交付源文件、Word、Excel、CSV和校核均采用10 kW。推荐预算 **€2,487,225**，上限下尚余 **€12,775**。原€2.40m为设计目标，规模修正增加€87,225；不把余额列成预备费。

技术责任链已在任务、接口及验收层面闭合。人员姓名、设备使用权、合成产线及实际报价的执行证据尚未齐全；本件不声称已完成这些机构性确认，也不因其缺失而停在WP标题层。

## 主要设计选择

1. **主要热服务**：55 °C源、25 °C排热、65→70 °C热水升级，单个完整双床Module以10 kW为机械和有用热基准。源热需同时包括蒸发和再生，假设热比0.4时约25 kW；有用水路约1.72 m³/h。额外八次只做相邻供水温度的转移检验，不建另一种机器或现场demo。
2. **库存由问题推导**：20 kg活性干MOF（每床10 kg）、动态摆幅0.15 kg/kg、吸附焓2.8 MJ/kg-water、完整床循环600 s、可利用比例0.75，对应10.5 kW。半周期约300 s。摆幅0.08时仅5.6 kW，故10 kW是设计点，不是已证明的材料或整机性能。低容量配置仍报告可行域；5 kW共同服务只用于合格的部分负荷比较，不改机械基准。
3. **机械共用与独立重复分开**：一套10 kW平台，四对可复用载体／接口，十二套独立成型双床内部件；不是十二台整机。参考／新材料×颗粒／导热结构形成四物理配置，每配置三独立组。控制与历史在同一组内配对，不能当成额外材料独立重复。
4. **粉体与合成**：早期57次小／中批合成共6.12 kg；Savery最终36次独立5 kg合成共180 kg新材料。六个不交叠的30 kg投料组，在85%有效回收率下各得25.5 kg活性MOF：20 kg装机、1.5 kg保留表征、4 kg归档／损失／返工。参考粉体共200 kg，含三个独立60 kg生产批和20 kg早期库存；从A批余量再拨4 kg，使早期成型进料达到24 kg，足够20.4 kg活性库存。最终参考两路线每批所需原料约47.1 kg，A批仍足够。
5. **先锁可生产配方再持续机制研究**：M9四组成下选，M12从确认候选中选择一个可生产配方；M13–M23完成最终粉体，M24成型和资格确认。Savery 一条5 kg线按每月180机时、每批32小时（含清洗周转）估算，11个月1,980机时，36批需1,152机时，余828机时。每批合格干粉量和实际节拍待验证。样本组A/B/C按M19/M21/M23逐次放行。
6. **两条主要shaping路线**：颗粒／温和挤出和导热复合／整体结构；继承HESTIA的材料—传递—循环匹配。薄涂层只作为必要参考，不另开第三条开发路线，避免变成常规涂层优化项目。
7. **早期双线并行**：参考台架M1起建、M8合格；模型M1、控制M3、参考成型M2启动。M24联合冻结，M25–M32初始比较，M33–M34明确纠正与复测，M35–M36转移及证据包。总集成验证窗口12个月。CPM的两条门控主线均在M24汇合；两个月纠正是有任务和资源的管理缓冲，不是额外免费浮时。
8. **控制公平性**：固定周期充分离线优化；经济型MPC充分调参；RL实质控制热分配、切换、蒸汽输运及压力辅助。共用信息、动作约束、状态估计和允许的边界预测。每种策略每物理配置六个完整开发历史；控制CPU预算每策略最多1,500 h，余500 h用于集成，另计RL适用GPU。最终数据不能反向调参。
9. **实验量与能力边界**：最终4×3×4×3=144次完整运行，每次8 h含4 h服务、2 h复位和2 h准备／稳定。另32次驱动消融、72次控制开发、24次复测、8次转移；主台架共2,104 h。24个寿命试样×500循环在独立设备上，占1,000 chamber-hours。三独立组只能支持相应精度，不能保证小于10%的效应显著；正文给出n=3时t区间半宽约2.48×组间标准差。
10. **完整边界**：泵、阀、蒸汽循环、压缩、控制用电、再生／蒸发源热、复位与初末库存全部核算。实验室用于施加源热／排热边界的设备电耗另记，避免既把源热作为热输入又把其制备电耗重复算成机器电耗。预算仍支付真实实验室能源，41 MWh×€180/MWh=€7,380直接成本。

## 人员月与预算

| 伙伴 | PM | 人员费 | 直接费 | 间接费 | 推荐总额 | 相对起点 |
| --- | --- | --- | --- | --- | --- | --- |
| SAV | 78 | 468,000 | 777,780 | 194,445 | 972,225 | 252,225 |
| IRC | 36.0 | 216,000 | 270,000 | 67,500 | 337,500 | -142,500 |
| IKTS | 40.0 | 320,000 | 414,000 | 103,500 | 517,500 | 17,500 |
| UP | 44.0 | 220,000 | 276,000 | 69,000 | 345,000 | -55,000 |
| HPE | 26.0 | 234,000 | 252,000 | 63,000 | 315,000 | 15,000 |


总人员费€1,458,000；设备使用€174,000；差旅€50,000；其他货物服务€307,780；直接费€1,989,780；间接费€497,445。无分包、无第三方补助、无预备费。人员费率是含雇主成本的假设，不是个人工资。设备采用租赁或经核实的折旧／项目使用比例，不自动按购置全额计费；设施机时与付费人员工时不等同。

与初始分配相比，Savery增加€252,225，IRCELYON减少€142,500，IKTS增加€17,500，UPorto减少€55,000，HPE增加€15,000。增加项源于10 kW下的粉体、内部件、热源／蒸汽设备及实验能源；保留44 PM建模和26 PM控制。

人工费率普涨5%时总额€2,578,350；再叠加设备／设施／算力基数€274,000涨10%时为€2,612,600，超上限€112,600。参考粉体单独升至€200/kg时总额€2,499,725；新MOF生产耗材单独升至€300/kg时为€2,498,475；两者不能同时吸收。统一人员费率仅有约0.70%上调空间。推荐预算符合上限，但成本鲁棒性有限，不能标成已核价或伙伴已接受。

## 岗位负荷

| 伙伴／岗位 | PM | 平均FTE | 峰值FTE | 预留FTE上限 | 最少人数 |
| --- | --- | --- | --- | --- | --- |
| SAV / Scientific coordinator | 12 | 0.33 | 0.56 | 0.6 | 1 |
| SAV / Integration engineers | 30 | 0.83 | 1.39 | 1.5 | 2 |
| SAV / Experimental technicians | 20 | 0.56 | 0.93 | 1.0 | 2 |
| SAV / Project and data officer | 4 | 0.11 | 0.19 | 0.2 | 1 |
| SAV / Synthesis scientist and technical operator | 12 | 0.33 | 0.56 | 0.85 | 2 |
| IRC / Materials scientific lead | 6 | 0.17 | 0.36 | 0.4 | 1 |
| IRC / Sorption and materials researchers | 20 | 0.56 | 1.19 | 1.65 | 2 |
| IRC / Laboratory technicians | 10 | 0.28 | 0.60 | 0.9 | 2 |
| IKTS / Shaping scientific lead | 6 | 0.17 | 0.35 | 0.4 | 1 |
| IKTS / Process researchers | 24 | 0.67 | 1.41 | 1.5 | 2 |
| IKTS / Manufacturing technicians | 10 | 0.28 | 0.59 | 0.8 | 2 |
| UP / Modelling scientific lead | 8 | 0.22 | 0.43 | 0.5 | 1 |
| UP / Dynamic modelling researchers | 30 | 0.83 | 1.61 | 1.8 | 2 |
| UP / Research software engineer | 6 | 0.17 | 0.32 | 0.4 | 1 |
| HPE / Control scientific lead | 6 | 0.17 | 0.28 | 0.4 | 1 |
| HPE / Control and HIL researchers | 20 | 0.56 | 0.93 | 1.3 | 2 |


每个任务先按其活跃月份均匀摊PM，再聚合月度和六个月阶段FTE。岗位按伙伴PM比例作当前阶段分配，因此是讨论用负荷模型；实际具名人员排程仍需伙伴确认。一个岗位若峰值超过1 FTE则给出至少两个人的分担，不将其伪装成单人的可用时间。未将DOE人员的真实工资或Aline在另一项目的角色自动移植至IRCELYON。

## 能力、法人及设施状态

Savery：技术职责和候选协调人Frédéric Cui明确；实验室宿主、压力／真空责任、具体人员及10 kW设备租用／所有权未落实。IRCELYON：机构公开资料支持吸附量热及材料表征，具名人员与仪器时段待确认；Savery负责全部合成，单条5 kg线的净干粉产量、机时与可计费成本待核实。IKTS：用户确认on board；公开材料支持MOF造粒、挤出与结构化，不推定本项目设备预约或性能已达标。UPorto：公开周期吸附及模型／优化／控制能力有依据；团队姓名和44 PM排程未获确认。HPE Galway：Galway研发据点有公开依据；本项目具名MPC／RL／HIL人员和算力须确认。

IRCELYON科研单位不直接当作申报法人；CNRS或UCBL签约及PIC单独核对。IKTS科研所与Fraunhofer申报法人、PIC分开。HPE Galway是团队／地点，不能直接冒充法人。没有因此添加第六方。

## 统一内部确认表

| ID | 项目 | 实际状态／读取等级 | 采用口径与待关闭事项 |
| --- | --- | --- | --- |
| A01 | 36 months | L2 design choice | Duration is not quoted as a mandatory call rule. |
| A02 | Personnel rates | Unconfirmed planning rates | EUR/PM 6000 SAV and IRC, 8000 IKTS, 5000 UP, 9000 HPE; eligible employer cost, not salary or partner commitment. |
| A03 | Legal entities and PICs | Unconfirmed | Savery Tech SAS is supported by the later DOE source but current HE signatory/PIC needs verification; IRCELYON research unit and CNRS/UCBL signatory are separate; IKTS is a Fraunhofer institute; HPE Galway is a site/team, not a verified legal person. |
| A04 | Synthesis capability | User assigned owner and line scale | Savery performs all synthesis and operates one 5 kg line. At M12 qualify dry output, cycle including cleaning, production staffing and availability. Production target 180 kg; six disjoint 30 kg allocations. Plan 36 lots at 5 kg released dry MOF per lot. |
| A05 | IKTS participation | User-confirmed on board | Named personnel, specific equipment and cost rates are still unconfirmed. |
| A06 | UPorto and HPE staff | Role slots costed, names/access pending | No individual commitment, facility booking or free compute is implied. |
| A07 | Primary thermal service | Calculated design point | User instruction 6 November 2026: single Module uses a 10 kW basis because 1 kW mechanical components are unsuitable. One 10 kW two-bed module with 20 kg active MOF; 55/25/70 C service. All full-machine comparisons use this platform, with replaceable independent adsorbent sets. |
| A08 | Working swing and enthalpy | Design assumptions | 0.15 kg/kg, 2.8 MJ/kg-water and a 600 s full bed cycle yield 10.5 kW at 20 kg active MOF and 75% useful-heat fraction; replace with measured values. At swing 0.08 the same hardware/inventory gives 5.6 kW, so achieved capacity remains an experimental result. |
| A09 | Equipment rentals/depreciation | Unquoted planning bases | Savery C2 EUR134k includes rental use EUR123k and assumed sensor depreciation EUR5k and synthesis-line depreciation EUR6k; pressure/flow maps, rental quotes and asset use remain unconfirmed. Other participants verify synthesis/measurement/manufacturing asset books and access. |
| A10 | Financial model | Standard actual-cost RIA planning basis | 100% eligible cost and 25% indirect rate with explicit exclusions; no lump-sum exception found in the read MAT61 topic text; Portal form and grant model must be checked before freezing Part A. |
| A11 | Service/facility purchases | Routine service assumption | Research design and interpretation remain at beneficiaries. If actual contract delegates an action task or uses an overhead-inclusive internal recharge, reclassify and recalculate indirect costs. |
| A12 | Template | User original V5.1 read | RTF V5.1 dated 22 January 2026, original SHA256 retained; authenticated call-session rendering/tags not accessed; do not label Portal-final. |
| A13 | Original source access | Mixed reading levels | HESTIA B1 and ESRs read; GRACE scientific extract and reconstruction read; DOE T04/T07/T10B/R10prime reviews read, T07 full scientific readback available; latest R10prime original not accessible on offline computer. |
| A14 | Publication and IP | No public Git push | Repository visibility is public. Do not push proposal, internal evidence, budget or private source extracts; local branch retains canonical mat-prod path. |
| A15 | Independent replication | Group-level design | Three disjoint powder/assembly groups per physical cell; repeated policies/histories within a group are paired observations, not additional independent material replicates. |
| A16 | Other applications | No additional field or machine mode | Eight adjacent-temperature transfer runs only; no data-centre/urban site, new beneficiary or cooling-mode prototype. |
| A17 | 10 kW budget change | User-steered re-costing | EUR2,487,225 recommended, including powder/large internals, thermal/vapour equipment and laboratory utilities. EUR12,775 remains below the EUR2.50m ceiling. Bulk powder and precursor prices are assumptions, not quotes; the initial EUR100k headroom is no longer available. |


这些事项集中用于L1及后续伙伴资源核实；本轮不发送邮件、不采购、不预约、不承诺经费、不登录Portal。机构性未确认项不会被自动改写为已落实事实。

## 文件与模板边界

用户原RTF实际为V5.1，2026-01-22；不是任务书所述通用V5.0。保留原始字节及SHA-256。适用表3.1a–h已逐字段对照；3.1h仅要求设备成本超过该伙伴人员费15%时说明，Savery为€134,000/€468,000=28.63%。Word正文和表格均≥11 pt，A4、四边16 mm；图注及图中文字单独可读。后续仍需与登录后的本call提交会话表单、标签和最终Part A核对，不能称Portal-final。

Section 3保留完整实施细节，当前版面页数见QA结果；全Part B的40页预算仍由L1统一分配。模板给3.1/3.2的页数仅是建议，不用缩小字体实现压页。来源读取等级与旧稿继承范围见Source_and_Reuse_Log.md。
