import sys, openpyxl, json
bp=openpyxl.load_workbook(sys.argv[1],data_only=True)
A={r[0]:r[1:] for r in bp['Annual'].iter_rows(values_only=True) if r[0]}
yrs=[2027,2028,2029,2030,2031]; col={y:A['Calendar year'].index(y) for y in yrs}
g=lambda k,y: A[k][col[y]]*1000  # k€
M=[r for r in bp['Monthly'].iter_rows(min_row=6,values_only=True) if hasattr(r[0],'year')]
def msum(ci,y): return sum((r[ci] or 0) for r in M if r[0].year==y)*1000
# annual bad debt from monthly? use L2 values for split of other opex
bad={2027:2.28,2028:9.46,2029:50.33,2030:158.52,2031:419.21}
grant_earned={2027:813.76,2028:1476.04,2029:195.79,2030:0,2031:0}
# scale grant earned to exact 2485.583
s=sum(grant_earned.values()); grant_earned={y:v*2485.58333/s for y,v in grant_earned.items()}
grant_rcv={2027:1491.35,2028:621.40,2029:372.84,2030:0,2031:0}
eq_net={2027:8000-145.4545,2028:25000-454.5455,2029:0,2030:70000-1272.7273,2031:0}
legacy_int={2027:2.91667}; legacy_settle={2027:13.125}; legacy_princ={2027:250.0}
import json as _j
cats=_j.load(open('/tmp/claude-0/-home-user-buildfly/b6cc519c-5a29-5537-9192-f5523eb5b76d/scratchpad/a18r2/../rephase_final_cats.json'))
CAPEX={2027:450.0,2028:5050.0}
out={}
cash=164.558; ppe=0; re=164.558-65.53-250.0; oe=250.0; grant_bal=0
for y in yrs:
    rev=g('Revenue',y); gp=g('Gross profit',y)+g('Production D&A add-back',y)
    rd=g('R&D expense',y); sgao=g('Sales, admin and other OPEX',y)
    sv=0
    if y==2027:
        gp+=cats['cogs']; rd-=cats['rd']; sgao-=cats['sga']; sv=cats['cogs']+cats['rd']+cats['sga']
    ebitda=gp-rd-sgao
    assert abs(ebitda-g('EBITDA',y)-sv)<1e-6
    da=g('Total D&A',y); fin=g('Finance expense',y)-legacy_int.get(y,0)
    ebt=ebitda-fin-da+grant_earned[y]; tax=g('Tax expense',y); ni=ebt-tax
    ocf=g('Operating cash flow',y)+legacy_settle.get(y,0)+sv
    capx=CAPEX.get(y,g('CAPEX',y)); inv=-capx
    draws=g('Debt drawings',y); rep=g('Principal repayments',y)-legacy_princ.get(y,0)
    finCF=grant_rcv[y]+draws-rep+eq_net[y]
    cash+=ocf+inv+finCF
    ppe+=capx-da
    grant_bal+=grant_rcv[y]-grant_earned[y]   # >0 deferred liability, <0 receivable
    re+=ni; oe+=eq_net[y]
    nexty=y+1; nrep=(A['Principal repayments'][A['Calendar year'].index(nexty)])*1000 if nexty in A['Calendar year'] else 0
    debt=g('Closing financing debt',y); st=min(nrep,debt); lt=debt-st
    inventory=g('Year-end inventory',y); ar=g('Receivables net',y); prep=g('Supplier prepayments',y)
    other_assets=prep+max(0,-grant_bal); defrev=g('Deferred customer revenue',y)
    other_liab=defrev+max(0,grant_bal)
    assets=cash+inventory+ar+ppe+other_assets; liab=st+lt+other_liab; equity=65.53+re+oe
    out[y]=dict(rev=rev,gm=gp,sga=sgao-bad[y],rd=rd,oth=bad[y],ebitda=ebitda,int=fin,dep=da,other=-grant_earned[y],ebt=ebt,tax=tax,ni=ni,
               ocf=ocf,inv=inv,fin=finCF,grants=grant_rcv[y],debt_in=draws,debt_out=-rep,eq=eq_net[y],cash=cash,inventory=inventory,ar=ar,ppe=ppe,
               oa=other_assets,ap=0,st=st,lt=lt,ol=other_liab,sc=65.53,re=re,oe=oe,resid=assets-liab-equity,bp_cash=g('Closing bank cash',y))
for k in ['rev','gm','sga','rd','oth','ebitda','int','dep','other','ebt','ni','ocf','inv','fin','grants','debt_in','debt_out','eq','cash','bp_cash','inventory','ar','ppe','oa','st','lt','ol','re','oe','resid']:
    print(f'{k:9s}',' '.join(f'{out[y][k]:12.2f}' for y in yrs))
json.dump(out,open(sys.argv[2],'w'))
