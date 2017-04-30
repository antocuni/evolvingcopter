import numpy as np
from model.quadcopter import Quadcopter
from plotter.quadplotter import QuadPlotter, RED, GREEN

class Creature(object):
    INPUTS = 2  # z_setpoint, current z position
    OUTPUTS = 1 # PWM for all 4 motors
    STATE_VARS = 1

    def __init__(self, id, generation=0, parent=None):
        N = self.INPUTS + self.STATE_VARS
        M = self.OUTPUTS + self.STATE_VARS
        self.id = id
        self.generation = generation
        self.parent = parent
        self.matrix = np.random.random(N*M).reshape(M, N) - 0.5
        self.constant = np.random.random(M) - 0.5
        self.reset()

    def reset(self):
        self.state = np.zeros(self.STATE_VARS)

    def run_step(self, inputs):
        in_values = np.concatenate([self.state, inputs])
        out_values = np.dot(self.matrix, in_values) + self.constant
        new_state = out_values[:self.STATE_VARS]
        outputs = out_values[self.STATE_VARS:]
        #
        self.state = new_state
        return outputs

    def evolve(self):
        """
        What do we want?
        We probably want two steps of evolution:

          1. the first does the "fine tuning": so we adjust many/most/all the values
             by a small amount (+/- 1%?)

         2. the second does rare mutations: it might adjust 1 or 2 values by a larger amount
            (+/- 20%?), but it occurs rarely
        """
        # mu = 0
        # sigma = 0.2
        # k = np.random.normal(mu, sigma, len(self.matrix))
        # matrix + (matrix*k)


class Environment(object):
    """
    Very simple environment. The quadcopter starts at position (0, 0, 3).

    The goal is to reach setpoint z=5 in 2 seconds (so, they need to "go up"),
    then to reach setpoint z=3 in other 2 seconds (so, "go down").

    Fitness is computed as to cumulative distance from the setpoint at each
    step
    """

    def __init__(self, dt=0.01, show=False):
        self.dt = dt
        self.show = show
        self.plotter = None
        if self.show:
            self.plotter = QuadPlotter()
            self.plotter.add_marker((0, 0, 5), RED)
            self.plotter.add_marker((0, 0, 3), GREEN)

    def run(self, creature):
        quad = Quadcopter()
        quad.position = (0, 0, 3)
        z_setpoint = 5 # first task: go to setpoint (0, 0, 5)
        fitness = 0
        while quad.t < 4:
            if quad.t >= 2:
                # switch to second task
                z_setpoint = 2
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


def main():
    import time
    #
    # create many creatures
    env = Environment(show=False)
    creatures = []
    print 'running simulation...'
    for i in range(50):
        c = Creature(i)
        fitness = env.run(c)
        creatures.append((fitness, c))

    creatures.sort()
    for fitness, c in creatures:
        print fitness, c.id

    # show the best
    show_env = Environment(show=True)
    fitness, c = creatures[0]
    show_env.run(c)

if __name__ == '__main__':
    main()
