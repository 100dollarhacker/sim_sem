import numpy as np
from plasmapy.simulation.particle_integrators import BorisIntegrator

B = np.array([[5.0e-8, 0.0, 0.0]])
E = np.array([[0.0, 0.0, 0.0]])
x_t0 = np.array([[0.0, 0.0, 0.0]])
v_t0 = np.array([[0.0, 0.0, 500.0]])
for n in range(100):
    x_t0, v_t0 = BorisIntegrator.push(x=x_t0, v=v_t0, B=B, E=E, q=-1.6e-19, m=9.1e-31, dt=1e-5)
    print(x_t0)
