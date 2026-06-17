# Combination of Electrical and Magnetic simulation 
  
import femm
import matplotlib.pyplot as plt
import math


eM =  9.1e-31
eQ = -1.6e-19
THREAD_NUM = 10
SIMULATION_POINTS = 100
ANODE_LEVEL = -50 # This should be set automatically as part of Anode/Cathode creation
t = 1e-10  # simulation time interval



# The package must be initialized with the openfemm command.
femm.openfemm();

# We need to create a new Magnetostatics document to work on.
femm.newdocument(0);

# Define the problem type.  Magnetostatic; Units of mm; Axisymmetric; 
# Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
# the depth dimension, and an angle constraint of 30 degrees
femm.mi_probdef(0, 'millimeters', 'axi', 1.e-8, 0, 30);
#femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, 0, 30);

# Draw a rectangle for the steel bar on the axis;
# femm.mi_drawrectangle(0, -10, 10, 10);

# Add some block labels materials properties
femm.mi_addmaterial('Air', 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0);
femm.mi_addmaterial('Coil', 1, 1, 0, 0, 58*0.65, 0, 0, 1, 0, 0, 0);


def addCoil(x0,y0, x1,y1, deg, B,name, femm):
	print('Adding magnetic coil at (%g,%g)<>(%g,%g)' % (x0, y0, x1, y1))

	# Draw a rectangle for the coil;
	femm.mi_drawrectangle(x0, y0, x1, y1);

	femm.mi_addblocklabel((x0 + x1)/2,(y0 + y1)/2);


	# Add a "circuit property" so that we can calculate the properties of the
	# coil as seen from the terminals.
	femm.mi_addcircprop('icoil'+name, B, 0);
	
	femm.mi_selectlabel((x0 + x1)/2,(y0 + y1)/2);
	femm.mi_setblockprop('Coil', 0, 1, 'icoil'+name, deg, 0, 1);
	femm.mi_clearselected()

	


addCoil(10, 20, 15, 30, 180, -180 ,"-A", femm)
# addCoil(10, -60, 15, -50, 0, -500,"-B" , femm)
addCoil(5, -3, 15, 0, 180, 838,"-B" , femm)


# Define an "open" boundary condition using the built-in function:
femm.mi_makeABC()

# Add block labels, one to each the steel, coil, and air regions.
# femm.mi_addblocklabel(5,0);
femm.mi_addblocklabel(5,20);
femm.mi_selectlabel(5,20);
femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()


# Now, the finished input geometry can be displayed.
femm.mi_zoomnatural()

# We have to give the geometry a name before we can analyze it.
femm.mi_saveas('./trash/coil.fem');


# Now,analyze the problem and load the solution when the analysis is finished
femm.mi_analyze()
femm.mi_loadsolution()

# Nice, but I am not sure it's gives real values.
coilName = "-B"
vals = femm.mo_getcircuitproperties('icoil'+coilName);

# If we were interested in inductance, it could be obtained by
# dividing flux linkage by current
L = 1000*vals[2]/vals[0];
print('The self-inductance of the coil-%s is %g mH' % (coilName,L));


# ELECTRIC PART ------------


# Create a new electrostatics problem
femm.newdocument(1)

femm.ei_probdef('millimeters','axi',10**(-8),10**6,30);

femm.ei_addmaterial('Iron',2500,2500,0);

# def addCoil(x0,y0, x1,y1, deg, B,name, femm):

def addElectrode(x0, y0, x1, y1 , name , voltage, material, femm):

	femm.ei_drawrectangle(x0,y0,x1,y1)
	femm.ei_addblocklabel((x0 + x1)/2,(y0+y1)/2)
	femm.ei_selectlabel((x0 + x1)/2,(y0+y1)/2)
	femm.ei_setblockprop(material,0,1,0);
	femm.ei_clearselected();

	# Add a "Conductor Property" for each of the strips
	# femm.ei_addconductorprop('v0',-500,0,1);
	femm.ei_addconductorprop(name,voltage,0,1);

	# Apply voltage v0 (+2000) on one of the electrodes
	femm.ei_selectsegment(x0,(y1+y0)/2);
	femm.ei_selectsegment(x1,(y0+y1)/2);
	femm.ei_selectsegment((x0 + x1)/2,y1);
	femm.ei_selectsegment((x0 + x1)/2,y0);
	femm.ei_setsegmentprop('<None>',0.25,0,0,0,name);
	femm.ei_clearselected()

