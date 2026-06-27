import numpy as np
from plasmapy.simulation.particle_integrators import BorisIntegrator

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # <-- Missing import

# Create the figure and a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(projection='3d') #


B = np.array([[-5.0e-9, -5e-7, 0]])
E = np.array([[0.0, 0.0, 0.0]])
x_t0 = np.array([[0.0, 0.0, 0.0]])
v_t0 = np.array([[500, 500000.0, 0.0]])
xs, ys, zs = [], [], []

for n in range(200):

    x_t0, v_t0 = BorisIntegrator.push(x=x_t0, v=v_t0, B=B, E=E, q=-1.6e-19, m=9.1e-31, dt=1e-6)
    print(x_t0)
    xs.append(x_t0[0,0])
    ys.append(x_t0[0,1])
    zs.append(x_t0[0,2])

# Plot the data
ax.plot3D(xs, ys, zs, 'gray')
ax.scatter3D(xs, ys, zs, c=zs, cmap='Greens')

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 100)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


# This opens the interactive window where you can left-click and drag to rotate
plt.show() 
