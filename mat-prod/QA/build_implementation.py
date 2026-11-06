#!/usr/bin/env python3
"""Generate proposal tables, CSVs, schedule figures and DOCX from one model."""
import json,csv,math,pathlib,argparse,re,hashlib,datetime
from collections import defaultdict
R=pathlib.Path(__file__).resolve().parents[1]
M=json.loads((R/'03_budget/implementation_model.json').read_text())
P=[p['id'] for p in M['partners']]; rates={p['id']:p['pm_rate'] for p in M['partners']}
S=R/'01_proposal/Schedule_and_Dependencies';S.mkdir(exist_ok=True)
C=R/'03_budget/CSV';C.mkdir(exist_ok=True)
def outcsv(path,rows):
 if not rows:return
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def num(x):return f'{x:,.0f}' if x==round(x) else f'{x:,.2f}'.rstrip('0').rstrip('.')
def table(headers,rows):
 def v(x):return str(x).replace('|','/').replace('\n',' ')
 return '| '+' | '.join(map(v,headers))+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(v,row))+' |' for row in rows)+'\n'
def build():
 pm={p:sum(t['pm'][p] for t in M['tasks']) for p in P}
 for c in M['costs']:c['calculated_cost']=c['qty']*c['unit_cost']*c['use_share']*c['eligible_fraction']*c['project_months']/c['life_months']
 budgets=[]
 for p in M['partners']:
  i=p['id'];pr=pm[i]*p['pm_rate'];cat={c:sum(v['calculated_cost'] for v in M['costs'] if v['partner']==i and v['category']==c) for c in ['C1','C2','C3']}
  direct=pr+sum(cat.values());ib=pr+sum(c['calculated_cost']*c['indirect_eligible'] for c in M['costs'] if c['partner']==i)
  b=dict(partner=i,pm=pm[i],pm_rate=p['pm_rate'],personnel=pr,travel=cat['C1'],equipment=cat['C2'],other_goods_services=cat['C3'],subcontracting=0,internal_recharge=0,direct=direct,indirect_base=ib,indirect=ib*M['indirect_rate'],total=direct+ib*M['indirect_rate'],initial=p['initial_budget'])
  b['change']=b['total']-b['initial'];budgets.append(b)
 monthly=[]
 for p in M['partners']:
  i=p['id'];a=[sum(t['pm'][i]/(t['end']-t['start']+1) for t in M['tasks'] if t['start']<=mo<=t['end']) for mo in range(1,37)]
  r=dict(partner=i,pm=pm[i],average_fte=pm[i]/36,peak_fte=max(a),peak_months=','.join(str(j+1) for j,x in enumerate(a) if abs(x-max(a))<1e-9))
  r.update({f'M{j+1}':x for j,x in enumerate(a)});r.update({f'phase_{j+1}_fte':sum(a[j*6:j*6+6])/6 for j in range(6)});monthly.append(r)
 roles=[]
 for p in M['partners']:
  for name,amount,cap,heads in p['roles']:
   peak=next(x['peak_fte'] for x in monthly if x['partner']==p['id'])*amount/pm[p['id']]
   roles.append(dict(partner=p['id'],role=name,pm=amount,average_fte=amount/36,peak_fte=peak,planned_fte_capacity=cap,minimum_people=heads,capacity_margin=cap-peak,basis='Pro-rata task-month profile; replace with named-role availability before partner commitment'))
 wp=[]
 for w in M['wps']:
  d=dict(w);d['pm']=sum(sum(t['pm'].values()) for t in M['tasks'] if t['wp']==w['id']);d['personnel']=sum(t['pm'][p]*rates[p] for t in M['tasks'] if t['wp']==w['id'] for p in P);d['purchases']=sum(c['calculated_cost'] for c in M['costs'] if c['wp']==w['id']);d['total']=(d['personnel']+d['purchases'])*1.25;wp.append(d)
 tasks=[]
 for t in M['tasks']:
  d={k:t[k] for k in ['id','wp','name','lead','start','end']};d.update(t['pm']);d['total_pm']=sum(t['pm'].values());d['personnel_cost']=sum(t['pm'][p]*rates[p] for p in P);d['inputs']=t['inputs'];d['work']=t['work'];d['acceptance']=t['acceptance'];tasks.append(d)
 workloads=[]
 for w in M['workloads']:
  v=dict(w);v['total_output']=w['count']*w['amount_per_unit'];v['total_hours']=w['count']*w['hours_per_unit'];workloads.append(v)
 # CPM uses elapsed months at boundaries; an activity with ES=0 and EF=2 runs M1-M2.
 nodes={x[0]:dict(id=x[0],name=x[1],duration=x[2],predecessors=x[3]) for x in M['cpm']};pending=set(nodes)
 order=[]
 while pending:
  ready=sorted(i for i in pending if all(p in order for p in nodes[i]['predecessors']))
  if not ready:raise ValueError('Cycle in CPM graph')
  for i in ready:
   n=nodes[i];n['ES']=max([nodes[p]['EF'] for p in n['predecessors']]+[0]);n['EF']=n['ES']+n['duration'];order.append(i);pending.remove(i)
 finish=max(n['EF'] for n in nodes.values())
 for i in reversed(order):
  n=nodes[i];succ=[s for s in nodes if i in nodes[s]['predecessors']];n['LF']=min([nodes[s]['LS'] for s in succ]+[finish]);n['LS']=n['LF']-n['duration'];n['float']=n['LS']-n['ES'];n['start_month']=n['ES']+1;n['end_month']=n['EF']
 cpm=[{**nodes[i],'predecessors':','.join(nodes[i]['predecessors'])} for i in order]
 deps=[dict(predecessor=p,successor=n['id'],type='finish-to-start',lag_months=0) for n in nodes.values() for p in n['predecessors']]
 for name,rows in [('Tasks',tasks),('Budget',budgets),('Costs',M['costs']),('WP',wp),('Monthly_FTE',monthly),('Roles',roles),('Workload',workloads),('Milestones',M['milestones']),('Deliverables',M['deliverables']),('Risks',M['risks']),('Interfaces',M['interfaces'])]:outcsv(C/(name+'.csv'),rows)
 outcsv(S/'Critical_Path.csv',cpm);outcsv(S/'Dependencies.csv',deps)
 outcsv(S/'Task_Schedule.csv',[{k:t[k] for k in ['id','wp','name','lead','start','end']} for t in M['tasks']])
 outcsv(C/'Conditions.csv',[dict(zip(['id','split','source_C','rejection_C','hot_supply_C','duty_kW','history'],x)) for x in M['conditions']])
 outcsv(C/'Assumptions.csv',[dict(zip(['id','item','status','basis'],x)) for x in M['assumptions']])
 outcsv(C/'Facilities.csv',[dict(zip(['partner','facility','hours','unit','basis'],x)) for x in M['facilities']])
 result=dict(partners=budgets,wps=wp,monthly=monthly,roles=roles,workload=workloads,cpm=cpm,total_pm=sum(pm.values()),total_budget=sum(b['total'] for b in budgets),total_direct=sum(b['direct'] for b in budgets),total_personnel=sum(b['personnel'] for b in budgets),total_equipment=sum(b['equipment'] for b in budgets),rig_hours=sum(w['total_hours'] for w in workloads if w['id'] in [f'W{i:02d}' for i in range(15,22)]),cpm_finish=finish)
 (R/'03_budget/calculated_snapshot.json').write_text(json.dumps(result,indent=2)+'\n')
 fragments={}
 fragments['TABLE_A']='### Table 3.1a List of work packages\n\n'+table(['Work package No','Work Package Title','Lead Participant No','Lead Participant Short Name','Person-Months','Start Month','End month'],[[w['id'],w['title'],next(p['number'] for p in M['partners'] if p['id']==w['lead']),w['lead'],num(w['pm']),w['start'],w['end']] for w in wp])
 bs=[]
 for w in wp:
  a=f"#### Work package {w['id'][2:]}\n\nWork package number: {w['id']}. Work package title: {w['title']}.\n\n**Objectives.** {w['objectives']}\n\n**Description of work.** Lead: {w['lead']}; M{w['start']}–M{w['end']}; {num(w['pm'])} PM.\n"
  for t in [t for t in M['tasks'] if t['wp']==w['id']]:
   a+=f"\n**{t['id']} {t['name']}.** M{t['start']}–M{t['end']}; lead {t['lead']}. Input and dependency: {t['inputs']} {t['work']} Acceptance: {t['acceptance']} Effort: "+', '.join(f"{p} {num(t['pm'][p])}" for p in P if t['pm'][p])+f" PM; total {num(sum(t['pm'].values()))} PM.\n"
  bs.append(a)
 fragments['TABLE_B']='### Table 3.1b Work package description\n\n'+'\n'.join(bs)
 fragments['TABLE_C']='### Table 3.1c List of Deliverables\n\n'+table(['Number','Deliverable name','Short description','Work package number','Short name of lead participant','Type','Dissemination level','Delivery date (in months)'],[[d['id'],d['name'],d['description'],d['wp'],d['lead'],d['type'],d['dissemination'],d['month']] for d in M['deliverables']])+'\nPU: public, after background/IP review. SEN: sensitive, restricted to the applicable grant-access conditions. OTHER: executable data/model/software package. Only interface, review and validation outputs are formal deliverables; routine boards and working records remain internal.\n'
 fragments['TABLE_D']='### Table 3.1d List of milestones\n\n'+table(['Milestone number','Milestone name','Related work package(s)','Due date (in month)','Means of verification'],[[d['id'],d['name'],d['wps'],d['month'],d['verification']] for d in M['milestones']])
 fragments['TABLE_E']='### Table 3.1e Critical risks for implementation\n\n'+table(['Description of risk (likelihood and severity)','Work package(s) involved','Proposed risk-mitigation measures'],[[f"{d['id']} {d['name']}. Likelihood {d['likelihood']}, severity {d['severity']}. Trigger: {d['trigger']} Impact: {d['impact']}",d['wps'],d['mitigation']+' Time/cost consequence: '+d['consequence']] for d in M['risks']])+'\nH, M and L denote high, medium and low. Cost exposures are overlapping conditional estimates, not additive allocations or a booked reserve. Existing work may absorb a change only after its affected scope is identified; additional eligible expenditure must remain within the ceiling.\n'
 rows=[[p, *[('**'+num(sum(t['pm'][p] for t in M['tasks'] if t['wp']==w['id']))+'**') if w['lead']==p else num(sum(t['pm'][p] for t in M['tasks'] if t['wp']==w['id'])) for w in wp],num(pm[p])] for p in P]
 rows.append(['Total Person Months',*[num(w['pm']) for w in wp],num(sum(pm.values()))])
 fragments['TABLE_F']='### Table 3.1f Summary of staff effort\n\n'+table(['Participant Number/Short Name',*[w['id'] for w in wp],'Total Person-Months per Participant'],[[str(i+1)+'/'+str(r[0]),*r[1:]] if i<5 else r for i,r in enumerate(rows)])
 fragments['BUDGET']='### Recommended budget in EUR\n\n'+table(['Participant','Personnel','Travel','Equipment use','Other goods/services','Direct','Indirect','Total'],[[b['partner'],*[num(b[k]) for k in ['personnel','travel','equipment','other_goods_services','direct','indirect','total']]] for b in budgets]+[['Total',*[num(sum(b[k] for b in budgets)) for k in ['personnel','travel','equipment','other_goods_services','direct','indirect','total']]]])
 fragments['BUDGET']+='\nBold PM values in Table 3.1f identify the WP leader.\n'
 fragments['FTE']='### Six month FTE profile\n\n'+table(['Participant','M1–6','M7–12','M13–18','M19–24','M25–30','M31–36','Peak monthly FTE'],[[x['partner'],*[f"{x['phase_'+str(j+1)+'_fte']:.2f}" for j in range(6)],f"{x['peak_fte']:.2f}"] for x in monthly])
 fragments['TABLE_G']='### Table 3.1g Subcontracting costs items\n\n'+table(['Participant Number/Short Name','Cost (€)','Description of tasks and justification'],[[str(p['number'])+'/'+p['id'],'0','No action task is planned for subcontracting. Routine instrument access/calibration purchases do not transfer research-task responsibility.'] for p in M['partners']])
 sb=next(b for b in budgets if b['partner']=='SAV')
 fragments['TABLE_H']='### Table 3.1h Purchase costs items major equipment costs\n\n'+table(['Participant Number/Short Name','Cost (€)','Justification'],[['1/SAV',num(c['calculated_cost']),c['description']+'. '+c['basis']+'.'] for c in M['costs'] if c['partner']=='SAV' and c['category']=='C2'])+f"\nSAV equipment use totals EUR {num(sb['equipment'])}, or {sb['equipment']/sb['personnel']*100:.2f}% of its personnel costs, exceeding the template’s 15% threshold. Other participants are below it: IRC 4.17%, IKTS 3.75%, UP 8.18% and HPE 1.71%. All equipment costs remain in the resource workbook. The threshold applies to equipment costs, not all purchases. Recoverable VAT is excluded; no procurement or asset availability is represented as committed.\n"
 fragments['INTERFACES']=table(['Interface','Provider to accepting partners','Release months','Data/model contract and acceptance'],[[i['id'],i['sender']+' to '+i['receiver'],i['months'],i['contract']+' Acceptance: '+i['acceptance']] for i in M['interfaces']])
 fragments['WP_GANTT']='![Work package timing and validation period](Schedule_and_Dependencies/WP_Gantt.png)\n\nFigure 3.1 Work package timing. The task-level editable schedule also shows early reference work, the M24 freeze and the M33–M34 correction period.\n'
 fragments['DEPENDENCY_FIGURE']='![Work package feedback and handover dependencies](Schedule_and_Dependencies/WP_Dependencies.png)\n\nFigure 3.2 Material and digital feedback loops converge on laboratory validation. WP1 controls releases and resources; WP7 uses validated manufacture and performance records.\n'
 source=(R/'01_proposal/Section3_Narrative_Source_EN.md').read_text()
 for k,v in fragments.items():source=source.replace('{{'+k+'}}',v)
 if '{{' in source:raise ValueError('Unresolved narrative tokens')
 (R/'01_proposal/Section3_Implementation_EN.md').write_text(source)
 (S/'Schedule_Method.md').write_text('# Schedule and dependencies\n\nAll months are relative to the future project start. A 36-month action is a design assumption. Task dates overlap intentionally; finish-to-start dependencies in Critical_Path.csv refer to gated releases, not to the first exploratory work.\n\nThe two gating spines reach M24: A-B-C-D-E-F and A-R-S-T-J. G cannot start until both F and J finish. G runs M25–M32; H is explicit corrective work in M33–M34; I runs M35–M36. CPM duration is 36 months. All gates on these spines have zero mathematical float because the planned correction/evidence work occupies the remaining period. H is a two-month management correction allocation, not spare labour or monetary contingency.\n\nThe original Task_Schedule.csv preserves every task interval. WP_Gantt.svg and Task_Gantt.svg are editable vector files; the Mermaid sources are editable logic diagrams. References and preliminary models allow work to start before the corresponding final material/model release.\n\n'+table(['ID','Activity','Duration','Predecessors','Start','End','Float'],[[n['id'],n['name'],n['duration'],n['predecessors'],n['start_month'],n['end_month'],n['float']] for n in cpm]))
 (S/'WP_Dependencies.mmd').write_text('flowchart TD\n  A["WP2 Composition and production"] --> B["WP3 Shaping and manufacture"]\n  A --> C["WP4 Models and estimation"]\n  B --> C\n  C --> D["WP5 MPC and RL"]\n  B --> E["WP6 Laboratory validation"]\n  D --> E\n  E -.-> C\n  E -.-> A\n  E -.-> B\n  F["WP1 Quality and governance"] -.-> B\n  E --> G["WP7 Exploitation and sustainability"]\n  B --> G\n')
 (S/'Critical_Path.mmd').write_text('flowchart TD\n'+'\n'.join(f'  {n["id"]}["{n["id"]} {n["name"]} M{n["start_month"]} to M{n["end_month"]}"]' for n in cpm)+'\n'+'\n'.join(f'  {e["predecessor"]} --> {e["successor"]}' for e in deps)+'\n')
 return result,source

