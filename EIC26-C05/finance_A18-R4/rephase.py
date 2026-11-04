import sys, openpyxl, json
bp=openpyxl.load_workbook(sys.argv[1],data_only=True)
br=openpyxl.load_workbook(sys.argv[2],data_only=True)
M={r[0].strftime('%Y-%m'):r for r in bp['Monthly'].iter_rows(min_row=6,values_only=True) if hasattr(r[0],'year')}
def sheet(n):
    rows=list(br[n].iter_rows(min_row=4,values_only=True)); h=rows[0]
    return {(r[0].strftime('%Y-%m') if hasattr(r[0],'strftime') else str(r[0])[:7]):dict(zip(h,r)) for r in rows[1:] if r[0]}
S=sheet('Source operations'); P=sheet('Programme inputs')
months=sorted(k for k in M if '2027-01'<=k<='2031-12')
def eic_opex(m):
    p=P.get(m); 
    if not p: return 0
    return sum((p.get(k) or 0) for k in ['Action payroll','Action subcontract','Action travel','Action other purchase'])/1e6
def eic_capex(m):
    p=P.get(m); return ((p.get('Action capex') or 0)/1e6) if p else 0
cfg=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
SEED=cfg.get('seed','2027-11'); RESTART=cfg.get('restart','2027-12')
sav={}; capex_new={}
for m in months:
    s=S[m]; s0=0.0
    pre = m<RESTART
    if pre and m>='2027-03':
        s0+= s['Sales payroll']/1e6*cfg.get('sales_defer',1.0)          # sales hires after Seed
        s0+= (s['Admin payroll']-9.8e3)/1e6                              # admin step-up after Seed
        if m=='2027-03': s0+= (s['Other fixed']-5.1e3)/1e6               # facility/overhead step-up from April with the action team
    if pre and m>='2027-01' and m<='2027-03':
        s0+= (s['R&D']-47.5e3)/1e6                                       # R&D step-up starts with the action (April)
    if pre and m>='2027-04':
        nonEIC=max(0,s['R&D']/1e6-eic_opex(m)-cfg.get('core_rd',0.0))
        s0+= nonEIC*cfg.get('rd_defer',0.0)                               # non-EIC R&D after Seed
        # field payroll: EU team from July, NA team after Seed
        fp=s['Field payroll']/1e6
        if m<'2027-07': s0+=fp
        else: s0+=fp/2*cfg.get('na_defer',1.0)
    if cfg.get('inv_shift') and m=='2027-03': s0+=0.1295      # reference-unit materials bought at production start (June)
    if cfg.get('inv_shift') and m=='2027-06': s0-=0.1295
    if cfg.get('factory_may') and m in ('2027-03','2027-04'): s0+=0.0167   # factory staff from May, production start June
    if cfg.get('fixed_half') and pre and '2027-04'<=m: s0+=(s['Other fixed']-5.1e3)/2e6  # half the overhead step-up after Seed
    if cfg.get('ext_pause') and m in ('2027-01','2027-02','2027-03'): s0+=0.0296   # baseline external R&D paused until the action starts
    sav[m]=s0
# capex: replace BP 700k (Mar/Jun 2027) by EIC asset schedule + rest of the 700k after Seed
for m in months:
    c=M[m][25]
    if m in ('2027-03','2027-06'): c=0
    c+=eic_capex(m)
    if m==RESTART: c+=0.700-sum(eic_capex(x) for x in months)
    capex_new[m]=c
eq={SEED:(8,0.145454),'2028-04':(25,0.454545),'2030-01':(70,1.272727)}
grant={'2027-04':1.49135,'2028-04':0.6214,'2029-06':0.37284}
c=0.164558; path={}; low=(9,None)
for m in months:
    r=M[m]
    ocf=r[24]+sav[m]+(0.013125 if m=='2027-03' else 0)
    rep=r[30]-(0.25 if m=='2027-03' else 0)
    g,f=eq.get(m,(0,0))
    c+=ocf-capex_new[m]+r[29]-rep+grant.get(m,0)+g-f
    path[m]=c
    if c<low[0]: low=(c,m)
yr=lambda y: sum(v for k,v in sav.items() if k.startswith(y))
print('cfg',cfg,'| min cash',round(low[0],3),low[1],'| 2027 cost savings',round(yr('2027'),3),'| capex 2027',round(sum(v for k,v in capex_new.items() if k<'2028'),3),'2028',round(sum(v for k,v in capex_new.items() if k.startswith('2028')),3))
print(' path',{k:round(v,2) for k,v in path.items() if k<='2028-04'})
json.dump({'sav':sav,'capex':capex_new,'path':path},open(cfg.get('out','/dev/null'),'w'))
