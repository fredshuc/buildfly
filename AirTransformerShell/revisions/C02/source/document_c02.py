import bootstrap,json,math
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import Table,TableStyle,Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
R=bootstrap.ROOT;D=R/'deliverables'
pdfmetrics.registerFont(TTFont('CN',r'C:\Windows\Fonts\msyh.ttc'))
W,H=1190.55,841.89
c=canvas.Canvas(str(D/'drawings/AT_SHELL2_2V_C02_Geometry_Review_CN.pdf'),pagesize=(W,H))
c.setTitle('AirTransformer C02｜双芯竖装、+X水路与四三通阀')
style=ParagraphStyle('cn',fontName='CN',fontSize=11,leading=18,textColor=colors.HexColor('#244655'))
def para(text,x,y,w=340,size=11):
 st=ParagraphStyle('p',parent=style,fontSize=size,leading=size*1.6)
 p=Paragraph(text,st);ww,hh=p.wrap(w,1000);p.drawOn(c,x,y-hh);return y-hh
def head(title,p):
 c.setFillColor(colors.HexColor('#123d51'));c.rect(0,H-86,W,86,fill=1,stroke=0)
 c.setFillColor(colors.white);c.setFont('CN',22);c.drawString(34,H-45,title)
 c.setFont('CN',10);c.drawString(35,H-68,'AirTransformer · L2-MI shell2 · AT-SHELL2-2V-C02 · 2026-11-04')
 c.setFillColor(colors.HexColor('#71848c'));c.setFont('CN',9)
 c.drawString(34,22,'几何候选｜单位 mm｜减重暂缓｜当前包不作为制造定尺文件');c.drawRightString(W-34,22,f'{p} / 4')
def pic(name,x,y,w,h):
 im=ImageReader(str(D/'views'/name));iw,ih=im.getSize();k=min(w/iw,h/ih)
 c.drawImage(im,x+(w-iw*k)/2,y+(h-ih*k)/2,width=iw*k,height=ih*k,mask='auto')
def table(data,x,top,widths,size=10):
 st=ParagraphStyle('t',parent=style,fontSize=size,leading=size*1.45)
 vals=[[Paragraph(str(v),st)for v in row]for row in data]
 t=Table(vals,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce9ee')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#bacbd1'))]))
 tw,th=t.wrap(1100,1000);t.drawOn(c,x,top-th);return top-th
head('双芯竖直安装，接管统一弯向 +X',1)
pic('01_cutaway.png',28,90,760,640)
y=H-120
for title,text in [
('布局','两只无手性 HX 竖直安装。B 芯绕 Z 轴旋转 180°，使两床接管端集中到中间区域。'),
('接管','四根上口短接均以 90° 弯头转向 +X。水平轴高为 Z1514 / Z1634，间隔 120。弯曲中心半径暂取 R50。'),
('水路','复用每床两只三通阀的切换拓扑。四只 R3025-BL2 原始阀体已导入，LRQ24A 执行器按尺寸占位。公共 CS、HR、CR、HS 总管为轴线及外径占位。'),
('壳体','主壳体 X=-52…1312，Y=-852…852，Z=0…1752。八个风阀孔及法兰孔阵保留，接管穿板改为 +X 面。'),
('本次范围','完成壳体、接管、阀位、开口和拆卸空间的几何候选。材料厚度沿用 C01；本轮不做减重优化。')]:
 y=para('<b>'+title+'</b>',815,y,335,12);y=para(text,815,y-4,335)-18
