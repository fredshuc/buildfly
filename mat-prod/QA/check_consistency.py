#!/usr/bin/env python3
"""Independent checks of design arithmetic, scope, dates, identifiers and exports."""
import json,csv,pathlib,hashlib,re,math,zipfile,datetime,sys
from collections import Counter
from xml.etree import ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1]
m=json.loads((R/'03_budget/implementation_model.json').read_text());snap=json.loads((R/'03_budget/calculated_snapshot.json').read_text())
checks=[]
def chk(name,ok,detail):checks.append(dict(check=name,passed=bool(ok),detail=detail))
def near(a,b):return abs(a-b)<1e-7
P=['SAV','IRC','IKTS','UP','HPE'];W={w['id']:w for w in m['wps']};T={t['id']:t for t in m['tasks']}
chk('Exactly the authorised five participants',[p['id'] for p in m['partners']]==P,str([p['id'] for p in m['partners']]))
for group,key in [('wps','id'),('tasks','id'),('costs','id'),('deliverables','id'),('milestones','id'),('risks','id'),('interfaces','id')]:
 ids=[x[key] for x in m[group]];chk('Unique '+group,len(ids)==len(set(ids)),len(ids))
chk('Seven WPs and 22 tasks',len(W)==7 and len(T)==22,{'wps':len(W),'tasks':len(T)})
for t in m['tasks']:
 chk(t['id']+' dates and responsibility',t['lead'] in P and t['wp'] in W and W[t['wp']]['start']<=t['start']<=t['end']<=W[t['wp']]['end']<=36,t['name'])
 chk(t['id']+' allocation and acceptance',set(t['pm'])==set(P) and all(x>=0 for x in t['pm'].values()) and bool(t['inputs'] and t['work'] and t['acceptance']),sum(t['pm'].values()))
pm={p:sum(t['pm'][p] for t in m['tasks']) for p in P};rates={p['id']:p['pm_rate'] for p in m['partners']}
chk('PM closure',near(sum(pm.values()),224),pm)
for p in m['partners']:
 chk(p['id']+' role PM closure',near(sum(r[1] for r in p['roles']),pm[p['id']]),sum(r[1] for r in p['roles']))
monthly={p:[sum(t['pm'][p]/(t['end']-t['start']+1) for t in m['tasks'] if t['start']<=mo<=t['end']) for mo in range(1,37)] for p in P}
for p in m['partners']:
 chk(p['id']+' monthly PM integral',near(sum(monthly[p['id']]),pm[p['id']]),sum(monthly[p['id']]))
 for role,rpm,cap,people in p['roles']:
  peak=max(monthly[p['id']])*rpm/pm[p['id']];chk(p['id']+' '+role+' peak',peak<=cap+1e-9 and cap<=people,{'peak':peak,'capacity':cap,'people':people})
personnel=sum(pm[p]*rates[p] for p in P)
costs={c['id']:c['qty']*c['unit_cost']*c['use_share']*c['eligible_fraction']*c['project_months']/c['life_months'] for c in m['costs']}
direct=personnel+sum(costs.values());ibase=personnel+sum(costs[c['id']]*c['indirect_eligible'] for c in m['costs']);total=direct+m['indirect_rate']*ibase
chk('Personnel cost',near(personnel,1458000),personnel);chk('Direct and indirect closure',near(direct,1989780) and near(total,2487225),{'direct':direct,'indirect':.25*ibase,'total':total})
chk('Ceiling and no reserve cost',total<=m['ceiling_eur'] and all(not re.search(r'contingency|reserve',c['description'],re.I) for c in m['costs']),m['ceiling_eur']-total)
chk('All cost lines have task/WP ownership',all(c['partner'] in P and c['wp'] in W and c['qty']>0 and c['unit_cost']>=0 and c['life_months']>0 for c in m['costs']),len(costs))
chk('Snapshot independently reconciles',near(snap['total_budget'],total) and near(snap['total_pm'],224) and near(sum(w['total'] for w in snap['wps']),total),snap['total_budget'])
esbase=sum(costs[c['id']] for c in m['costs'] if c['category']=='C2' or '-X' in c['id'])
stress=total+1.25*(.05*personnel+.1*esbase)
chk('Sensitivity arithmetic',near(esbase,274000) and near(stress,2612600),{'equipment_facility_compute':esbase,'combined_stress':stress})
for ds in ['deliverables','milestones']:
 for d in m[ds]:
  involved=[d['wp']] if 'wp' in d else (list(W) if d['wps']=='WP1-WP6' else d['wps'].split(','))
  chk(d['id']+' date inside action',1<=d['month']<=36 and all(w in W for w in involved),d['month'])
