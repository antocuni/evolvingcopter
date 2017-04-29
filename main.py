import numpy as np
from model.quadcopter import Quadcopter
from plotter.quadplotter import QuadPlotter

def P_controller(quad, setpoint):
    """
    a very simple "P-only" controller
    """
    F = 0.5 # PWM needed to contrast the gravity
    K = 0.1
    diff = setpoint - quad.position.z
    T = F + K*diff
    quad.set_thrust(T, T, T, T)

def lift_controller(quad):
    """
    make the quad lift vertically
    """
    T = 0.5 # PWM needed to contrast the gravity
    quad.set_thrust(T, T, T, T)

def yaw_controller(quad):
    """
    make the quad rotate
    """
    T = 0.5
    d = T*0.1
    quad.set_thrust(T-d, T+d, T-d, T+d)


def main():
    quad = Quadcopter()
    plotter = QuadPlotter()

    F = 6.3245 # total thrust needed to constrast the gravity
    quad.position = (0, 0, 3) # put it a bit above the ground
    dt = 0.01
    setpoint = 5
    plotter.add_marker((0, 0, setpoint))
    while plotter.show_step():
        P_controller(quad, setpoint=setpoint)
        #lift_controller(quad)
        #yaw_controller(quad)
        quad.step(dt)
        plotter.update(quad.position, quad.rpy)



if __name__ == '__main__':
    main()
