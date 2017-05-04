import random
import numpy as np

class Creature(object):
    INPUTS = 2  # z_setpoint, current z position
    OUTPUTS = 1 # PWM for all 4 motors
    STATE_VARS = 1

    def __init__(self, parent=None, matrix=None, constant=None):
        N = self.INPUTS + self.STATE_VARS
        M = self.OUTPUTS + self.STATE_VARS
        self.id = None
        self.parent = parent
        self.matrix = matrix
        self.constant = constant
        #
        if self.matrix is None:
            self.matrix = np.random.random(N*M).reshape(M, N) - 0.5
        if self.constant is None:
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

    def reproduce(self):
        """
        What do we want?
        We probably want two steps of evolution:

          1. the first does the "fine tuning": so we adjust many/most/all the values
             by a small amount (+/- 1%?)

         2. the second does rare mutations: it might adjust 1 or 2 values by a larger amount
            (+/- 20%?), but it occurs rarely
        """
        mu = 0
        sigma = 0.1
        if random.choice([True, False]):
            # evolve the matrix
            k = np.random.normal(mu, sigma, self.matrix.shape)
            new_matrix = self.matrix + (self.matrix*k)
            new_constant = self.constant
        else:
            # evolve the constant
            new_matrix = self.matrix
            k = np.random.normal(mu, sigma, self.constant.shape)
            new_constant = self.constant + (self.constant*k)
        #
        return Creature(parent=self, matrix=new_matrix, constant=new_constant)
