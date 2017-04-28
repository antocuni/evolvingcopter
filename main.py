import numpy as np
from model.quadcopter import Quadcopter
from plotter.quadplotter import QuadPlotter

def main():
    quad = Quadcopter()
    plotter = QuadPlotter()

    F = 1.7
    quad.set_thrust(0, 2*F, 0, 2*F)
    dt = 0.01
    for i in range(1000):
        quad.step(dt)
        plotter.plot_step(quad)


if __name__ == '__main__':
    main()
