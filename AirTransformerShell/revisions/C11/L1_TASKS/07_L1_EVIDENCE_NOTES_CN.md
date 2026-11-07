# C11任务签发｜L1核读依据与数值校正

日期：2026-11-07。用途：内部技术追溯；四份L2任务书本身可独立领取。

## 1. 核读范围

固定证据树`fredshuc/buildfly@16b44e96c4640a4bccb565ae371fee445999634f`，来自红队分支`claude/jolly-hopper-mndk80`。该树已包含C10的`a42fdb8` CAD和`82e51e3`英文README。任务签发没有修改C10 CAD，也未独立重复RT5的全模型重建/碰撞计算。

本次实际核读：RT5全文及CSV、C10英文README、build.py/verify.py、输入表、A柱焊缝表、热模型及屋顶深度/风速JSON；HYD-S2、H01、D03和D04负责人资料；H01端口/变换/条件签认；C05原包中接水盘源码。三专业并行核对后，L1统一分工和验收要求。

## 2. 不能只看红队摘要的事项

| 事项 | 实际依据 | 本轮处理 |
|---|---|---|
| F6遗漏 | RT5正文保留0.603mm根套间隙、80°越程997.55mm³相交，CSV没有独立F6行 | 在任务和关闭矩阵显式保留F6 |
| N2材料假设 | 1.9mm压片挠度采用50kPa胶套反力假设，尚无实际材料/压缩曲线 | 保留刚度风险，要求实际密封反力和压片设计，不把1.9mm写成实测 |
| N4口的混淆 | H01新水排口X=-698已在湿侧；旧header closure位于X603…618；C05嘴为气侧凝结水嘴 | 28组功能端逐类处理，不统一“封堵或开盖” |
| N4间距泛化 | RT5的4个C05嘴`nearest_host_mm`为`>80`；17–20mm主要指vent和旧header drain/closure | 不把17–20mm归到每一个排水嘴 |
| 旧签认 | H01 `conditions[3]`仍记录4处FS/Q交叉；其README仍保留原1.65mm冠部空间 | 用HYD-S2及C10实际证据刷新；保留真正尚未完成的条件 |
| D04局部净距 | 19.893mm仅是新增膜/保持件至运动包络 | 不用于关闭旧上叶至H01的1.2119mm问题 |
| A柱22% | 指削切后的单柱弱轴惯性矩 | 组合加强结构必须按web/焊缝传力计算，不直接套22%到全框 |

## 3. 气流JSON校核

`c10_header_model.json`在说明中明确使用RT3占位值60Pa/芯@2.21m/s，未取得C05涂层气侧曲线；模型未包含入口射流、风阀尾流、40mm导轨遮挡和两层间横向混合。

从其`cores_in_series=2`输出取极值：

| 模式/风量 | CV范围 |
|---|---:|
| P，4,870m³/h | 20.04–30.22% |
| R，2,435m³/h | 17.22–28.28% |
| P，2,435m³/h | 14.13–21.95% |

`c10_apex_sweep.json`中8→120mm的结果：

| 模式 | k_div | CV起点→终点 | 变化，百分点 |
|---|---:|---:|---:|
| P，4,870m³/h | 0.6 | 18.01→20.59% | +2.58 |
| P，4,870m³/h | 1.0 | 23.62→28.34% | +4.72 |
| R，2,435m³/h | 0.6 | 16.36→17.23% | +0.87 |
| R，2,435m³/h | 1.0 | 21.08→21.95% | +0.87 |

因此RT5“均少于3个百分点”不准确。各结果仍不支持靠进一步抬顶解决整体分配。本轮选择保留屋顶、可拆布风预留和无板/有板测量配置；没有把模型CV当实测，也未冻结穿孔板压降。

## 4. 热桥JSON校核

RT5 `condensation.json`明确：空气温度/露点为illustrative，尚非项目设计环境。模型按D35管、5°C水和一维等厚圆筒：

`R_cond = ln(r_o/r_i)/(2πkL)`，`R_conv = 1/(2πr_o hL)`，

`T_surface = T_air − (T_air−T_water) / [1 + h·r_o·ln(r_o/r_i)/k]`。

该式忽略内部换热热阻和局部三维桥接；用于本轮风险筛查。对32°C空气/26°C露点/5°C水，k=0.034–0.040W/(m·K)、h=5–8W/(m²·K)：

