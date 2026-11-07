"""Record the actual interpreter and imported package versions."""
from common import *
import importlib.metadata as md
names=['cadquery','cadquery-ocp','numpy','reportlab','pillow','pypdf']
versions={}
for n in names:
    try:versions[n]=md.version(n)
    except md.PackageNotFoundError:versions[n]='metadata unavailable; see module paths'
dump(E/'runtime_manifest.json',{'python':sys.version,'platform':sys.platform,'packages':versions,'cadquery_module':str(Path(cq.__file__).name),'cadquery_version':cq.__version__,'CADQUERY_LIBDIRS_role':'Optional existing library paths, not an input model. No external CAD cache is required for clean rebuild.','units':'mm,N,MPa unless otherwise stated'})
print(versions)
