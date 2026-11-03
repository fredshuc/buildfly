# A16-R5-S123 内部变更、来源与整合记录

2026-11-03。依据正式 `EIC26-C05-A16-R4-S123_L1_REVIEW_AND_R5_ORDER_CN.md` 执行定点修订。R4 的正式状态为 **ACCEPT_WITH_OPEN_ITEMS / CLOSED，仅独立 S123 文本工作基线**；R5 为本次本地完成的候选，仍由 L1 作内容裁定。保持11月4日提交目标、C05、blended finance及€2m EIC investment。

交付三份完整英文MD、本中文记录和三份配图文件。按用户已明确指示，由用户手动回传；没有向L1发送、操作Portal、签署、外联、恢复已删除的自动任务或领取合版任务。

## 1. 本轮优先指示与当前事实

| 当前输入 | R5处理 |
|---|---|
| Frédéric Cui、Qin Yu、Ina Wang当前均全职 | S3采用当前事实，三人公司commitment均100%；项目投入仍12／21／12 PM，共45 PM。其余十一拟招聘角色仍213 PM，总258 PM，不把拟招聘写为当前雇员。 |
| 其他当前团队成员没有期权 | 撤下旧激励池假设及其治理分母。CURMA持有已发行股份及表决权100%；创始人例外指现有持股，不新增founder option grant。BSA-AIR仍按条款在下一轮转换，不能由无期权推导最终fully diluted 100%。 |
| 当前现金€300,000、无未偿债务／短期负债、BSA未转换 | 直接写当前事实，删除启动前再审流动性的正文句；不编造BSA金额、人数、转换比例或已到账融资。 |
| 已接受G3.1中央情景的Seed→A保护缺口已闭合 | 删除两轮间隔五个月的评论。正文说明Seed和A的用途、阶段及里程碑，不从日历间隔推断缺口。 |
| 用户在本轮执行令之后明确允许保留原拼图，并已替换同路径SEM | 此直接指示优先于正式令中“旧拼贴不继续嵌入”的要求。Figure1用新功能图；Figure2保留用户更新后的拼图。不是漏执行换图，也未擅自改动用户图片。 |

红队v4及内部register v3作为建议输入，采用指标表、市场风险和数字显示意见；不把其未证实的造假／燃烧推断、旧团队比例、旧激励池及旧缺口状态作为当前事实。register v3文件仍带旧v2标题，其版本名不具有覆盖最新申请人和L1指示的效力。

## 2. 三处精确替换与关联清理

以下 old 仅用于变更追溯，不是当前安排。

### 2.1 当前全职投入

Old（R4历史）：

> Commitment is planned full-time company commitment during the action, including wider company responsibilities. It is a prospective work allocation, separate from current contract or payroll status and from historical recorded hours. EIC project effort is specified in the implementation resource plan below.

New（R5）：

> Frédéric Cui, Qin Yu and Ina Wang work full-time for Savery. The commitment column records their company commitment; their EIC action allocations are set out in Section 3.3.

### 2.2 当前流动性事实

Old（R4历史）：

> At application preparation, Savery has reported €300,000 cash across its accounts, no outstanding debt and no short-term liabilities. BSA-AIR instruments remain unconverted. Management will review mobilisation liquidity against intervening operating expenditure, collections and financing before the action starts.

New（R5）：

> Savery has €300,000 in cash, no outstanding debt and no short-term liabilities. Existing BSA-AIR financing remains unconverted.

### 2.3 Seed与A的用途及里程碑

Old（R4历史）：

> The April 2028 Series A target follows the planned November 2027 Seed close by five months, so pilot-factory diligence and preparation overlap the Seed deployment phase.

New（R5）：

> Seed financing supports productisation and initial deployment capacity. Series A finances pilot-factory capacity and commercial expansion. Each round is linked to the corresponding qualification and scale-up milestones.

### 2.4 关联治理及融资文字

治理部分已联动撤下旧“10% reserved option pool”、CURMA 90%／pool 10%分配、pool-inclusive标题及其分母解释；本记录不再将这些列作有效安排。S3当前表题为 **Current issued shareholding**，仅CURMA 100%及TOTAL 100%。BSA转换权保留在正文，不填零，不将当前已发行口径冒称最终fully diluted结构。

