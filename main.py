import numpy as np
from model.quadcopter import Quadcopter
from plotter.quadplotter import QuadPlotter

def P_controller(quad, setpoint):
    """
    a very simple "P-only" controller
    """
    F = 6.3245 # ~total thrust needed to constrast the gravity
    K = 1.5
    diff = quad.position.z - setpoint
    F = K*diff
    T = F/4 + K*diff
    quad.set_thrust(T, T, T, T)

def lift_controller(quad):
    """
    make the quad lift vertically
    """
    F = 6.3245 # ~total thrust needed to constrast the gravity
    T = F/4
    T *= 1.1
    quad.set_thrust(T, T, T, T)

def yaw_controller(quad):
    """
    make the quad rotate
    """
    F = 6.3245 # ~total thrust needed to constrast the gravity
    T = F/4
    d = T*0.1
    quad.set_thrust(T-d, T+d, T-d, T+d)


def main():
    quad = Quadcopter()
    plotter = QuadPlotter()

    F = 6.3245 # total thrust needed to constrast the gravity
    quad.qr.z = -3
    dt = 0.01
    setpoint = -5
    plotter.add_marker((0, 0, -setpoint))
    for i in range(1000):
        quad.step(dt)
        P_controller(quad, setpoint=setpoint)
        #lift_controller(quad)
        #yaw_controller(quad)
        plotter.update(quad.position, quad.rpy)
        plotter.show_step()


if __name__ == '__main__':
    main()