# Draw the geometry --- Electric
# electrodes
addElectrode(0,50,32,52,'v1', -500, 'Iron', femm)
addElectrode(0,-50,32,-52,'v0', 2500, 'Iron', femm)

femm.ei_makeABC()


# env property
femm.ei_addmaterial('air',1,1,0);
femm.ei_addblocklabel(50,10);
femm.ei_selectlabel(50,10);
femm.ei_setblockprop('air',0,1,0);
femm.ei_clearselected();


femm.ei_zoomnatural();

# Save the geometry to disk so we can analyze it
femm.ei_saveas('./trash/strips.fee');

femm.ei_analyze();
femm.ei_loadsolution()

#
# ELECTIC PART END ---- back to magnetic part



for i in range (0,THREAD_NUM): # t
	# start position
	pos = (0.01 + i/10,50-0.1,0)
	v = (0,0,0)
	a = (0,0,0)

	prev_pos = pos
	run = True

	for n in range(0,SIMULATION_POINTS):

		if not run:
			continue

		_,Bx,By,_,_,_,_,_,_,_,_,_,_,_ = femm.mo_getpointvalues(pos[0],pos[1])

		_,_,_,Ex,Ey,_,_,_             = femm.eo_getpointvalues(pos[0],pos[1])
		
		print('                                                   V/A v(%g,%g,%g) a(%g,%g,%g) ' % (v[0], v[1],v[2], a[0], a[1], a[2]))
		v = (v[0] + a[0]*t,v[1] + a[1]*t, v[2] + a[2] *t)
		# F = E*q =m * a ==> a = E* q / m

			
		a = (Ex*eQ/eM + v[2]*By*eQ/eM,Ey*eQ/eM + v[2]*Bx*eQ/eM, (v[1]*Bx + v[0]*By)*eQ/eM )



		pos_m = (pos[0]/1000 + v[0]*t + a[0]*t*t/2,pos[1]/1000 + v[1]*t + a[1]*t*t/2, pos[2]/1000 + v[2]*t + a[2]*t*t/2)
		
		#Mirror particles
		if pos_m[0] < 0:
			pos_m = (-pos_m[0],pos_m[1],pos_m[2])
			v = (-v[0],v[1],v[2])

		pos = (pos_m[0]*1000, pos_m[1]*1000, pos_m[2]*1000)



		# a = (Ex*eQ/eM,Ey*eQ/eM) # ma = F = E*q  ==> a = E*q/m
		print('Pos @ n:%g x:%g y:%g z:%g  %g,%g,%g' % (n, pos[0], pos[1], pos[2], prev_pos[0], prev_pos[1], prev_pos[2]))	

		if pos[1] < ANODE_LEVEL:
			run = False
			continue

		femm.ei_addnode(math.sqrt(pos[0]*pos[0]* + pos[2]*pos[2]),pos[1])
		femm.ei_addnode(math.sqrt(prev_pos[0]*prev_pos[0] + prev_pos[2]*prev_pos[2]),prev_pos[1])
		femm.ei_addsegment(math.sqrt(prev_pos[0]*prev_pos[0] + prev_pos[2]*prev_pos[2]),prev_pos[1],math.sqrt(pos[0]*pos[0]* + pos[2]*pos[2]),pos[1])

		femm.mi_addnode(pos[0],pos[1])
		femm.mi_addnode(prev_pos[0],prev_pos[1])
		femm.mi_addsegment(prev_pos[0],prev_pos[1],pos[0],pos[1])

		prev_pos = pos


femm.prompt('Press <ENTER> to continue')

# When the analysis is completed, FEMM can be shut down.
femm.closefemm()