资金安排集中为April2027动员、September2027 Seed启动、November2027目标交割；€8m含€2m EIC、grant及EIC investment各按其支付／交割程序。融资延迟应对仅在原风险行保留一次。S1/S2删除相应重复现金评论，保留June2027初始测试准备能力及实际参考交付与资格顺序。

其余修改：S2收入以€m两位显示，三个ROI情景用整数区间；§2.4指标表区分资格目标和208–283kW工程比较；S3新增采购／参考验收延迟与客户选择替代方案两项风险；标准句改为整机协议与适用子系统方法。核心技术、IP、CETP分工及试验计划保持。

完整26处候选old/new和位置记录见 `work/A16/R5/CANDIDATE_PATCHES.json`，三份逐行差异亦在该目录。`EXACT_PATCHES=[]`仅表示接受归档文件未修改，不表示候选没有改动。

## 3. G3.1现金记录与日历版本

本轮直接读取本地正式G3.1 DOCX的融资表及现金保护表，并直接提取10月21日经营复核PDF物理第3页。核得：

| 阶段 | 最低银行现金 | 月份 | 三个月现金保护缺口 |
|---|---:|---|---:|
| Seed to A | €3.23m | March2028 | €0.00m |

经营复核明确中央预测覆盖Seed之后的三个月经营现金底线。10月20日L1 closure接受G3.1作为资金条款审阅基线的事实，沿本次正式令对该原件的实际核读继承；L2本轮未另取得closure原件，不称独立重读。

G3.1融资表仍为March2027 Seed，现行EIC正文采用较新的September启动／November交割计划。€3.23m是原G3.1日历中的既有结果，不放进正文冒称November日历重算值。旧Seed→A中央缺口诊断不再有效；日历差异只记录为后续来源同步项，不再生成缺口判断或本轮重算任务。

G3.1及经营复核的融资表保留历史USD标签；现行S123沿申请人已批准的名义EUR融资指示。未换汇，也没有重算月度现金、利息、债务、股权或估值。旧期初现金与历史保护项不代替当前€300k现金事实。

| 实际来源 | 本轮读法与身份 |
|---|---|
| `work/A01/R1/intake/package/sources/03_Savery_Growth_Business_Plan_EN_G3_1.docx` | 48160B；SHA256 `1f2d2ed2e1c52c5699ab26c0653537c806ab630874eb2bc3696de143c21a6a34`。直接读第2、第12张表（零基索引1、11）；物理p1/p6定位来自L1正式令，本轮未重渲染整份BP。 |
| `C:/Users/Gebruiker/Downloads/03_Savery_Development_Plan_Review_EN_2026-10-21.pdf` | 161868B；SHA256 `3533639bab58fc224e51a15a3c820bdb07d6a8d3b7a97052fe54f5a02930ae74`。直接读取物理p3文本。 |
| 本次L1裁定及R5令 | 18645B；SHA256 `68590ece6ef466a5767eee985ab7f6c2b6a6aa76e7a3a5a050fd3859b6fe2e17`。根目录与L1_issuance副本同字节；包含closure读取结论及新旧日历区别。 |

逐字段原文读回保存在 `work/A16/R5/BP_CASH_SOURCE_READBACK.json`。

## 4. 配图与实际视觉检查

**Figure1**为基于本次已接受S1架构绘制的原生SVG。文字、方框、连线和箭头均为矢量对象，无嵌入栅格照片，无第三方logo，无新增硬件几何、Roots部件、材料曲线或机器照片。另导出3600×2760 PNG用于MD可见显示；SVG保留可编辑源。

图中主空气依次通过分级MOF接触器和IEC后交付；接触器交替处理／再生。吸附热接入兼容热汇，再生有余热输入和回路返回。IEC工作空气、蒸发补水、湿排气与交付空气分开。液水回收模式另示冷凝／热汇、处理、隔离储存和合格非雾化设备清洁用途，并保留库存、损失、排弃、内耗、净输出分别记账。图不推导固定产水量、不混入供热压缩机，也不宣称某现场用途已获批准。

图内保留50–70°C含液水回收、40–50°C无液水回收、风机／泵／控制／必要辅助电输入，以及20kW thermal模块与600kW thermal集装箱配置；没有把配置容量赋给G3.1 forecast unit。