| 等效厚度 | 表温范围 | 对26°C露点的最差裕量 |
|---|---:|---:|
| 5mm | 16.18–20.41°C | -9.82K |
| 19.143mm | 25.84–28.34°C | -0.16K |
| 25mm | 27.27–29.27°C | +1.27K |

“5mm约20.4°C”与“19.1mm裕量2.3K”仅为其中较有利组合，不代表全范围。局部倒角不等于整圈19.143mm圆筒。隔汽、表面温度和滴水路径是三个不同设计问题；一层vapour-tight胶套不能自动提高薄层外表温度。

本轮将32/26/5作为局部暂定挑战点，要求在工况表中标明新指定的性质、实际项目额定边界的来源及所需裕量。

## 5. C05盘嘴功能与H01旋转的独立核对

C05包`M101_C05_RT2_CAD.zip`为2,197,105字节；本地包计算Git blob SHA-1：`0d0d7b2c1789296b0e820e48b911566af169fd27`，与指定远端证据树目录记录一致。

包内`source/build_c05.py::make_tray()`：

- 接水面162×612mm；local Z24–32，沿+Y落差8mm。
- 生成`C05_CORE_CARRIED_TRAY`和`C05_SHORT_DRAIN_SPIGOT`。
- `report['drain']['fixed_drain_system_status']`明确将软管、穿底板和外部trap列为Shell未完事项。

H01四芯共同旋转矩阵：

| 全局坐标 | 对应局部坐标 |
|---|---|
| X | tx−z |
| Y | ty−y |
| Z | tz−x |

原盘面法向接近local Z，旋转后接近global X；原朝local−Z的嘴朝global+X。RT5所报嘴包围盒X619…635，下层Z719…741、上层Z1054…1076与此一致。

**事实**：C05嘴为气侧接水盘接口，且随H01改变方向。**工程推论**：旧竖装盘不能自动证明横装重力接水成立。**仍需核对**：全机是否已有另一个有效收集件及其连续外排路径。本轮新增L1-N7要求HX/Shell确认并补齐，未把该推论写成已重建证实的整机缺陷。

## 6. 任务的接受标准与实体试验

本包签发的是局部设计工作，当前未产生C11实物。几何、公差、计算、制造图和可执行试验方案可以在本轮完成；实际检漏、压痕、冷浸、充排水、残液和面风速记录在样件/台架可用后完成。

L1后续可按分项详图和计算授权测试件制造，并在独立支承、压力连接、排气排水及保护条件具备后授权受控首次试水。首次试水数据用于后续稳定运行裁定，避免“必须先做充排水试验才能允许任何充水”的循环条件。

## 7. 固定版本的关键来源

- [RT5全文](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/RT5_REVIEW/C10_RT5_REVIEW.md)
- [RT5发现CSV](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/RT5_REVIEW/C10_RT5_FINDINGS.csv)
- [C10 build.py](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/source/build.py) / [verify.py](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/source/verify.py)
- [气流结果与模型假设](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/RT5_REVIEW/results/c10_header_model.json)
- [屋顶扫描JSON](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/RT5_REVIEW/results/c10_apex_sweep.json)
- [热计算JSON](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/RT5_REVIEW/results/condensation.json)
- [服务端口原始测量](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/AirTransformerShell/revisions/C10/RT5_REVIEW/results/vent_drain_S1.json)
- [C05原包](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/HX/M101_D952_P254_220_39x6_C05/M101_C05_RT2_CAD.zip)
- [C05排水接口说明](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/HX/M101_D952_P254_220_39x6_C05/RT2_RESPONSE_EN.md)
- [H01位姿](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/HX/M101_C08_HORIZONTAL_H01/PLACEMENTS.json) / [八口表](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/HX/M101_C08_HORIZONTAL_H01/EIGHT_PORTS_AND_SPOOLS.csv) / [签认](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/HX/M101_C08_HORIZONTAL_H01/HX_SIGNOFF.json)
- [HYD-S2](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/hydronics/H01_HYD_S2/README_CN.md)
- [D03](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/dampers/c08-d03/README_CN.md) / [D04](https://github.com/fredshuc/buildfly/blob/16b44e96c4640a4bccb565ae371fee445999634f/dampers/c09r1-d04/README_CN.md)
