# AirTransformerShell

AirTransformer 双芯竖装壳体，负责人：L2-MI shell2。

本目录是 shell2 后续设计文件的 Git 存储位置。保留各版源代码、接口表、验证结果、审查图和完整工程包。

## 当前文件
- [C02 四页几何审查图](revisions/C02/deliverables/drawings/AT_SHELL2_2V_C02_Geometry_Review_CN.pdf)
- [C02 完整 CAD 工程包](revisions/C02/packages/AT_SHELL2_2V_C02_CAD_20261104.zip)：三份 STEP、具名 BRep、输入源件、脚本与全部交付资料。
- [C02 说明](revisions/C02/deliverables/README_CN.md)
- [可编辑建模源代码](revisions/C02/source/)
- [接口与布置表](revisions/C02/deliverables/tables/)
- [几何检查证据](revisions/C02/deliverables/evidence/)
- [下一版 HX 接口调整](NEXT_HX_INTERFACE_CN.md)

C02 为2026-11-04的几何候选：两芯、+X侧水路、四只三通阀、八个风阀口。
主壳体1364×1704×1752 mm。当前已通过的检查及范围见C02说明和证据文件。

**版本状态：** C02仍包含120 mm接管高度错层、B芯180°安装及相应W1/W2互换。
2026-11-05已提出两水口沿Y分开、同高度朝+X、两芯同向的下一版方向。
这项接口调整尚未在本目录的C02 CAD中实施；等待L2-B HX新版接口，再更新壳体。

## 后续提交
新设计版本放入 revisions/<版本>/，保留已交付版本。源代码、接口表和审查文档按文件跟踪；
完整STEP、BRep及重建输入暂随具名工程ZIP保存，SHA256见对应版本记录。
重建C02时先解压完整工程包；本目录的展开文件用于浏览和版本比较。
质量与验证状态写入每版README；仅在实际提交成功后记录commit SHA。