**Figure2**直接复制用户更新SEM后的 `deliverables/A16-R4-S123/assets/legacy_p14_image01.jpeg`：1297×704、363100B，SHA256 `57632fb40565dd0f45bc6ebe65b54c17a3d1538dcc2a4f0b83a3ef05a386c6bc`。未改像素、数据栏、标签或图内任何对象。S1图注明确其为Savery提供的工程概览，含示意集成图，旧吸附曲线不是当前CAU批次测试结果；保留图内历史logo不构成新增合作承诺。未凭图标或微观标签判定造假／燃烧，也未对SEM进行独立材料身份认证。

R4接受归档中的历史图仍为208945B、SHA256 `a265f249ad61d3da1f91e83475712a148295409902eeaa7e52ecc13bb6762acb`，本轮未覆盖。用户新图单列为新输入，因此不把其与旧冻结图不同误报为文件损坏。

最终功能图PNG与用户拼图均已实际查看。功能图核文字可读、箭头方向、分离路径、回路与边界，无裁切或文字遮挡；MD两条相对图片路径均有效。Markdown交付未生成DOCX/PDF，不声称完成合版分页或20页审查。

## 5. 数字显示与保留的计算值

本轮仅核显示映射，沿用R4已独立复算的12个COP×水端点，不重跑财务模型。客户共同条件：H=8000有效替代压缩制冷小时／年，Q=100kW归一冷量，EER3，COP8或20，水基准1.5L/kWh冷量，节水40%或60%，水价€4/m³，余热边际采购成本0，增量服务€2000/年。年水价值€1920–€2880。8,000不是设施uptime；自然冷却和实际职责会改变被替代压缩小时及回报，该条件在正文集中保留一次。

年净现金节省 = H×Q×(1/3−1/COP)×电价 + 年节水价值 − 2000；年简单税前现金ROI = 节省／安装资本；回收月数 = 12／ROI。资本、税费、退化及大修排除边界沿R4。

| 安装资本／电价 | 年净节省EUR（六位显示） | 回收月数（六位显示） | 年简单现金ROI（六位显示） |
|---|---:|---:|---:|
| €120000 / €0.25 | 41586.666667–57546.666667 | 25.023170–34.626483 | 34.655556–47.955556% |
| €120000 / €0.20 | 33253.333333–46213.333333 | 31.159838–43.303929 | 27.711111–38.511111% |
| €100000 / €0.20 | 33253.333333–46213.333333 | 25.966532–36.086608 | 33.253333–46.213333% |

正文分别显示约€42–58k／25–35月／35–48%，约€33–46k／31–43月／28–39%，以及约€33–46k／26–36月／33–46%。每个端点的原保存精度、输入和市场比值记录原样保留在 `work/A16/R5/INHERITED_CALCULATIONS.json`，不是用显示整数反算底层结果。

€100k仅为100kW归一情景中€900/kW硬件+€100/kW安装工程的未来成本；现有G3.1商业单位仍为€110k设备+€8k安装+€2k工程，不推定每台100kW。未引入公司ROIC或股东IRR。

| 年份 | 公司计划接受数 | 收入原值，€m | 正文显示，€m |
|---|---:|---:|---:|
| 2027 | 4 | 0.480000 | 0.48 |
| 2028 | 13 | 1.562310 | 1.56 |
| 2029 | 71 | 8.535279 | 8.54 |
| 2030 | 222 | 26.7181011 | 26.72 |
| 2031 | 624 | 75.24415599 | 75.24 |
| 2032 | 1498 | 180.890300391 | 180.89 |

934=4+13+71+222+624，仅2027–2031公司累计预测接受量，未新增到正文，更未用作M24／C05行动交付或气候目标。2031/2032相对于€15bn公司规划参照的约0.5%／1.2%保持；USD20.5bn全球行业参照不换汇或改成区域SAM。

§2.4保留既有60–70%节电资格目标（≥60%下界）、40–60%外部补水下降目标及职责连续性；208–283kW/MW仍是COP8–20对EER3的工程比较，不冒称M24现场实测目标。三个电网比较行及其计算值不变。

## 6. 冻结的预算、实施与证据边界

