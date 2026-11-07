"""Review views from C10 STEP sections, not fabrication flat patterns."""
from common import *
from build import cache_host
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

def section(ax,shape,axis,value,color,linewidth=1.0):
    point=[0.,0.,0.];point[axis]=value
    normal=[0.,0.,0.];normal[axis]=1
    plane=cq.Face.makePlane(4500,4500,cq.Vector(*point),cq.Vector(*normal))
    part=shape.intersect(plane)
    for e in part.Edges():
        if e.Length()<1e-6:continue
        pts=[e.positionAt(t).toTuple() for t in np.linspace(0,1,2 if e.geomType()=='LINE' else 40)]
        axes=([1,2] if axis==0 else [0,2])
        ax.plot([p[axes[0]] for p in pts],[p[axes[1]] for p in pts],color=color,lw=linewidth)

def main():
    shell=named(CAD/'C10_SHELL.step');parent=cache_host('S1');old=parent['SHELL']
    crown=named(HYD/'W2_ADDITIONAL_INSULATION.step');budget=named(HYD/'W2_HOST_SPACE_REQUEST.step')
    fig,axes=plt.subplots(2,2,figsize=(14,9))
    fig.suptitle('C10 | H01 heat exchangers + D04 dampers + HYD-S2 water island',fontsize=17,weight='bold')
    ax=axes[0,0]
    for n,c in [('AIR_TOP_SPLITTER_A_O','#087e8b'),('AIR_SIDE_IN_A_O','#637381')]:
        section(ax,shell[n],1,-432.5 if 'TOP' in n else -45.75,c,1.2)
    section(ax,old['AIR_TOP_SPLITTER_A_O'],1,-432.5,'#b66336',1)
    ax.add_patch(Rectangle((-410,991.35),1000,152,facecolor='#d9e8ed',edgecolor='#809da9'))
    ax.text(70,1058,'Upper H01 fin window',ha='center',fontsize=10)
    ax.text(-440,1500,'Orange: C09 roof   Teal: C10 roof',fontsize=9)
    ax.annotate('Raised roof and closed inner cheek',xy=(570,1243.4),xytext=(-250,1460),arrowprops={'arrowstyle':'->'},fontsize=10)
    ax.set(xlim=(-500,780),ylim=(970,1525),title='A | Upper plenum section and cheek profile',xlabel='Global X / mm',ylabel='Global Z / mm')
    for col,bed,y in [(0,'A',-754),(1,'B',100)]:
        ax=axes[1,col]
        for n,s in shell.items():
            if (f'C10_{bed}_W2_POCKET' in n or n in [f'AIR_PROCESS_IN_FLOOR_{bed}_O',f'AIR_PROCESS_IN_WRAP_{bed}_O']):section(ax,s,1,y,'#087e8b',1.4)
        section(ax,old[f'AIR_PROCESS_IN_FLOOR_{bed}_O'],1,y,'#b66336',1)
        section(ax,parent['DAMPERS'][f'DAMPER_SEAT_{bed}_UPPER_DEEP_O'],1,y,'#637381',1.4)
        section(ax,crown[bed+'_W2_25mm_CROWN_ONLY'],1,y,'#d39631',1.2)
        section(ax,budget[bed+'_W2_25mm_PLUS_2mm_SPACE'],1,y,'#bdc2c6',.8)
        ax.set(xlim=(-605,-495),ylim=(1125,1185),title=f'{bed} | Closed insulation pocket at Y = {y} mm',xlabel='Global X / mm',ylabel='Global Z / mm')
        ax.text(-602,1180,'Roof underside 1168.5 | sheet 1.5',fontsize=9)
        ax.text(-602,1128,'Gold: insulation   Grey: installation space',fontsize=8)
    ax=axes[0,1]
    for n,s in shell.items():
        if n.startswith('C10_A_U_GLAND_RETAINER'):section(ax,s,0,-653.5,'#087e8b',1.2)
        if n.startswith('C10_A_U_GLAND_MEMBRANE'):section(ax,s,0,-651.5,'#d39631',.9)
        if n.startswith('C10_A_U_GLAND_NUT'):section(ax,s,0,-656,'#374957',.9)
    ax.set(xlim=(-780,-500),ylim=(810,980),title='A upper | Two-hole split gland, view along +X',xlabel='Global Y / mm',ylabel='Global Z / mm')
    ax.text(-775,972,'Skin Ø120/94 | retainers Ø126/100 | 6 × M4',fontsize=8)
    for ax in axes.flat:
        ax.set_aspect('equal');ax.grid(alpha=.14);ax.tick_params(labelsize=8)
    fig.text(.06,.018,'GEOMETRY REVIEW CANDIDATE — not a cutting, pressure or structural release. Actual component names and checks accompany the STEP.',fontsize=9,color='#804b36')
    fig.subplots_adjust(left=.07,right=.98,bottom=.09,top=.90,wspace=.20,hspace=.40)
    fig.savefig(HERE/'C10_STRUCTURE_REVIEW.png',dpi=160);plt.close(fig)
    print('Drawing exported',flush=True)
if __name__=='__main__':main()
