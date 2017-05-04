import numpy as np
from model.quadcopter import Quadcopter
from plotter.quadplotter import QuadPlotter, RED, GREEN

class Environment(object):
    """
    Very simple environment. The quadcopter starts at position (0, 0, 3).

    The goal is to reach setpoint z=5 in 2 seconds (so, they need to "go up"),
    then to reach setpoint z=3 in other 2 seconds (so, "go down").

    Fitness is computed as to cumulative distance from the setpoint at each
    step
    """

    def __init__(self, dt=0.01, z1=5, z2=3, show=False):
        self.dt = dt
        self.z1 = z1
        self.z2 = z2
        self.show = show
        self.plotter = None
        if self.show:
            self.plotter = QuadPlotter()
            self.plotter.add_marker((0, 0, z1), RED)
            self.plotter.add_marker((0, 0, z2), GREEN)

    def run(self, creature):
        quad = Quadcopter()
        quad.position = (0, 0, 3)
        z_setpoint = self.z1 # first task: go to setpoint (0, 0, z1)
        fitness = 0
        while quad.t < 4:
            if quad.t >= 2:
                # switch to second task
                z_setpoint = self.z2
            #
            inputs = [z_setpoint, quad.position.z]
            outputs = creature.run_step(inputs)
            assert len(outputs) == 1
            pwm = outputs[0]
            quad.set_thrust(pwm, pwm, pwm, pwm)
            quad.step(self.dt)
            fitness += self.compute_fitness(quad, z_setpoint)
            self.show_step(quad)
        return fitness

    def show_step(self, quad):
        if self.show:
            self.plotter.update(quad)
            self.plotter.show_step()

    def compute_fitness(self, quad, z_setpoint):
        # for now, the goal is to reach the target position as fast as
        # possible and then to stay there. So a measure of the fitness is the
        # distance to the target at every step (the goal is to *minimize* the
        # total value, of course)
        target = [0, 0, z_setpoint]
        position = np.array(quad.position)
        distance = np.linalg.norm(target - position)
        return distance

