# Wound Copper Coil with an Iron Core
# David Meeker
# dmeeker@ieee.org
#  
# This program consider an axisymmetric magnetostatic problem
# of a cylindrical coil with an axial length of 100 mm, an
# inner radius of 50 mm, and an outer radius of 100 mm.  The
# coil has 200 turns and the coil current is 20 Amps. There is
# an iron bar 80 mm long with a radius of 10 mm centered co-
# axially with the coil.  The objective of the analysis is to
# determine the flux density at the center of the iron bar,
# and to plot the field along the r=0 axis. This analysis
# defines a nonlinear B-H curve for the iron and employs an
# asymptotic boundary condition to approximate an "open"
# boundary condition on the edge of the solution domain.
  
import femm
import matplotlib.pyplot as plt

# The package must be initialized with the openfemm command.
femm.openfemm();

# # We need to create a new Magnetostatics document to work on.
# femm.newdocument(0);

# # Define the problem type.  Magnetostatic; Units of mm; Axisymmetric; 
# # Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
# # the depth dimension, and an angle constraint of 30 degrees
# femm.mi_probdef(0, 'millimeters', 'axi', 1.e-8, 0, 30);
# #femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, 0, 30);

# # Draw a rectangle for the steel bar on the axis;
# # femm.mi_drawrectangle(0, -10, 10, 10);

# # Draw a rectangle for the coil;
# femm.mi_drawrectangle(50, -50, 100, 50);

# # Define an "open" boundary condition using the built-in function:
# femm.mi_makeABC()

# # Add block labels, one to each the steel, coil, and air regions.
# # femm.mi_addblocklabel(5,0);
# femm.mi_addblocklabel(75,0);
# femm.mi_addblocklabel(30,100);

# # Add some block labels materials properties
# femm.mi_addmaterial('Air', 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0);
# femm.mi_addmaterial('Coil', 1, 1, 0, 0, 58*0.65, 0, 0, 1, 0, 0, 0);
# # femm.mi_addmaterial('LinearIron', 2100, 2100, 0, 0, 0, 0, 0, 1, 0, 0, 0);

# # A more interesting material to add is the iron with a nonlinear
# # BH curve.  First, we create a material in the same way as if we 
# # were creating a linear material, except the values used for 
# # permeability are merely placeholders.

# # femm.mi_addmaterial('Iron', 2100, 2100, 0, 0, 0, 0, 0, 1, 0, 0, 0);

# # A set of points defining the BH curve is then specified.
# # bdata = [ 0.,0.3,0.8,1.12,1.32,1.46,1.54,1.62,1.74,1.87,1.99,2.046,2.08]; 
# # hdata = [ 0, 40, 80, 160, 318, 796, 1590, 3380, 7960, 15900, 31800, 55100, 79600];
# # for n in range(0,len(bdata)):
# # 	femm.mi_addbhpoint('Iron', bdata[n],hdata[n]);

# # Add a "circuit property" so that we can calculate the properties of the
# # coil as seen from the terminals.
# femm.mi_addcircprop('icoil', 20, 0);

# # Apply the materials to the appropriate block labels
# # femm.mi_selectlabel(5,0);
# # femm.mi_setblockprop('Iron', 0, 1, '<None>', 0, 0, 0);
# # femm.mi_clearselected()

# femm.mi_selectlabel(75,0);
# femm.mi_setblockprop('Coil', 0, 1, 'icoil', 0, 0, 200);
# femm.mi_clearselected()

# femm.mi_selectlabel(30,100);
# femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0);
# femm.mi_clearselected()


# # Now, the finished input geometry can be displayed.
# femm.mi_zoomnatural()

# # We have to give the geometry a name before we can analyze it.
# femm.mi_saveas('./trash/coil.fem');


# # Now,analyze the problem and load the solution when the analysis is finished
# femm.mi_analyze()
# femm.mi_loadsolution()

# ELECTRIC PART ------------


# Create a new electrostatics problem
femm.newdocument(1)

# Draw the geometry
femm.ei_probdef('millimeters','planar',10**(-8),10**6,30);
# femm.ei_probdef('millimeters','axi',10**(-8),10**6,30);
femm.ei_drawrectangle(2,0,22,2);
femm.ei_drawrectangle(2+24,0,22+24,2);
femm.ei_drawrectangle(-2,0,-22,2);
femm.ei_drawrectangle(-2-24,0,-22-24,2);
femm.ei_drawrectangle(-100,-20,100,0);
femm.ei_drawline(-120,-20,120,-20);
femm.ei_drawarc(120,-20,-120,-20,180,2.5);
# femm.ei_drawarc(100,100,120,100,180,2.5);
# femm.ei_drawline(100,100,120,100);

# Create and assign a "periodic" boundary condition to 
# model an unbounded problem via the Kelvin Transformation
# femm.ei_addboundprop('periodic',0,0,0,0,3);
# femm.ei_selectarcsegment(0,100);
# femm.ei_selectarcsegment(110,80);
# femm.ei_setarcsegmentprop(2.5,'periodic',0,0,'<none>');
# femm.ei_clearselected();

# Define the ground plane in both the geometry and the exterior region
femm.ei_addboundprop('ground',0,0,0,0,0);
femm.ei_selectsegment(0,-20);
femm.ei_selectsegment(110,-20);
femm.ei_selectsegment(-110,-20);
femm.ei_selectsegment(110,100);
femm.ei_setsegmentprop('ground',0,1,0,0,'<none>');
femm.ei_clearselected();

# Add block labels for each strip and mark them with "No Mesh"
for k in range(0,4):
	femm.ei_addblocklabel(-36+k*24,1)
for k in range(0,4):
	femm.ei_selectlabel(-36+k*24,1)
