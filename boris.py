import numpy as np
from plasmapy.simulation.particle_integrators import BorisIntegrator

B = np.array([[0.0, 0.0, 5.0]])
E = np.array([[0.0, 0.0, 0.0]])
x_t0 = np.array([[0.0, 0.0, 0.0]])
v_t0 = np.array([[5.0, 0.0, 0.0]])
for n in range(200):
    x_t0, v_t0 = BorisIntegrator.push(x=x_t0, v=v_t0, B=B, E=E, q=1.0, m=1.0, dt=0.01)
    print(x_t0)
