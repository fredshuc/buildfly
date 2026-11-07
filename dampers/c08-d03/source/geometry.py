from pathlib import Path
import sys
import json
import hashlib
import csv
import os
import zipfile

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
for folder in os.environ.get("CADQUERY_LIBDIRS","").split(os.pathsep):
    if folder:sys.path.insert(0,folder)
for folder in (REPO/"R5_WORK/early_vendor",REPO/"R5_WORK/runtime_ready"):
    if folder.is_dir():sys.path.append(str(folder))
import cadquery as cq
from cad_io import leaves, bb

OLD=REPO/"AirTransformerShell/references/four-core-outdoor/V050_SM_M2_IN1_R1_OUTDOOR_SHEET_METAL_ONLY.stp"
HX=REPO/"AirTransformerShell/interfaces/four-core-horizontal-HX/FOUR_HX_INSTALLED.step"
if not HX.is_file():HX=ROOT/"inputs/FOUR_HX_INSTALLED.step"
assert hashlib.sha256(OLD.read_bytes()).hexdigest()=="d20fbdc7a29cf05dad60b861e0eac5a06509d531450b63370dea08928586f6ae"
assert hashlib.sha256(HX.read_bytes()).hexdigest()=="0360e579144f74aba14026e1d77f619e547365f2ee48cb3fdcd67370db4d271c"
WORK=ROOT/".work"
def records(path):
    data={}
    for pathkey,shape in leaves(path):
        fields=pathkey.split("/")
        name=next((k for k in reversed(fields) if k.endswith("_O")),fields[-2])
        if name in data: raise ValueError((path,name,pathkey))
        data[name]=shape
    return data

def cache(path,label):
    cache_dir=WORK/label
    cache_dir.mkdir(parents=True,exist_ok=True)
    index=cache_dir/"index.json"
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    if not index.exists() or json.loads(index.read_text())["sha"]!=sha:
        parts=records(path)
        rows={}
        for i,(name,s) in enumerate(parts.items()):
            f=f"{i}.brep";s.exportBrep(str(cache_dir/f));rows[name]=[f,bb(s)]
        index.write_text(json.dumps(dict(sha=sha,rows=rows)))
    return cache_dir,json.loads(index.read_text())["rows"]

def save_json(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding="utf-8")
def table(path,rows):
    with path.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=="__main__":
    folder,rows=cache(OLD,"old")
    for n,(f,b) in rows.items():
        if ("DAMPER" in n or "PORT_LAND" in n or "POST" in n) and ("_A_" in n or "POST" in n):
            print(n, " ".join(f"{x:.2f}" for x in b))