dm=[d for d in m['deliverables'] if d['type']=='DMP'];pec=[d for d in m['deliverables'] if d['id']=='D7.1']
chk('Separate early DMP and communication plan',len(dm)==1 and len(pec)==1 and dm[0]['month']<=6 and pec[0]['month']<=6 and dm[0]['id']!=pec[0]['id'],{'DMP':dm[0]['month'],'PEC':pec[0]['month']})
chk('Early parallelism',T['T6.1']['start']==1 and T['T4.1']['start']==1 and T['T5.1']['start']==3 and T['T3.1']['start']==2,True)
chk('At least nine months integrated validation',36-25+1>=9 and T['T6.3']['start']<=25 and T['T6.3']['end']>=34,12)
cp={x[0]:(x[2],x[3]) for x in m['cpm']};finish={};pending=set(cp)
while pending:
 ready=[i for i in pending if all(p in finish for p in cp[i][1])]
 if not ready:break
 for i in ready:finish[i]=max([finish[p] for p in cp[i][1]]+[0])+cp[i][0];pending.remove(i)
chk('Acyclic 36-month critical schedule',not pending and max(finish.values())==36 and finish['F']==24 and finish['J']==24,finish)
nom=[c for c in m['conditions'] if c[1]=='FINAL' and c[2:6]==[55,25,70,10.0]]
chk('Final matrix includes a nominal 10 kW condition',len(nom)==1,nom)
svc=m['service'];mass=svc['beds']*svc['dry_mof_kg_per_bed'];power=mass*svc['working_swing_kgkg']*svc['adsorption_enthalpy_jkg']*svc['useful_heat_fraction']/svc['full_bed_cycle_s']/1000
flow=svc['nominal_kw']*1000/(svc['cp_water_jkgK']*(svc['hot_supply_c']-svc['hot_return_c']))*3.6
chk('User 10 kW module basis',svc['nominal_kw']==10 and mass==20 and svc['full_bed_cycle_s']==600,{'nominal_kW':10,'dry_mass_kg':mass,'cycle_s':svc['full_bed_cycle_s']})
chk('Independent sizing and dimensions',near(power,10.5) and 1.72<flow<1.73,{'estimated_kW':power,'water_flow_m3h':flow})
# NIST Antoine coefficients valid 304-333 K, P in bar; low-density ideal water vapour is a design approximation.
tv=323.15;pv=10**(5.20389-1733.926/(tv-39.485))*1e5;mdot=mass*svc['working_swing_kgkg']/svc['full_bed_cycle_s'];vflow=mdot*461.5*tv/pv*3600
chk('Vapour flow design range',200<vflow<300,{'T_K':tv,'p_abs_Pa':pv,'water_kg_s':mdot,'m3_h':vflow,'source':'NIST Chemistry WebBook coefficients plus ideal-gas approximation'})
chk('All proposed condition duties use 10 kW basis',all(5<=c[5]<=10 for c in m['conditions']),{c[0]:c[5] for c in m['conditions']})
work={w['id']:w for w in m['workloads']};rig=sum(work[f'W{i:02d}']['count']*work[f'W{i:02d}']['hours_per_unit'] for i in range(15,22))
syn=sum(work[f'W{i:02d}']['count'] for i in range(1,6));powder=sum(work[f'W{i:02d}']['count']*work[f'W{i:02d}']['amount_per_unit'] for i in range(1,6))
chk('93 syntheses and 186.12 kg new powder',syn==93 and near(powder,186.12),{'syntheses':syn,'kg':powder})
rec=svc['production_recovery']*svc['new_final_powder_kg'];charge=work['W08']['count']*work['W08']['amount_per_unit'];chk('Final powder and shaped charge balance',near(rec,153) and charge==240 and near(120+9+24,rec),{'new_recovered':rec,'all_final_active':charge})
chk('Reference development and final feed fits',200-24-120/.85>=0 and 60-4-40/.85>=0,{'total_raw_spare':200-24-120/.85,'batch_A_raw_spare':60-4-40/.85})
capacity=m['production_capacity']['trains']*m['production_capacity']['hours_per_train_month']*m['production_capacity']['months'];required=work['W05']['count']*work['W05']['hours_per_unit']
chk('Production finishes before M24 forming',m['production_capacity']['powder_finish_month']==23 and capacity>=required,{'capacity':capacity,'required':required,'margin':capacity-required})
chk('All synthesis owned by Savery',all(work[f'W{i:02d}']['owner']=='SAV' for i in range(1,6)) and T['T2.3']['lead']=='SAV',5)
chk('One 5 kg line and disjoint allocations',m['production_capacity']['trains']==1 and work['W05']['amount_per_unit']==5 and work['W05']['count']==36 and required==1152 and capacity==1980 and 6*6*5==svc['new_final_powder_kg'],{'groups':6,'lots_per_group':6})
chk('Synthesis costing and task transfer',pm['SAV']==78 and pm['IRC']==36 and all(c['partner']=='SAV' for c in m['costs'] if c['id'] in {'S-M1','S-M2','S-M3','S-ME1'}),pm)
chk('Full-history rig hours',rig==2104 and work['W19']['count']*work['W19']['hours_per_unit']==1152,{'all_rig_hours':rig,'primary':1152})
matrixpath=R/'03_budget/CSV/Validation_Matrix.csv'
with matrixpath.open(encoding='utf-8-sig') as f:matrix=list(csv.DictReader(f))
chk('Complete planned validation matrix',len(matrix)==144 and len({r['planned_run_id'] for r in matrix})==144 and all(float(r['total_hours'])==8 and float(r['module_nominal_kW'])==10 for r in matrix),len(matrix))
chk('Replication is at independent group level',set(Counter((r['material'],r['route'],r['group']) for r in matrix).values())=={12},'12 paired histories per set, 3 independent sets per physical cell')
for risk in m['risks']:chk(risk['id']+' trigger impact and consequences',all(risk[k] for k in ['trigger','impact','mitigation','consequence','likelihood','severity']),True)
template=R/'00_call/templates/Tpl_Application Form (Part B) (HE RIA and IA).rtf';h=hashlib.sha256(template.read_bytes()).hexdigest();chk('Original template preserved',h=='507cc6ad2831936b3b41e2bed6ec784cb1c50ba61b1e8dd80590639565575977',h)
md=(R/'01_proposal/Section3_Implementation_EN.md').read_text();chk('All official table identifiers',all('Table 3.1'+c in md for c in 'abcdefgh'),True)
chk('No obsolete small-module duty in final narrative',not re.search(r'(?<![\d.])(?:0\.5|0\.25|0\.525|1)\s*kW\b',md),True)
chk('Narrative current budget',all(x in md for x in ['2,487,225','972,225','337,500','517,500','345,000','315,000','186.12 kg','93 syntheses']),True)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(R/'01_proposal/Section3_Implementation_EN.docx') as z:
 doc=ET.fromstring(z.read('word/document.xml'));styles=ET.fromstring(z.read('word/styles.xml'))
 text=' '.join(e.text or '' for e in doc.findall('.//w:t',ns));chk('Word contains complete task and budget content',all(t in text for t in T) and '2,487,225' in text and '10 kW' in text,True)
 table_fonts=[int(x.attrib['{'+ns['w']+'}val']) for x in doc.findall('.//w:tbl//w:sz',ns)];chk('Table text at least 11 pt',table_fonts and min(table_fonts)>=22,min(table_fonts)/2)
 margins=doc.findall('.//w:sectPr/w:pgMar',ns);chk('A4 section margins at least 15 mm',all(int(e.attrib['{'+ns['w']+'}'+k])>=850 for e in margins for k in ['top','bottom','left','right']),len(margins))
 chk('No title paragraph border or hidden revisions',not doc.findall('.//w:pBdr',ns) and not doc.findall('.//w:vanish',ns) and not doc.findall('.//w:ins',ns) and not doc.findall('.//w:del',ns),True)
 chk('No inherited title border in styles',not styles.findall('.//w:pBdr',ns),True)
