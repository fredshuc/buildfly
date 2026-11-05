"""Extract the exact public owner inputs needed to rerun C07. Run from a fresh checkout."""
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import gzip, hashlib, shutil
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
HX=ROOT/"HX/M101_D952_P254_220_39x6_C05"
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()
def unpack(archive,dest,prefix=""):
    with ZipFile(archive) as z:
        for member in z.infolist():
            name=PurePosixPath(member.filename)
            if member.is_dir() or not member.filename.startswith(prefix): continue
            if name.is_absolute() or ".." in name.parts or name.name.startswith("."): continue
            target=dest.joinpath(*name.parts)
            if not target.resolve().is_relative_to(dest.resolve()): raise ValueError(name)
            if target.exists():
                with z.open(member) as a:
                    if sha(target)!=hashlib.file_digest(a,"sha256").hexdigest():
                        raise ValueError(f"Local file differs from archive: {target}. Use a clean checkout.")
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(member) as a,target.open("xb") as f: shutil.copyfileobj(a,f)
def main():
    for directory,archive in (("AirTransformerShell/revisions/C06","C06_CAD_REVIEW_PACKAGE.zip"),
        ("dampers/c04-d01","D01_CAD_REVIEW_PACKAGE.zip"),("dampers/c06-d02","D02_CAD_REVIEW_PACKAGE.zip"),
        ("HX/"+HX.name,"M101_C05_RT2_CAD.zip")):
        dest=ROOT/directory;unpack(dest/archive,dest)
    unpack(ROOT/"hydronics/C06_RT2_HYD_R2/C06_HYD_RT2.zip",ROOT,"hydronics/C06_RT2_HYD_R2/")
    step=HX/(HX.name+".step")
    with gzip.open(str(step)+".gz","rb") as src:
        if step.exists():
            if sha(step)!=hashlib.file_digest(src,"sha256").hexdigest(): raise ValueError(step)
        else:
            with step.open("xb") as out:shutil.copyfileobj(src,out)
    print("Prepared C06, D01, D02, M101 C05 and HYD R2.")
if __name__=="__main__":
    main()
