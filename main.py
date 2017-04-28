import numpy as np
from model.quadcopter import Quadcopter
from plotter.quadplotter import QuadPlotter

def main():
    quad = Quadcopter()
    plotter = QuadPlotter()

    F = 1.7
    quad.set_thrust(F, F*1.01, F, F*1.01)
    dt = 0.01
    for i in range(1000):
        quad.step(dt)
        plotter.update(quad.position, quad.rpy)
        plotter.show_step()


if __name__ == '__main__':
    main()
