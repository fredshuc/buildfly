"""Four gasket carriers with independent core datums and opposed frame clamps.

No core transform is changed. Dimensions remain candidates until the HX owner
accepts the calculated clamp reactions and the complete assembly is checked.
"""
from common import *

def add_face_seals(d):
    rows=[]
    for bed,dy in [('A',0),('B',865)]:
      for stage,dz in [('LOWER',0),('UPPER',335)]:
        tag=bed+'_'+stage;p='C11_'+tag+'_FACE';st='L' if stage=='LOWER' else 'U'
        z=620+dz; top=z-4.45; bottom=top-2
        y0=-758.5+dy;y1=-106.5+dy
        x0,x1=-430.,610.;ox0,ox1=-472.,659.;oy0,oy1=y0-22,y1+22
        # 12 mm gasket centred on the actual 20 mm frame land, with 4 mm
        # outer margin for positive stops. Narrow strips stay on a carrier
        # liner during knife cutting and assembly (no unsupported die cutting).
        gasket=ring_xy(x0+4,y0+4,x1-4,y1-4,top,z,12)
        d.remove(f'C09_FACE_GASKET_{tag}','Replace 2 mm strip with selected 6.35 mm closed-cell sponge; core remains at original Z')
        d.add(p+'_GASKET_INSTALLED',gasket,'Norseal R10480S closed-cell silicone sponge; selected 6.35 +/-0.10 mm','Installed4.45 mm; qualified cold/hot gap4.20..4.70 gives24.8..34.9% compression; single bonded scarf joint on outboard Y edge')
        carrier=ring_xy(ox0,oy0,ox1,oy1,bottom,top,42)
        # The X-positive outer margin is deliberately wider for a clamp clear
        # of the return bend. Keep the central air aperture exactly unchanged.
        carrier=box(ox0,oy0,bottom,ox1,oy1,top).cut(box(x0+20,y0+20,bottom-1,x1-20,y1-20,top+1))
        adapter=box(ox0,oy0,top,ox1,oy1,z-2).cut(box(ox0+10,oy0+10,top-1,ox1-10,oy1-10,z))
        for half in ['MIN','MAX']:
            n=f'HX_MASK_{bed}_{st}_{half}_O'
            mask=d.parts[n].cut(box(ox0,oy0,z-10,ox1,oy1,z+10)).clean()
            d.replace(n,mask,'Existing 1.5 mm sheet','Open perimeter for lowered seal carrier; original outer mask attachment plane retained; continuous seal weld to adapter')
        # Positive three-point supports are separate from the compressible seal.
        # Pads are machined/shimmed to the frozen loaded datum. No silicone is
        # in the gravity load path. Each pad is welded to its existing RHS rail.
        supports=[(-464,-424,y0-12,y0+3.5,-440,-426,y0+.5,y0+3.5,'FIX_XY'),
                  (490,530,y0-12,y0+3.5,500,520,y0+.5,y0+3.5,'SLIDE_X'),
                  (490,530,y1-3.5,y1+12,500,520,y1-3.5,y1-.5,'GUIDE_Y_SLIDE_X')]
        for i,(a,b,c,e,fa,fb,fc,fe,datum) in enumerate(supports,1):
            base=box(a,c,z-8,b,e,z-6)
            finger=box(fa,fc,z-6,fb,fe,z)
            pad=base.fuse(finger).clean()
            # This is an explicit support aperture, outside the gasket loop,
            # sealed by a continuous carrier-to-pad seam, not a collision fix.
            carrier=carrier.cut(pad);adapter=adapter.cut(pad)
            d.add(p+f'_DATUM_SUPPORT_{i}',pad,'S235JR machined support block','Three-point bearing; base weld to RHS. Final loaded bearingZ='+str(z)+' +/-0.05; '+datum+'; seam to carrier seals support aperture')
        # Datum stops contact frame edges, never the copper or fins. The remote
        # guide restrains Y while retaining >=1.5 mm X travel each direction.
        locators=[('LOCATOR_X',box(-443,y0-12,z-6,-440,y0+3.5,z+6),'Fixed X at actual HX corner post edge X=-440;15.5mm root width'),
                  ('LOCATOR_Y',box(-440,y0-5,z-6,-426,y0,z+6),'Fixed Y at same datum corner;5mm thick'),
                  ('GUIDE_Y',box(500,y0-5,z-6,520,y0,z+6),'Remote guide on SAME Y edge; X unrestricted +/-1.5mm, opposite Y edge free for thermal growth')]
        for suffix,s,reason in locators:
            carrier=carrier.cut(s);adapter=adapter.cut(s)
            d.add(p+'_'+suffix,s,'S235JR machined stop',reason+'; welded foot on datum support, sealed through carrier')
        # 18 mm downturned reinforcement, outside the clear air aperture.
        # Predefined notches clear the two unchanged RHS rails by 0.5 mm.
        stiff=[box(x0+18,y0+20,bottom-18,x0+20,y1-20,bottom),
               box(x1-20,y0+20,bottom-18,x1-18,y1-20,bottom)]
        for y in (y0+18,y1-20):
            beam=box(x0+20,y,bottom-18,x1-20,y+2,bottom)
            for xa,xb in [(-464,-424),(490,530)]:
                beam=beam.cut(box(xa-.5,y-1,z-40,xb+.5,y+3,z-7.5))
            stiff.append(beam.clean())
        for i,s in enumerate(stiff,1):d.add(p+f'_STIFFENER_{i}',s,'S235JR strip 2.0 x18','Continuous welded inner skirt; notches at rail crossings, no reduction of nominal air aperture')
        # The collector prevents intermediate X-edge clamps. Support the
        # Shell seal carrier continuously on the existing left RHS, and add
        # an outboard closed-section strongback to the other long edge.
        # This does not establish the separate HX frame uplift capacity.
        shim=box(-464,y0+3.5,z-8,-424,y1-3.5,bottom)
        d.add(p+'_LEFT_CONTINUOUS_BEARING',shim,'S235JR ground strip nominal1.55','Continuous carrier bearing on unchanged left RHS; select/grind thickness to actual loaded datum; qualified edge attachment; no raising core')
        beam=box(617.5,y0-5,bottom-50,647.5,y1+5,bottom).cut(box(620.5,y0-6,bottom-47,644.5,y1+6,bottom-3))
        d.add(p+'_RIGHT_CARRIER_STRONGBACK',beam,'S235JR RHS50Zx30Xx3','Continuous a3 upper seams to carrier;635mm clamp span screen; remains outside clear air aperture and distribution frame; HX frame capacity remains separate HOLD')
        if stage=='LOWER':
            host='AIR_PROCESS_OUT_CHANNEL_'+bed+'_O'
            aperture=box(617.5,y0-5,bottom-50,647.5,y1+5,bottom)
            before=d.parts[host];after=before.cut(aperture).clean()
            d.replace(host,after,'Existing formed air sheet','Registered30x50 closed RHS carrier penetration; beam ends capped and continuous qualified sheet-to-RHS seal weld around crossing. Local outlet flow obstruction requires pressure-loss review; no structural post cut.')
            d.interfaces.append({'id':p+'_STRONGBACK_DUCT_JOINT','host':host,'removed_sheet_mm3':before.Volume()-after.Volume(),'seal':'Continuous sheet-to-closed-RHS seam; caps seal hollow section; leak proof required','flow':'Outside frozen core aperture; local outlet-channel obstruction not assigned zero pressure loss'})
        for end,a,b in [('MIN',y0-5,y0-2),('MAX',y1+2,y1+5)]:
            d.add(p+'_RIGHT_STRONGBACK_CAP_'+end,box(620.5,a,bottom-47,644.5,b,bottom-3),'S235JR plate3','Recessed end cap; continuous seal weld before coating')
        # Distributed opposed clamps close the load locally through the 8 mm
        # steel land and carrier. They do not press on fins or thin water parts.
        stations=[]
        for x in [-350,-230,-110,10,130,250,370,550]:
            stations.extend([(x,y0-10,'YMIN'),(x,y1+10,'YMAX')])
        # All reactions are at the bottom frame. Upper-corner long ties were
        # rejected by the continuous D05 sweep, despite clear endpoint poses.
        stations.extend([(-410,y0-10,'YMIN_LEFT'),(645,y0+100,'XMAX'),(-418,y1+10,'YMAX'),(645,y1-100,'XMAX')])
        for i,(x,y,side) in enumerate(stations,1):
            contact_z=z+8;thin=side=='YMIN_LEFT';jaw_t=3.5 if thin else 8
            post=cyl(5,contact_z-top,(x,y,top),(0,0,1)).cut(cyl(2.1,10,(x,y,top),(0,0,1)),cyl(2.6,contact_z-top-10+1,(x,y,top+10),(0,0,1)))
            adapter=adapter.cut(cyl(5,4,(x,y,top),(0,0,1)))
            if thin:jaw=box(x-20,y-7,contact_z,x+20,y0+5,contact_z+jaw_t);stop=box(x-6,y0+.5,top,x+6,y0+3.5,z)
            elif side=='YMIN':jaw=box(x-12,y-7,z+8,x+12,y0+10,z+16);stop=box(x-6,y0+.5,top,x+6,y0+3.5,z)
            elif side=='YMAX':jaw=box(x-12,y1-10,z+8,x+12,y+7,z+16);stop=box(x-6,y1-3.5,top,x+6,y1-.5,z)
            else:jaw=box(x1-10,y-12,z+8,x+7,y+12,z+16);stop=box(x1-3.5,y-6,top,x1-.5,y+6,z)
            jaw=jaw.cut(cyl(2.75,jaw_t+2,(x,y,contact_z-1),(0,0,1)))
            if side=='YMAX' or thin:jaw=jaw.cut(cq.Solid.makeCone(2.5,5,2.5,cq.Vector(x,y,contact_z+jaw_t-2.5),cq.Vector(0,0,1)))
            engagement=6.05 if thin else 7.55;tipgap=3.95 if thin else 2.45
            d.add(p+f'_STOP_{i:02}',stop,'S235JR ground spacer','4.45 +/-0.05 mm stop; welded to carrier outside gasket. Verify complete gap budget after welding')
            d.add(p+f'_STANDOFF_{i:02}',post,'S235JR machined M5 reaction sleeve',f'OD10; height{contact_z-top}mm; lower10mm M5 tap withD4.2 minor, upperD5.2 clearance. Tap from lower end before sealed attachment. Screw engagement{engagement}mm, tip gap{tipgap}mm; proof1.5kN. All clamps react on bottom frame.')
            d.add(p+f'_CLAMP_{i:02}',jaw,'S235JR plate '+str(jaw_t),'Opposed bottom frame-land clamp; M5 clearance5.5; max500N,0.50Nm; thin left YMIN jaw40mm wide with15mm maximum toe arm; qualify local plate/contact behaviour',
                  {'kind':'flat_Z','thickness_mm':jaw_t,'R_inside_mm':0,'K':None,'datum':f'HX steel contact top Z={contact_z};'+('top90deg countersinkD10 flushM5 head' if side=='YMAX' or thin else 'socket head'), 'tolerance':'profile +/-0.2; hole +/-0.1; underside flatness0.05'})
            bolt=cyl(2.5,contact_z+8-(z-2),(x,y,z-2),(0,0,1)).fuse(cyl(4.25,5,(x,y,contact_z+8),(0,0,1)))
            # Socket representation is a real axial recess, not a solid head.
            bolt=bolt.cut(cyl(2,3,(x,y,contact_z+10),(0,0,1)))
            if side=='YMAX':bolt=cyl(2.5,15.5,(x,y,z-2),(0,0,1)).fuse(cq.Solid.makeCone(2.5,5,2.5,cq.Vector(x,y,z+13.5),cq.Vector(0,0,1))).cut(cyl(1.8,2,(x,y,z+14),(0,0,1)))
            if thin:bolt=cyl(2.5,9.5,(x,y,z-.5),(0,0,1)).fuse(cq.Solid.makeCone(2.5,5,2.5,cq.Vector(x,y,z+9),cq.Vector(0,0,1))).cut(cyl(1.8,2,(x,y,z+9.5),(0,0,1)))
            d.add(p+f'_SCREW_{i:02}',bolt,'M5 class8.8 '+('12mm overall90deg countersunk screw' if thin else '18mm overall90deg countersunk screw' if side=='YMAX' else '18mm underhead socket screw'),'0.50Nm dry;333..500N; selected flush heads clear H02 collector. Verify supplied head geometry, engagement and proof. No load release before HX frame acceptance.')
            d.contact(p+f'_SCREW_{i:02}',p+f'_STANDOFF_{i:02}',f'M5 nominal thread engagement in lower10mm tap;{engagement}mm actual engagement;1.5kN axial proof required')
            if i in (17,19):
                ya,yb=(y0-20,y0+10) if i==17 else (y1-10,y1+20)
                d.add(p+f'_LEFT_END_MOUNT_{i}',box(-424,ya,z-28.5,-421,yb,z-12.5),'S235JR plate3','30x16 mounting plate on unchanged left RHS sideX-424; perimeter a3 weld, effective horizontal24/vertical10mm; local RHS wall and complete bracket1.5kN proof required. Verify real stock corner/weld access; no frame cut.',{'kind':'flat_X','thickness_mm':3,'R_inside_mm':0,'K':None,'datum':'back face X=-424; centred within25mm RHS side height','tolerance':'profile+/-0.2; root fit per qualified WPS'})
                d.add(p+f'_LEFT_END_BEARING_{i}',box(-421,ya,bottom-8,-395,yb,bottom),'S235JR plate8','26x30 bearing extension supports carrier and left end clamp; weld to mount and two gussets; top flush to carrier underside; no load through skin or copper',{'kind':'flat_Z','thickness_mm':8,'R_inside_mm':0,'K':None,'datum':f'top Z={bottom}; root X=-421','tolerance':'bearing flatness0.05; selected height+/-0.05'})
                for j,yy in enumerate((ya,yb-3),1):
                    wire=cq.Wire.makePolygon([cq.Vector(-421,yy,bottom-8),cq.Vector(-395,yy,bottom-8),cq.Vector(-421,yy,bottom-20)],close=True)
                    d.add(p+f'_LEFT_END_GUSSET_{i}_{j}',cq.Solid.extrudeLinear(wire,[],cq.Vector(0,3,0)),'S235JR plate3','Right triangle26x12; double-sided a3 root welds to mount and shelf; effective root6mm each side; qualify thin-wall welds and proof complete bracket1.5kN',{'kind':'flat_Y','thickness_mm':3,'R_inside_mm':0,'K':None,'datum':f'Y={yy}; root X=-421','tolerance':'profile+/-0.2; root fit per qualified WPS'})
            rows.append({'core':tag,'clamp':i,'X_mm':x,'Y_mm':y,'datum_Z_mm':z,'frame_contact_Z_mm':contact_z,'reaction':'bottom Y-end frame on gusseted bearing extension' if i in (17,19) else 'bottom frame land','jaw_thickness_mm':jaw_t,'thread_engagement_mm':engagement,'seal_free_mm':6.35,'installed_mm':4.45,'gap_min_mm':4.20,'gap_max_mm':4.70,'force_design_max_N':500,'torque_Nm':.5,'HX_allowable_status':'NOT RELEASED; HX fixture1000N is not service allowance; long edge uplift/frame proof OPEN'})
        d.add(p+'_CARRIER',carrier.clean(),'S235JR plate 2.0','Lowered seal bed; inner skirt welded before flatness grinding; fixed core plane unchanged',
              {'kind':'flat_Z','thickness_mm':2,'R_inside_mm':0,'K':None,'datum':f'seal bed Z={top:.2f}','tolerance':'seal plane peak-to-valley0.10; stop heights +/-0.05'})
        d.add(p+'_MASK_ADAPTER',adapter.clean(),'S235JR ground plate 2.45','Continuous adapter between original mask plane and lowered seal carrier; weld and leak check around perimeter',
              {'kind':'flat_Z','thickness_mm':2.45,'R_inside_mm':0,'K':None,'datum':f'original mask top Z={z-2:.2f}','tolerance':'thickness +/-0.05; continuous air seal weld'})
        d.interfaces.append({'id':'IF-09_'+tag,'datum_Z_mm':z,'transform_changed':False,'gasket':'R10480S closed-cell,6.35selected+/-0.10,width12','gap_mm':[4.2,4.7],'supports':3,'clamps':len(stations),'clamp_force_acceptance':'HX force allowable pending; calculate from selected curve then submit whole loop','thermal_X_slide_mm':1.5})
    table(HERE/'C11_FACE_SEAL_AND_CLAMP_SCHEDULE.csv',rows)
