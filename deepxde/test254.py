import os
os.environ["DDE_BACKEND"] = "pytorch"

import deepxde as dde
import numpy as np

# Viscosity
nu = 0.01

# Geometry: 2D square + time
geom = dde.geometry.Rectangle([-1, -1], [1, 1])
timedomain = dde.geometry.TimeDomain(0, 1)
geomtime = dde.geometry.GeometryXTime(geom, timedomain)


# PDE definition
def pde(x, u):
    u1 = u[:, 0:1]

    du_x = dde.grad.jacobian(u, x, i=0, j=0)
    du_y = dde.grad.jacobian(u, x, i=0, j=1)
    du_t = dde.grad.jacobian(u, x, i=0, j=2)

    du_xx = dde.grad.hessian(u, x, i=0, j=0)
    du_yy = dde.grad.hessian(u, x, i=0, j=1)

    return du_t + u1 * du_x + u1 * du_y - nu * (du_xx + du_yy)


# Initial condition
def initial_condition(x):
    return np.sin(np.pi * x[:, 0:1]) * np.sin(np.pi * x[:, 1:2])


ic = dde.IC(
    geomtime,
    initial_condition,
    lambda _, on_initial: on_initial,
)


bc = dde.DirichletBC(
    geomtime,
    lambda x: 0,
    lambda _, on_boundary: on_boundary,
)


data = dde.data.TimePDE(
    geomtime,
    pde,
    [bc, ic],
    num_domain=5000,
    num_boundary=400,
    num_initial=1000,
)


net = dde.nn.FNN(
    [3] + [128] * 5 + [1],
    "tanh",
    "Glorot normal"
)

model = dde.Model(data, net)

model.compile("adam", lr=1e-3)

losshistory, train_state = model.train(epochs=5000)


model.compile("L-BFGS")
model.train()


model.save("scary_pinn_model")