关键预算表和金额保持：eligible €3,550,833.33；grant €2,485,583.33；non-grant eligible €1,065,250.00；EIC investment €2m包含在Seed €8m内，其他Seed €6m，总EIC €4,485,583.33。Action cash €3,908,916.67，beyond grant €1,423,333.33；purchases €529000／depreciation €170916.67。WP6 €2,112,500 = EIC €1.9m + 其他Seed €212500，另€100000 EIC用于行动共同融资。未为显示凑平修改未舍入源值或正式费用。

人员、五grantWP、证据门和CETP/EIC分工表不变：258PM=45核心+213拟招聘；平均10.75FTE、峰12.375FTE；18PM热验证+18PM监督控制=36PM，18PM嵌入式另计。公司三核心全职不等于其所有工时都计入EIC。

保留六批／十二接触器／十八见证、4000h内部耐久／1200h独立fixture，M10工业单元、M10–M14五个十二天气候／负荷campaign。Qin及field lead在M12前落实增量EIC场地范围、接口、责任与窗口，M16安装，M17–M23共1600h运行，M24分析／复测／资格决定。CETP为2026–2029已获资助项目、HPE场地、TRL7；研究与EIC产品实施、工时／资产／发票只计一次的边界不变。

S1有限时间技术论述326词、整周期恢复边界、局部线性适用域及单段工业控制／RL保留。两新申请族、IP/FTO处理、当前产品规格、测试定义及用途保持；不提前执行约1000词削减清单。

S3标准句按令精炼，仍是整机协议加适用子系统方法；ASHRAE143排除干燥一次／二次空气装置、EN13141-7住宅通风范围和ISO/IEC17025实验室能力边界沿R4已核来源，未变成通用整机认证或认证仪器。其余法规、市场、专利来源沿已接受文本和既有读取链，不虚报本轮重新开展法律、FTO或市场研究。

## 7. 阅读与核验记录

| 输入 | 实际处理 |
|---|---|
| 本轮正式L1裁定及R5执行令 | 全文读取；根目录和签发目录副本一致。 |
| R4四份接受MD与接受归档图 | 文本及本轮受影响上下文读取；其余技术、表格、窗口和引用以精确比较保持；前后哈希核验。 |
| red-team v4、register v3 | 本轮读取；仅采用符合最新正式令和直接用户指示的部分。 |
| 用户同路径更新图 | 实际打开查看，原字节复制到R5；与历史接受图分列身份。 |
| G3.1 DOCX／经营复核PDF | 有界直接读取融资及现金表／物理p3，原文读回已保存。 |
| 10月20日closure | 沿L1正式令已核结论，本轮未重读原件。 |
| R4已核计算与budget.json | 只读身份及显示／冻结比较；没有重跑BP或预算。 |
| 既有模板、CV、法规、专利和市场来源 | 沿已接受R4与其阅读记录继承；本轮未新增广泛检索，也未登录Portal。 |

本地验证记录在 `work/A16/R5/CHECKS.json` 和 `OUTPUT_MANIFEST.json`：三份全文、表列数、引用、图路径、26处变更反向恢复、治理清理、当前全职与项目PM、ROI显示、收入序列、指标／风险表及全部本轮输入身份。两个最终配图的实际查看记录在 `VISUAL_QA.json`。检查结果不替代L1接受。

## 8. 后续整合事项（非本轮扩大任务）

1. 合版时补题目选择后的C05 fit、最多半页摘要和实际在线CV链接，按真实页数再决定压缩。三人CV摘要仍保留，不编造链接。
2. 本次未新取得2025 EN原报告，不造题名、实验室、日期或报告号，不加占位符；S1已自足给出批准结果和测试边界。R4原文没有“test report in Annex”，不能将其列为现存错误；不假定Portal有通用报告上传栏，也不把“未列通用附件项”夸大成所有额外报告均被明文禁止。
3. 最终资本表依据真实BSA条款及下一轮转换口径形成fully diluted分母；当前表是已发行100%口径，其他团队成员无期权。旧BP长期激励情景不自动成为今日授予。需要同步的BP日历以最新真实来源为准，不再复活已闭合的旧Seed→A诊断。
4. 按既有计划完成场地增量范围、版本／地域权利审查、成本一次归属及真实附件清点。未获授权在本轮代签LOI、拍摄视频、联系供应方或提交申请。

本轮仅完成独立S123候选。接受归档、BP、正式FP/DB和其他产品未修改；自动任务保持删除，最后真实自动回传时间仍属A14历史，不能拿来证明R5已发送。