def figures():
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import textwrap
 from matplotlib.patches import FancyArrowPatch,Rectangle
 plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':10})
 colors=['#314E70','#597AA0','#3B817B','#6D65A0','#9B6C43','#3F6C93','#65734F']
 for mode in ['WP','Task']:
  rows=M['wps'] if mode=='WP' else M['tasks'];n=len(rows)
  fig,ax=plt.subplots(figsize=(7,4.6) if mode=='WP' else (12.4,10.4));fig.subplots_adjust(left=.41 if mode=='WP' else .40,right=.98,top=.80 if mode=='WP' else .87,bottom=.13 if mode=='WP' else .08)
  ax.axvspan(24.5,36.5,color='#EAF2F7',zorder=0);ax.axvspan(32.5,34.5,color='#F6E2BF',zorder=0)
  for j,w in enumerate(rows):
   ix=int((w['id'] if mode=='WP' else w['wp'])[2:])-1
   ax.broken_barh([(w['start']-.5,w['end']-w['start']+1)],(n-j-.31,.62),facecolors=colors[ix])
  labels=[textwrap.fill(w['id']+' '+(w['title'] if mode=='WP' else w['name']),32 if mode=='WP' else 48) for w in rows]
  ax.set_yticks([n-j for j in range(n)],labels,fontsize=9)
  ax.set_xlim(.5,36.5);ax.set_ylim(.3,n+.7);ax.set_xticks([1,6,12,18,24,30,36]);ax.set_xlabel('Project month');ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
  ax.axvline(24.5,color='#303840',linestyle='--',linewidth=1)
  for spine in ['top','right','left']:ax.spines[spine].set_visible(False)
  ax.tick_params(axis='y',length=0)
  fig.suptitle(('Work packages' if mode=='WP' else 'Task schedule')+' over 36 months',fontsize=13,x=.04,ha='left')
  fig.text(.04,.89 if mode=='WP' else .92,'M24 freeze. Blue: integrated validation M25–M36.\nAmber: correction and repeats M33–M34.',fontsize=8.5)
  fig.savefig(S/(mode+'_Gantt.svg'));fig.savefig(S/(mode+'_Gantt.png'),dpi=180);plt.close(fig)
 fig,ax=plt.subplots(figsize=(7.1,4.0));ax.set_xlim(0,11);ax.set_ylim(0,6);ax.axis('off')
 boxes={'A':(1.8,4.8,'WP2\nComposition and\nproduction'),'B':(1.8,3.05,'WP3\nShaping and\nmanufacture'),'C':(5.5,4.8,'WP4\nModels and\nestimation'),'D':(9.2,4.8,'WP5\nMPC and\nconstrained RL'),'E':(7.35,2.6,'WP6\nLaboratory\nvalidation'),'F':(1.8,.8,'WP1\nQuality and\ngovernance'),'G':(7.35,.8,'WP7\nExploitation and\nsustainability')}
 for k,(x,y,l) in boxes.items():ax.add_patch(Rectangle((x-1.45,y-.44),2.9,.88,facecolor='#F1F5F8',edgecolor='#697D8E',lw=1));ax.text(x,y,l,ha='center',va='center',fontsize=8)
 for a,b,style,rad in [('A','B','-',0),('A','C','-',0),('B','C','-',0),('C','D','-',0),('B','E','-',0),('D','E','-',0),('E','C','--',.17),('E','A','--',-.2),('E','B','--',.2),('F','B','--',0),('E','G','-',0),('B','G','-',-.15)]:
  x,y,_=boxes[a];xx,yy,_=boxes[b];dx=xx-x;dy=yy-y
  # Clip each arrow to the rectangular box boundary.
  ratio=min(1.45/abs(dx) if dx else 1e6,.44/abs(dy) if dy else 1e6)
  start=(x+dx*ratio,y+dy*ratio);end=(xx-dx*ratio,yy-dy*ratio)
  ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=12,color='#52687A',linewidth=1.1,linestyle=style,connectionstyle=f'arc3,rad={rad}'))
 fig.suptitle('Work package interfaces and feedback',fontsize=13,x=.05,ha='left');fig.text(.05,.03,'Solid: handover. Dashed: governance or measured feedback.',fontsize=8.5)
 fig.savefig(S/'WP_Dependencies.svg');fig.savefig(S/'WP_Dependencies.png',dpi=180);plt.close(fig)

 for svg in S.glob('*.svg'):
  svg.write_text('\n'.join(x.rstrip() for x in svg.read_text().splitlines())+'\n')