femm.ei_setblockprop('<No Mesh>',0,1,0);
femm.ei_clearselected();

# Add and assign the block labels for the air and dielectric regions
femm.ei_addmaterial('air',1,1,0);
femm.ei_addmaterial('dielectric',4,4,0);
femm.ei_addblocklabel(0,-10);
femm.ei_addblocklabel(0,50);
femm.ei_addblocklabel(110,95);
femm.ei_selectlabel(0,-10);
femm.ei_setblockprop('dielectric',0,1,0);
femm.ei_clearselected();
femm.ei_selectlabel(0,50);
femm.ei_selectlabel(110,95);
femm.ei_setblockprop('air',0,1,0);
femm.ei_clearselected();

# Add a "Conductor Property" for each of the strips
femm.ei_addconductorprop('v0',2000,0,1);
femm.ei_addconductorprop('v1',-2000,0,1);
# femm.ei_addconductorprop('v2',0,0,1);
# femm.ei_addconductorprop('v3',0,0,1);

# Assign the "v0" properties to all sides of the first strip
femm.ei_selectsegment(-46,1);
femm.ei_selectsegment(-26,1);
femm.ei_selectsegment(-36,2);
femm.ei_selectsegment(-36,0);
femm.ei_setsegmentprop('<None>',0.25,0,0,0,'v0');
femm.ei_clearselected()

# Assign the "v1" properties to all sides of the second strip
femm.ei_selectsegment(-46+24,1);
femm.ei_selectsegment(-26+24,1);
femm.ei_selectsegment(-36+24,2);
femm.ei_selectsegment(-36+24,0);
femm.ei_setsegmentprop('<None>',0.25,0,0,0,'v1');
femm.ei_clearselected()

# # Assign the "v2" properties to all sides of the third strip
# femm.ei_selectsegment(-46+2*24,1);
# femm.ei_selectsegment(-26+2*24,1);
# femm.ei_selectsegment(-36+2*24,2);
# femm.ei_selectsegment(-36+2*24,0);
# femm.ei_setsegmentprop('<None>',0.25,0,0,0,'v2');
# femm.ei_clearselected()

# # Assign the "v3" properties to all sides of the fourth strip
# femm.ei_selectsegment(-46+3*24,1);
# femm.ei_selectsegment(-26+3*24,1);
# femm.ei_selectsegment(-36+3*24,2);
# femm.ei_selectsegment(-36+3*24,0);
# femm.ei_setsegmentprop('<None>',0.25,0,0,0,'v3');
# femm.ei_clearselected()

femm.ei_zoomnatural();

# Save the geometry to disk so we can analyze it
femm.ei_saveas('./trash/strips.fee');

# Create a placeholder matrix which we will fill with capacitance values
c=[]
 
# for k in range(0,4):
# femm.ei_modifyconductorprop('v0',1,1000);
# femm.ei_modifyconductorprop('v1',1,-1000);
# femm.ei_modifyconductorprop('v2',1,1 if (k==2) else 0);
# femm.ei_modifyconductorprop('v3',1,1 if (k==3) else 0);
femm.ei_analyze();
femm.ei_loadsolution()
# c.append([femm.eo_getconductorproperties('v0')[1],femm.eo_getconductorproperties('v1')[1],femm.eo_getconductorproperties('v2')[1], femm.eo_getconductorproperties('v3')[1]])

#
# ELECTIC PART END ---- back to magnetic part

# femm.mi_setfocus('./trash/coil.fem')


# # Add use less line
# for n in range(0,10):
# 	femm.mi_addnode(-n*5,-n*5)
# 	femm.mi_addnode(-(n+1)*5,-(n+1)*5)
# 	femm.mi_addsegment(-n*5,-n*5,-(n+1)*5,-(n+1)*5)


# # If we were interested in the flux density at specific positions, 
# # we could inquire at specific points directly:
# b0=femm.mo_getb(0,0);
# print('Flux density at the center of the bar is %g T' % b0[1]);
# b1=femm.mo_getb(0,50);
# print('Flux density at r=0,z=50 is %g T' % b1[1]);

# # The program will report the terminal properties of the circuit:
# # current, voltage, and flux linkage 
# vals = femm.mo_getcircuitproperties('icoil');

# # # [i, v, \[Phi]] = MOGetCircuitProperties["icoil"]

# # # If we were interested in inductance, it could be obtained by
# # # dividing flux linkage by current
# # L = 1000*vals[2]/vals[0];
# # print('The self-inductance of the coil is %g mH' % L);

# # # Or we could, for example, plot the results along a line using 
# zee=[]
# bee=[]
# for n in range(-10,10):
# 	b=femm.mo_getb(0,n);
# 	# ma01,Bx,By,ma04,ma05,ma06,ma07,ma08,ma09,ma10,ma11,ma12,ma13,ma14 = femm.mo_getpointvalues(2,n);
# 	_,Bx,By,_,_,_,_,_,_,_,_,_,_,_ = femm.mo_getpointvalues(2,n);
# 	zee.append(n)
# 	bee.append(b[1]);
# 	print('At pos %d  B is %g Bx:%g By:%g' % (n,b[1],Bx,By))

# # TODO:: Add this here as V x B = F 
# # import numpy as np
# # a = np.array([1,0,0])  
# # b = np.array([0,1,0])  
# # #print the result    
# # print(np.cross(a,b))

# # plt.plot(zee,bee)
# # plt.ylabel('Flux Density, Tesla')
# # plt.xlabel('Distance along the z-axis, mm')
# # plt.title('Plot of flux density along the axis')
# # plt.show()

femm.prompt('Press <ENTER> to continue')

# When the analysis is completed, FEMM can be shut down.
femm.closefemm()


