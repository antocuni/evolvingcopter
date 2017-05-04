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
        return '<Creature id=%s>' % (self.id,)

    def reset(self):
        self.state = np.zeros(self.STATE_VARS + self.INPUTS)

    def run_step(self, inputs):
        # state: [state_vars ... inputs]
        # out_values: [state_vars, ... outputs]
        self.state[self.STATE_VARS:] = inputs
        out_values = np.dot(self.matrix, self.state) + self.constant
        self.state[:self.STATE_VARS] = out_values[:self.STATE_VARS]
        outputs = out_values[self.STATE_VARS:]
        return outputs

    def reproduce(self):
        mutate_meths = [self._mutate_normal,
                        self._mutate_random,
                        self._mutate_one,
                        self._mutate_all]
        mutate = random.choice(mutate_meths)
        matrix = self.matrix
        constant = self.constant
        if random.choice([True, False]):
            matrix = mutate(matrix)
        else:
            constant = mutate(constant)
        return Creature(parent=self, matrix=matrix, constant=constant)

    def _mutate_random(self, x):
        # change every value of a random k between 50% and 150%
        k = np.random.random(x.shape) + 0.5
        return x*k

    def _mutate_normal(self, x):
        # like mutate_random, but with a normal distribution
        mu = 0
        sigma = 0.1
        k = np.random.normal(mu, sigma, x.shape) + 0.5
        return x*k
        return self.matrix, new_constant

    def _mutate_one(self, x):
        # change only one item, between 50% and 150%
        shape = x.shape
        flat = x.flatten()
        i = random.randrange(len(flat))
        k = random.random() + 0.5
        flat[i] *= k
        return flat.reshape(shape)

    def _mutate_all(self, x):
        # change all the items by the same k
        k = random.random() + 0.5
        return x*k
