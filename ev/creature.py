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
        # don't save the parent for now, else pickle.dump gives RecursionError
        #self.parent = parent
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
                        self._mutate_all,
                        self._mutate_zero_or_one,
                        self._mutate_set_equal_to]
        mutate = random.choice(mutate_meths)
        matrix = self.matrix
        constant = self.constant
        if random.choice([True, False]):
            matrix = mutate(matrix)
        else:
            constant = mutate(constant)
        return self.__class__(parent=self, matrix=matrix, constant=constant)

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

    def _mutate_zero_or_one(self, x):
        shape = x.shape
        flat = x.flatten()
        i = random.randrange(len(flat))
        v = random.choice([0.0, 1.0])
        flat[i] = v
        return flat.reshape(shape)

    def _mutate_set_equal_to(self, x):
        flat = x.flatten()
        i = random.randrange(len(flat))
        j = random.randrange(len(flat))
        flat[i] = flat[j]
        return flat.reshape(shape)


class SpecializedCreature(Creature):
    """
    This is equivalent to Creature if:
        INPUTS = 2
        OUTPUTS = 1
        STATE_VARS = 1

    but it unrolls the dot() product, so it is much faster
    """

    def __init__(self, *args, **kwargs):
        Creature.__init__(self, *args, **kwargs)
        # store the data in a plain Python list, which pypy is able to
        # optimize as a float array
        self.data = list(self.matrix.ravel()) + list(self.constant)
        self.data_state = [0.0]
        assert self.matrix.shape == (2, 3)
        assert len(self.data) == 8

    def run_step(self, inputs):
        # state: [state_vars ... inputs]
        # out_values: [state_vars, ... outputs]
        k0, k1, k2, q0, q1, q2, c0, c1 = self.data
        s0 = self.data_state[0]
        z_sp, z = inputs
        #
        # compute the output
        out0 = s0*k0 + z_sp*k1 + z*k2 + c0
        out1 = s0*q0 + z_sp*q1 + z*q2 + c1
        #
        self.data_state[0] = out0
        outputs = [out1]
        #
        # sanity check
        ## expected_outputs = Creature.run_step(self, inputs)
        ## assert self.data_state[0] == self.state[0]
        ## assert expected_outputs == outputs
        #
        return outputs
