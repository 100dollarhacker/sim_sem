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

femm.ei_probdef('millimeters','axi',10**(-8),10**6,30);

# Draw the geometry --- 
# electrodes
femm.ei_drawrectangle(0,50,10,52);
femm.ei_drawrectangle(0,-50,10,-52);

# envirnment enclusure
# femm.ei_drawline(1,0,120,0);
# femm.ei_drawline(1,200,120,200);
# femm.ei_drawline(1,0,1,200);
# femm.ei_drawline(120,0,120,200);
femm.ei_makeABC()


# electrodes property
femm.ei_addmaterial('Iron',2500,2500,0);
femm.ei_addblocklabel(5,51)
femm.ei_selectlabel(5,51)
femm.ei_addblocklabel(5,-51)
femm.ei_selectlabel(5,-51)
femm.ei_setblockprop('Iron',0,1,0);
femm.ei_clearselected();


# env property
femm.ei_addmaterial('air',1,1,0);
femm.ei_addblocklabel(50,10);
femm.ei_selectlabel(50,10);
femm.ei_setblockprop('air',0,1,0);
femm.ei_clearselected();

# Add a "Conductor Property" for each of the strips
femm.ei_addconductorprop('v0',-2000,0,1);
femm.ei_addconductorprop('v1',2000,0,1);

# Apply voltage v0 (+2000) on one of the electrodes
femm.ei_selectsegment(0,51);
femm.ei_selectsegment(10,51);
femm.ei_selectsegment(5,52);
femm.ei_selectsegment(5,50);
femm.ei_setsegmentprop('<None>',0.25,0,0,0,'v0');
femm.ei_clearselected()

# Assign the "v1" voltage on the other electorde
femm.ei_selectsegment(0,-51);
femm.ei_selectsegment(10,-51);
femm.ei_selectsegment(5,-52);
femm.ei_selectsegment(5,-50);
femm.ei_setsegmentprop('<None>',0.25,0,0,0,'v1');
femm.ei_clearselected()


femm.ei_zoomnatural();

# Save the geometry to disk so we can analyze it
femm.ei_saveas('./trash/strips.fee');

femm.ei_analyze();
femm.ei_loadsolution()

#
# ELECTIC PART END ---- back to magnetic part

# femm.mi_setfocus('./trash/coil.fem')


# # Add use less line
# for n in range(0,10):
# 	femm.mi_addnode(-n*5,-n*5)
# 	femm.mi_addnode(-(n+1)*5,-(n+1)*5)
# 	femm.mi_addsegment(-n*5,-n*5,-(n+1)*5,-(n+1)*5)


# # If we were5afda6c79c86f819a9404f702ebb16d09986eb2cq interested in the flux density at specific positions, 
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
# # zee=[]
# # bee=[]

eM =  9.1e-31
eQ = -1.6e-19

# start position
pos = (2,50)
v = (0,0)
a = (0,0)
t = 1e-8



for n in range(-10,10):
	# b=femm.mo_getb(0,n);
	# ma01,Bx,By,ma04,ma05,ma06,ma07,ma08,ma09,ma10,ma11,ma12,ma13,ma14 = femm.mo_getpointvalues(2,n);
	# _,Bx,By,_,_,_,_,_,_,_,_,_,_,_ = femm.mo_getpointvalues(2,n)
	_,_,_,Ex,Ey,_,_,_             = femm.eo_getpointvalues(pos[0],pos[1])
	# zee.append(n)
	# bee.append(b[1]);
	
	# print('Pos v(%g,%g) a(%g,%g) ' % (v[0], v[1], a[0], a[1]))
	v = (v[0] + a[0]*t,v[1] + a[1]*t)
	pos = (pos[0] + v[0]*t + a[0]*t*t/2,pos[1] + v[1]*t + a[1]*t*t/2)

	# v = (v_n[0], v_n[1])
	a = (Ex*eQ/eM,Ey*eQ/eM) # ma = F = E*q  ==> a = E*q/m
	print('Pos @ n:%g x:%g y:%g', n, pos[0], pos[1])	




	# print('At pos (2,%d)  Bx:%g By:%g Ex:%g Ey:%g' % (n, Bx, By, Ex, Ey))

# TODO:: Add this here as V x B = F 
# import numpy as np
# a = np.array([1,0,0])  
# b = np.array([0,1,0])  
# #print the result    
# print(np.cross(a,b))

# plt.plot(zee,bee)
# plt.ylabel('Flux Density, Tesla')
# plt.xlabel('Distance along the z-axis, mm')
# plt.title('Plot of flux density along the axis')
# plt.show()

femm.prompt('Press <ENTER> to continue')

# When the analysis is completed, FEMM can be shut down.
femm.closefemm()


