"""Write one installed STEP with D01 definitions shared, excluding its old HOST."""
from pathlib import Path
import json,hashlib
from OCP.TDocStd import TDocStd_Document
from OCP.STEPCAFControl import STEPCAFControl_Reader,STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_Label,TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString as String
from OCP.TopLoc import TopLoc_Location
from OCP.gp import gp_Trsf,gp_Vec
from OCP.IFSelect import IFSelect_RetDone
from OCP.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCP.XCAFDoc import XCAFDoc_ColorGen
from cad_io import named,leaves
from integrate_c07 import HERE,C06,D01,D02,HX,ORIGINS,merged_water

def nm(label):
    a=TDataStd_Name()
    return a.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(),a) else ""
def title(label,name):
    TDataStd_Name.Set_s(label,String(name))
def placement(xyz):
    tr=gp_Trsf();tr.SetTranslation(gp_Vec(*xyz));return TopLoc_Location(tr)
def main():
    doc=TDocStd_Document(String("C07"))
    rd=STEPCAFControl_Reader();rd.SetNameMode(True);rd.SetColorMode(True)
    assert rd.ReadFile(str(D01/"cad/D01_EIGHT_DAMPERS_INSTALLED.step"))==IFSelect_RetDone and rd.Transfer(doc)
    st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main()); ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    q=TDF_LabelSequence();st.GetFreeShapes(q);assert q.Length()==1
    root=q.Value(1);children=TDF_LabelSequence();st.GetComponents_s(root,children);drops=[]
    for j in range(1,children.Length()+1):
        l=children.Value(j);t=TDF_Label();st.GetReferredShape_s(l,t)
        if nm(t)=="HOST":drops.append((l,t))
    assert len(drops)==1
    component,old_product=drops[0]
    st.RemoveComponent(component);st.RemoveShape(old_product,True)
    title(root,"C07_INSTALLED_MACHINE")
    def product(name,group,color):
        label=st.NewShape();title(label,name)
        for n,s in group.items():
            definition=st.AddShape(s.wrapped,False);title(definition,n)
            occ=st.AddComponent(label,definition,TopLoc_Location());title(occ,n)
            ct.SetColor(definition,Quantity_Color(*color,Quantity_TOC_RGB),XCAFDoc_ColorGen)
        return label
    modules=[("C07_SHEET_METAL",named(HERE/"C07_SHELL.step"),(.52,.65,.70)),
        ("D02_DAMPER_SUPPORTS",named(D02/"cad/D02_DAMPER_SUPPORTS.step"),(.32,.38,.42)),
        ("HYD_R2_INSTALLED",merged_water(),(.22,.48,.65))]
    for name,g,c in modules:
        occ=st.AddComponent(root,product(name,g,c),TopLoc_Location());title(occ,name)
    hx=product("M101_C05",named(HX/(HX.name+".step")),(.72,.52,.30))
    for b,xyz in ORIGINS.items():title(st.AddComponent(root,hx,placement(xyz)),b+"_HX_C05")
    st.UpdateAssemblies()
    wr=STEPCAFControl_Writer();wr.SetColorMode(True);wr.SetNameMode(True)
    assert wr.Transfer(root,STEPControl_AsIs)
    out=HERE/"C07_INSTALLED_MACHINE.step"
    assert wr.Write(str(out))==IFSelect_RetDone
    counts={}
    for n,s in leaves(out):
        path=n.split("/")
        assert "HOST" not in path
        assert "C07_INSTALLED_MACHINE" in path
        group=next((c for c in ("C07_SHEET_METAL","D02_DAMPER_SUPPORTS","HYD_R2_INSTALLED","A_HX_C05","B_HX_C05") if c in path),"D01")
        counts[group]=counts.get(group,0)+1
    assert counts=={"C07_SHEET_METAL":len(modules[0][1]),"D02_DAMPER_SUPPORTS":149,"HYD_R2_INSTALLED":44,"A_HX_C05":549,"B_HX_C05":549,"D01":7212},counts
    (HERE/"machine_readback.json").write_text(json.dumps({"shell_sha256":hashlib.sha256((HERE/"C07_SHELL.step").read_bytes()).hexdigest(),"installed_occurrences":sum(counts.values()),"by_module":counts,"old_HOST_occurrences":0},indent=2))
    print(counts,flush=True)
if __name__=="__main__":main()
