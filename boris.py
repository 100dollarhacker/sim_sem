import numpy as np
from plasmapy.simulation.particle_integrators import BorisIntegrator

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # <-- Missing import

# Create the figure and a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(projection='3d') #

# Generate dummy 3D data
z = np.linspace(0, 15, 100)
x = np.sin(z)
y = np.cos(z)

# Plot the data
#ax.plot3D(x, y, z, 'gray')
#ax.scatter3D(x, y, z, c=z, cmap='Greens')

# This opens the interactive window where you can left-click and drag to rotate
#plt.show() 

B = np.array([[5.0e-7, 0, 0.0]])
E = np.array([[0.0, 0.0, 0.0]])
x_t0 = np.array([[0.0, 0.0, 0.0]])
v_t0 = np.array([[100.0, 500000.0, 0.0]])
#updated_array = [x_t0]
xs, ys, zs = [], [], []

for n in range(200):
    x_t0, v_t0 = BorisIntegrator.push(x=x_t0, v=v_t0, B=B, E=E, q=-1.6e-19, m=9.1e-31, dt=1e-6)
    print(x_t0)
    #updated_array = np.append(updated_array, [x_t0], axis=0)
    xs.append(x_t0[0,0])
    ys.append(x_t0[0,1])
    zs.append(x_t0[0,2])

#adata = updated_array
#xp, yp, zp = data[:, 0], data[:, 1], data[:, 2]
#xp, yp, zp = data[0], data[1], data[2]


# Plot the data
ax.plot3D(xs, ys, zs, 'gray')
ax.scatter3D(xs, ys, zs, c=zs, cmap='Greens')


# This opens the interactive window where you can left-click and drag to rotate
plt.show() 