xn={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(R/'03_budget/Implementation_Resources.xlsx') as z:
 formulas=[];errors=[];caches=[]
 for name in z.namelist():
  if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',name):
   tree=ET.fromstring(z.read(name))
   for c in tree.findall('.//x:c',xn):
    if c.attrib.get('t')=='e':errors.append((name,c.attrib.get('r'),c.findtext('x:v',namespaces=xn)))
    if c.find('x:f',xn) is not None:formulas.append((name,c.attrib['r']));caches.append(c.findtext('x:v',namespaces=xn))
 chk('Workbook contains live formulas and no cached errors',len(formulas)>200 and not errors,{'formula_cells':len(formulas),'errors':errors})
chk('Workbook recalculation tests passed',json.loads((R/'QA/workbook_recalculation.json').read_text())['restored'],True)
result={'task':m['task_id'],'date':'2026-11-06','basis':'10 kW module','tests':len(checks),'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','checks':checks,'scope_limit':'Design/file/arithmetic checks only. No physical experiment, partner commitment or Portal submission was executed.'}
(R/'QA/qa_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(R/'QA/QA_Results_CN.md').write_text('# 一致性检查结果\n\n任务 '+m['task_id']+'，10 kW版。\n\n'+f"状态 **{result['status']}**；{result['passed']}/{result['tests']}项通过。\n\n"+'检查包括：任务/ID/日期/责任、逐层PM和成本、角色峰值、早期交付、36个月依赖、10 kW库存与水/蒸汽流量、93次合成及粉体平衡、M23前产能、144完整运行矩阵、风险字段、原模板哈希、Word字号/内容及Excel公式。\n\nExcel另有两个真实改输入→重算→恢复测试：Savery费率增加€1/PM使总额增加€97.50；实验室电价增加€1/MWh使总额增加€51.25。公式错误扫描零命中。没有执行Microsoft Excel界面复核；使用公式引擎及保存文件结构/缓存校核。\n\n这些是设计与文件检查，不是设备测试或伙伴能力确认。剩余执行前提见设计假设和L2回件。\n')
print(json.dumps({k:result[k] for k in ['status','tests','passed','failed']}))
for c in checks:
 if not c['passed']:print(c)
sys.exit(0 if result['status']=='PASS' else 1)
