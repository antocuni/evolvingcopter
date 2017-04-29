import numpy as np
from model.quadcopter import Quadcopter
from plotter.quadplotter import QuadPlotter, RED

def P_controller(quad, sp_z):
    """
    a very simple "P-only" controller
    """
    F = 0.5 # PWM needed to contrast the gravity
    K = 0.1
    diff = sp_z - quad.position.z
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


class PD(object):

    def __init__(self, kp=0.2, kd=0.1):
        self.kp = kp
        self.kd = kd
        self.last_error = None

    def __call__(self, quad, dt, sp_z):
        F = 0.5 # PWM to contrast the gravity
        z = quad.position.z
        error = sp_z - z
        if self.last_error is None:
            d_error = 0
        else:
            d_error = (error - self.last_error) / dt
        #
        self.last_error = error
        diff = self.kp*error + self.kd*d_error
        T = F+diff
        quad.set_thrust(T, T, T, T)


def main():
    quad = Quadcopter()
    plotter = QuadPlotter()
    pd_controller = PD()

    quad.position = (0, 0, 3) # put it a bit above the ground
    dt = 0.01
    setpoint = 5
    plotter.add_marker((0, 0, setpoint), RED)
    while plotter.show_step():
        #P_controller(quad, sp_z=setpoint)
        pd_controller(quad, dt, sp_z=setpoint)
        #lift_controller(quad)
        #yaw_controller(quad)
        quad.step(dt)
        plotter.update(quad.position, quad.rpy)



if __name__ == '__main__':
    main()
