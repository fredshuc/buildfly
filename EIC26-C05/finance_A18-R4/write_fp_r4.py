import sys, json, openpyxl, shutil
src, js, dst = sys.argv[1], sys.argv[2], sys.argv[3]
raw=json.load(open(js)); out={int(k):v for k,v in raw.items() if k[0]!='_'}; out['_c82']=raw.get('_c82')
wb=openpyxl.load_workbook(src)
ws=wb['Financial plan']
print('validations',len(ws.data_validations.dataValidation),'cf',len(ws.conditional_formatting))
cols={2027:'C',2028:'D',2029:'E',2030:'F',2031:'G'}
rowmap={17:'rev',18:'gm',19:'sga',20:'rd',21:'oth',23:'int',24:'dep',25:'other',27:'tax',31:'ocf',32:'inv',
        35:'grants',36:'debt_in',37:'debt_out',38:'eq',45:'cash',46:'inventory',47:'ar',48:'ppe',50:'oa',53:'ap',54:'st',55:'lt',56:'ol',59:'sc',60:'re',61:'oe'}
for y,c in cols.items():
    o=out[y]; o['ap']=0
    for r,k in rowmap.items():
        cell=ws[f'{c}{r}']
        assert not (isinstance(cell.value,str) and str(cell.value).startswith('=')), cell.coordinate
        cell.value=(o[k] if k=='eq' else round(o[k],2))
    ws[f'{c}39'].value=0; ws[f'{c}49'].value=0
ws['C80'].value=66
ws['D80'].value='Business-plan forecast burn for November 2026 (EUR66k); October 2026 actual all-account burn to be reconciled.'
ws['C82'].value=round(out['_c82'],2)
ws['D82'].value='EUR94.98m cumulative operating and investing cash from EUR300k (3 Nov 2026) to the low point in Feb 2032, before trailing-12-month operating cash flow turns positive (May 2032). Business-plan costs with the pre-Seed cost plan; no grant, equity or debt receipts deducted.'
ws['C83'].value='03/27'
ws['D83'].value='Current cash covers the pre-Seed cost plan until the grant pre-financing at action start (April 2027); the Seed closes in November 2027.'
ws['D100'].value='EIC EUR2m within the EUR8m Seed (September 2027 launch, November 2027 close), subject to EIC investment due diligence.'
ws['D101'].value='Other Seed investors: EUR6m gross in the same November 2027 close. Five-year other-investor equity is reported in Equity needed D15.'
we=wb['Equity needed']
we['C16'].value=('N=2027; all five years are forecasts. EUR103m gross equity targets less EUR1.873m fees = EUR101.127m net. '
 'EIC: EUR2m; other investors: EUR99.127m net over five years. Seed EUR8m including EIC EUR2m: launch September 2027, close November 2027. '
 ' Later rounds: Series A April 2028, Series B January 2030. Fees borne by non-EIC funds.')
wb.calculation.fullCalcOnLoad=True
wb.save(dst)
w2=openpyxl.load_workbook(dst)['Financial plan']
print('after: validations',len(w2.data_validations.dataValidation),'cf',len(w2.conditional_formatting))