def docx(md):
 from docx import Document
 from docx.shared import Mm,Pt,RGBColor
 from docx.oxml import OxmlElement
 from docx.oxml.ns import qn
 from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
 from docx.enum.text import WD_ALIGN_PARAGRAPH
 from docx.enum.section import WD_SECTION_START,WD_ORIENT
 d=Document();sec=d.sections[0];sec.page_width=Mm(210);sec.page_height=Mm(297);sec.top_margin=Mm(16);sec.bottom_margin=Mm(16);sec.left_margin=Mm(16);sec.right_margin=Mm(16)
 for sn in ['Normal','Title','Heading 1','Heading 2','Heading 3','Heading 4','Caption']:
  st=d.styles[sn];st.font.name='Times New Roman';st.font.color.rgb=RGBColor(0,0,0);st.font.size=Pt(11 if sn=='Normal' else 15 if sn=='Title' else 12 if sn.startswith('Heading') else 9)
  st.paragraph_format.space_after=Pt(5);st.paragraph_format.line_spacing=1
 for sn in ['Heading 1','Heading 2','Heading 3','Heading 4']:d.styles[sn].paragraph_format.keep_with_next=True;d.styles[sn].paragraph_format.space_before=Pt(10)
 for st in d.styles:
  for border in st.element.xpath('./w:pPr/w:pBdr'):border.getparent().remove(border)
 for stname in ['Normal','Title','Heading 1','Heading 2','Heading 3','Heading 4']:
  st=d.styles[stname];st.font.underline=False
  rf=st.element.get_or_add_rPr().get_or_add_rFonts()
  for att in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
   if qn('w:'+att) in rf.attrib:del rf.attrib[qn('w:'+att)]
  for att in ['ascii','hAnsi','eastAsia','cs']:rf.set(qn('w:'+att),'Times New Roman')
 def inline(p,txt):
  parts=re.split(r'(\*\*[^*]+\*\*|\[[^]]+\]\(https?://[^)]+\))',txt)
  for part in parts:
   if not part:continue
   link=re.fullmatch(r'\[([^]]+)\]\((https?://[^)]+)\)',part)
   if link:
    from docx.opc.constants import RELATIONSHIP_TYPE
    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),d.part.relate_to(link.group(2),RELATIONSHIP_TYPE.HYPERLINK,is_external=True))
    rr=OxmlElement('w:r');pr=OxmlElement('w:rPr')
    sz=OxmlElement('w:sz');sz.set(qn('w:val'),'22');pr.append(sz)
    col=OxmlElement('w:color');col.set(qn('w:val'),'000000');pr.append(col)
    und=OxmlElement('w:u');und.set(qn('w:val'),'single');pr.append(und)
    rr.append(pr);tt=OxmlElement('w:t');tt.text=link.group(1);rr.append(tt);h.append(rr);p._p.append(h)
   else:
    r=p.add_run(part[2:-2] if part.startswith('**') else part);r.bold=part.startswith('**')
 def set_orientation(landscape):
  s=d.add_section(WD_SECTION_START.NEW_PAGE)
  s.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
  s.page_width=Mm(297 if landscape else 210);s.page_height=Mm(210 if landscape else 297)
  s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Mm(16)
 def make_table(lines):
  cells=lambda x:[x.strip() for x in x.strip().strip('|').split('|')]
  data=[cells(lines[0])]+[cells(x) for x in lines[2:]]
  n=len(data[0]);landscape=n>=7
  if (d.sections[-1].orientation==WD_ORIENT.LANDSCAPE)!=landscape:
   heading=None
   if d.paragraphs and d.paragraphs[-1].style.name.startswith('Heading'):
    last=d.paragraphs[-1];heading=(last.text,last.style.name);last._element.getparent().remove(last._element)
   set_orientation(landscape)
   if heading:d.add_paragraph(heading[0],heading[1])
  page_width=265 if landscape else 178
  t=d.add_table(rows=1,cols=n);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
  n=len(data[0]);widths=[1/n]*n
  # Allocate width by the actual table schema, not equally across narrative fields.
  h=data[0]
  if h[0]=='Description of risk (likelihood and severity)':widths=[.42,.13,.45]
  elif h[0]=='Milestone number':widths=[.12,.17,.12,.11,.48]
  elif h[0]=='Number':widths=[.07,.21,.26,.08,.12,.06,.11,.09]
  elif h[0]=='Work package No':widths=[.08,.34,.11,.13,.12,.11,.11]
  elif h[0]=='Interface':widths=[.10,.16,.20,.54]
  elif h[0]=='Participant Number/Short Name' and n==3:widths=[.18,.13,.69]
  elif h[0]=='Participant Number/Short Name':widths=[.22]+[.78/(n-1)]*(n-1)
  elif h[0]=='Participant' and n==8:widths=[.14]+[.86/7]*7
  for j,c in enumerate(t.rows[0].cells):c.width=Mm(page_width*widths[j])
  for j,w in enumerate(widths):t.columns[j].width=Mm(page_width*w)
  for ri,row in enumerate(data):
   cells_=t.rows[0].cells if ri==0 else t.add_row().cells
   for j,(c,txt) in enumerate(zip(cells_,row)):
    c.width=Mm(page_width*widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p=c.paragraphs[0];p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3);inline(p,re.sub(r',(?=[A-Za-z])',', ',txt))
    for run in p.runs:run.font.size=Pt(11)
    if ri==0:
     sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E9EEF2');c._tc.get_or_add_tcPr().append(sh)
     for run in p.runs:run.bold=True
    if n>=7 and j>0 and re.fullmatch(r'[\d,.]+',txt):p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    tcPr=c._tc.get_or_add_tcPr();mar=OxmlElement('w:tcMar')
    for side in ['top','left','bottom','right']:
     x=OxmlElement('w:'+side);x.set(qn('w:w'),'70');x.set(qn('w:type'),'dxa');mar.append(x)
    tcPr.append(mar)
   cant=OxmlElement('w:cantSplit');t.rows[ri]._tr.get_or_add_trPr().append(cant)
   if ri==0:
    repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
  borders=OxmlElement('w:tblBorders')
  for edge in ['top','left','bottom','right','insideH','insideV']:
   e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
  t._tbl.tblPr.append(borders)
  d.add_paragraph().paragraph_format.space_after=Pt(1)
 lines=md.splitlines();i=0
 while i<len(lines):
  s=lines[i].strip()
  if not s:i+=1;continue
  if s.startswith('|'):
   group=[]
   while i<len(lines) and lines[i].strip().startswith('|'):group.append(lines[i]);i+=1
   make_table(group);continue
  if s.startswith('!['):
   if d.sections[-1].orientation==WD_ORIENT.LANDSCAPE:set_orientation(False)
   match=re.search(r'!\[([^]]*)\]\(([^)]+)\)',s);p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
   p.add_run().add_picture(str(R/'01_proposal'/match.group(2)),width=Mm(178))
   i+=1;continue
  if s.startswith('#'):
   nxt=next((x.strip() for x in lines[i+1:] if x.strip()),'')
   next_landscape=nxt.startswith('|') and len(nxt.strip('|').split('|'))>=7
   if d.sections[-1].orientation==WD_ORIENT.LANDSCAPE and not next_landscape:set_orientation(False)
   lev=len(s)-len(s.lstrip('#'));txt=s[lev:].strip();d.add_paragraph(txt,'Title' if lev==1 else 'Heading '+str(min(lev-1,4)));i+=1;continue
  if d.sections[-1].orientation==WD_ORIENT.LANDSCAPE:set_orientation(False)
  p=d.add_paragraph();inline(p,s)
  if s.startswith('Figure 3.'):p.style=d.styles['Caption']
  if s.startswith(('S2.','S3.','S4.','S5.','S6.','S7.','S8.')):
   for r in p.runs:r.font.size=Pt(11)
  i+=1
 # Basic pagination only; no substantive information lives in headers/footers.
 p=sec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.RIGHT;r=p.add_run();fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');r._r.addnext(fld)
 d.core_properties.title='Section 3 Implementation';d.core_properties.subject=M['task_id'];d.core_properties.author='Savery consortium';d.core_properties.comments=''
 target=R/'01_proposal/Section3_Implementation_EN.docx';d.save(target);return target

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--docx',action='store_true');args=a.parse_args()
 result,md=build();figures()
 if args.docx:print(docx(md))
 print(json.dumps({k:result[k] for k in ['total_pm','total_budget','total_direct','total_personnel','total_equipment','rig_hours','cpm_finish']}))
 print('Role peak margins:',[(r['partner'],r['role'],round(r['capacity_margin'],3)) for r in result['roles']])
