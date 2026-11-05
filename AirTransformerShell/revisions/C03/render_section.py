"""Draw from the section stations used by the CAD builder."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,Circle,Patch
root=Path(__file__).parent
data=json.loads((root/"verification.json").read_text())
fig,(side,front)=plt.subplots(1,2,figsize=(13,6.8),gridspec_kw={"width_ratios":[1,1.34]})
fig.subplots_adjust(top=.83,bottom=.19,wspace=.23)
fig.suptitle("AirTransformer  |  Vertical-core air ducts",fontsize=21,x=.075,ha="left",y=.97)
colors={"P":"#8cc9e5","R":"#f4b37b","COMMON":"#a5cfc7"}
for ax in (side,front):
 ax.set_aspect("equal");ax.spines[["top","right"]].set_visible(False);ax.tick_params(labelsize=8);ax.set_ylabel("Z  [mm]")
for a,b in zip(data["air_sections"][::2],data["air_sections"][1::2]):
 if not a["segment"].startswith("A_"):continue
 tag=a["segment"].split("_")[-1]
 pts=[(a["x"],a["z_min"]),(b["x"],b["z_min"]),(b["x"],b["z_max"]),(a["x"],a["z_max"])]
 side.add_patch(Polygon(pts,fc=colors[tag],ec="#2e4553",lw=1))
for x in (-182,750):
 for z,h,tag in [(300,345,"P"),(940,180,"R")]:
  side.add_patch(Rectangle((x,z-38),180,h+76,fc=colors[tag],ec="#465b68",ls="--",alpha=.52))
  side.text(x+90,z+h/2,tag,ha="center",va="center",weight="bold")
side.add_patch(Rectangle((296.65,204),152,1000,fc="#d8c599",ec="#726544",hatch="////"))
side.text(372,710,"HX C04",ha="center",va="center",rotation=90,bbox=dict(fc="white",ec="none"))
side.set(xlim=(-225,990),ylim=(120,1330),xlabel="X  [mm]",title="Single bed  /  X–Z section")
for ty,label in [(-802.175,"A"),(37.825,"B")]:
 cy=ty+367.775
 front.add_patch(Rectangle((cy-306,204),612,1000,fc="#ede5d4",ec="#75694a"))
 front.text(cy,1230,"HX "+label,ha="center",fontsize=10)
 for p in data["damper_ports"]:
  if p["bed"]!=label or p["face"]!="R":continue
  front.add_patch(Rectangle((float(p["opening_y_mm"]),float(p["opening_z_mm"])),630,float(p["height_mm"]),fc=colors[p["circuit"]],ec="#354956",alpha=.78))
 for y in (ty+576.85,ty+726.85):front.add_patch(Circle((y,1370),55,fc="white",ec="#37567a",lw=1.5))
front.set(xlim=(-895,895),ylim=(120,1530),xlabel="Y  [mm]",title="+X bulkhead  /  projected openings")
fig.legend(handles=[Patch(color=colors["P"],label="Process branch"),Patch(color=colors["R"],label="Regeneration branch"),Patch(color=colors["COMMON"],label="Shared bed plenum"),Patch(fc="#ede5d4",label="Active face  612 × 1000")],loc="lower center",bbox_to_anchor=(.5,.07),ncol=4,frameon=False)
fig.text(.075,.035,"SHELL C03   /   M101 C04     •     Dashed boxes: damper body reservations     •     Circles: Ø110 water penetrations",size=10)
fig.savefig(root/"C03_duct_sections.png",dpi=155)