c.showPage()
head('旧坐标关系保留，X 向收薄',2)
pic('04_geometry.png',28,286,1130,440)
table([['参照项目','旧四芯壳体读取值','C02 当前几何'],
['X 范围 / 厚度','-650.8…1200 / 1850.8','-52…1312 / 1364；厚度减少 486.8'],
['Y 侧板','约 ±850','±852；两床仍并列'],
['顶部 Z','1527','1752；为竖芯上口、弯接和服务空间加高 225'],
['水路舱分界','X≈750','接管穿板仍为 X750；+X 外盖延至 X1312'],
['风阀孔','P：630×345；R：630×180','4×P + 4×R；P 法兰32孔、R法兰28孔，均Ø9'],
['口面 / 占位','原风阀法兰基准','-X 与 +X 两面分布；风阀本体及外侧驱动仍为占位']],
35,270,[220,380,515],9)
para('主壳体尺寸不包含外侧风阀及驱动占位。图中旧壳体是坐标参照轮廓；新旧整机的管路、附件和支脚范围不能直接视为同一总包络。',40,66,1100,9)
c.showPage()
head('四三通阀与 HX 接口对应',3)
pic('05_water_detail.png',25,225,650,510)
table([['阀位','O=(X,Y,Z)','AB 接 HX','A / B 功能'],
['A-VL','976, -75.325, 760','A.W1','CS / HR'],
['A-VU','1076, -75.325, 1230','A.W2','CR / HS'],
['B-VL','1076, +75.325, 760','B.W2','CS / HR'],
['B-VU','1176, +75.325, 1230','B.W1','CR / HS']],690,710,[75,185,90,100],9)
y=460
for txt in [
'阀体统一采用真实刚体旋转 -90° 绕 Z。厂家 A 口朝 +Y、B 口朝 -Y、AB 朝 -X。每只原厂 STEP 的 4 个源实体均保留。',
'执行器采用 227×85×95 操作包络；另留 +Z235 拔出空间。四阀沿 X 错开 100，避免相邻支口对撞。',
'B 芯旋转后，W1/W2 的空间位置互换。本候选将 B.W2 接 CS/HR、B.W1 接 CR/HS；该水流方向须与 HX 工艺方向一并确认。',
'阀体刻字按 2026-10-18 COR01 接口基准：下阀 A=CS、B=HR；上阀 A=CR、B=HS。']:
 y=para(txt,692,y,450,10)-14
table([['接管与接头','当前几何定义'],
['可拆分界','HX 上口 Z1414；水平拆分面 X700；拆除两根弯接适配段后抽芯'],
['管路 / 保温','路由实体 OD35 / ID29、R50；保温径向25；冷/热工况不以颜色判定'],
['ZR 接头','外伸按 50…66 范围占位；CAD 路由接到66上限参照端。实际旋合量与末端定尺尚未锁定'],
['公共总管','CS Z200、HR Z760、CR Z1180（X1260）；HS Z1680（X1200）。阀口至总管支路未连接']],
35,205,[175,940],9)
c.showPage()
head('检修顺序与当前几何检查',4)
pic('03_service.png',25,180,660,550)
v=json.loads((D/'evidence/VALIDATION.json').read_text());e=json.loads((D/'evidence/EXTENDED_VALIDATION.json').read_text())
checks=[['检查项','本次结果'],['实体 BRep 有效性','全部有效'],['壳体 / 接管实体交集',str(len(v['physical_pairs']))+' 处'],['设备占位与结构 / 设备',str(len(v['equipment_metal'])+len(v['equipment_pairs']))+' 处'],
['HX 静态 / 抽芯扫掠',str(len(v['hx_static'])+len(v['core_removal']))+' 处'],
['执行器 +Z235 拆卸',str(len(v['actuator_withdrawal']))+' 处'],
['保温与结构 / 设备',str(len(v['insulation_shell'])+len(e['insulation_equipment'])+len(e['header_insulation_shell']))+' 处'],
['三份 STEP 独立读回',str(len(e['step_readback']))+' / 3 通过']]
table(checks,715,715,[270,135],10)
y=390
for txt in [
'抽芯：停机、隔离并排液 → 释放 X700 与 HX 上口接头 → 拆除两根弯接段 → 拆前风阀、前风箱及前上盖 → 抬升30 → 沿 -X 移出800。',
'执行器：打开 +X 维修盖，保持对应 +Z235 通道畅通。驱动接线和阀杆联接按后续实件装配细化。',
'交集阈值0.001 mm³。扫掠检查采用 HX 完整包络；并未加载真实翅片、接线或完整风阀传动件。']:
 y=para(txt,715,y,415,10)-12
para('<b>继续深化：</b>公共总管及 FLOW_STOP 支路；Rp1¼ HX 端与 DN25 阀组的变径/活接；接头旋合量；管夹、HX 固定与热位移；风阀完整机构及外侧驱动罩；钣金折弯、接缝、密封和底盘排水。',40,145,1100,11)
para('当前结论：壳体和侧接水路的几何关系已形成可检查 CAD。完整流体连通、制造定尺、结构强度与过程性能不在本轮完成范围。',40,75,1100,10)
c.save()
print('PDF_READY',flush=True)
