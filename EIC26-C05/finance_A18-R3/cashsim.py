import sys, openpyxl, datetime as dt
wb=openpyxl.load_workbook(sys.argv[1],data_only=True); ws=wb['Monthly']
rows=[r for r in ws.iter_rows(min_row=6,values_only=True) if hasattr(r[0],'year')]
M={r[0].strftime('%Y-%m'):r for r in rows}
months=[k for k in sorted(M) if '2027-01'<=k<='2031-12']
def run(opening, equity, grant, drop_old_debt=True, label=''):
    c=opening; low=(1e9,None); path={}
    for m in months:
        r=M[m]; fcf=r[26]; draws=r[29]; rep=r[30]
        if drop_old_debt and m=='2027-03': rep-=0.25
        c+= fcf + draws - rep + equity.get(m,0) + grant.get(m,0)
        path[m]=c
        if c<low[0]: low=(c,m)
    return low,path
bp_open=M['2026-12'][32]
act_open=0.164558
grant={'2027-04':1.49135,'2028-04':0.6214,'2029-06':0.37284}
bp_eq={m:M[m][27]-M[m][28] for m in months if M[m][27]}
print('BP check low 2027-2031:',run(bp_open,bp_eq,{},drop_old_debt=False)[0])
eurA={'2027-03':6-0.145454,'2027-11':2.0,'2028-04':25-0.454545,'2030-01':70-1.272727}
eurB={'2027-11':8-0.145454,'2028-04':25-0.454545,'2030-01':70-1.272727}
eurBP_EUR={'2027-03':8-0.145454,'2028-04':25-0.454545,'2030-01':70-1.272727}
for lab,eq in [('A: Mar27 €6m private + Nov27 €2m EIC',eurA),('A2: Mar27 €8m incl EIC',eurBP_EUR),('B: Nov27 €8m',eurB)]:
    for g,gl in [(grant,'grant 60/25/15'),({}, 'no grant')]:
        low,p=run(act_open,eq,g)
        print(f'{lab:40s} {gl:15s} low {low[0]:.3f} in {low[1]} | Dec27 {p["2027-12"]:.2f} Dec28 {p["2028-12"]:.2f} Dec29 {p["2029-12"]:.2f} Dec30 {p["2030-12"]:.2f} Dec31 {p["2031-12"]:.2f}')
# before-seed months under A
low,p=run(act_open,eurA,grant)
print({m:round(p[m],3) for m in months[:14]})
low,p=run(act_open,eurB,grant)
print('B path',{m:round(p[m],3) for m in months[:12]})
