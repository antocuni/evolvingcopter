import numpy as np

class Creature(object):
    INPUTS = 2  # z_setpoint, current z position
    OUTPUTS = 1 # PWM for all 4 motors
    STATE_VARS = 1

    def __init__(self, generation=0, parent=None):
        N = self.INPUTS + self.STATE_VARS
        M = self.OUTPUTS + self.STATE_VARS
        self.id = None
        self.generation = generation
        self.parent = parent
        self.matrix = np.random.random(N*M).reshape(M, N) - 0.5
        self.constant = np.random.random(M) - 0.5
        self.reset()

    def __repr__(self):
        return '<Creature id=%s, generation=%s>' % (self.id, self.generation)

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

