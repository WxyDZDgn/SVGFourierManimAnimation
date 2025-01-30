from math import floor

from Fourier import Fourier
from SVG import SVG

if __name__ == '__main__':
    svg = SVG('./res/QianJianTec1737905305902.svg')
    f = Fourier(svg.fitting_parameters())
    delta = 0.001
    for i in range(floor(1 / delta)):
        res = f.get_value(i * delta)
        print(f'{res.real}\t{res.imag}')
