import math
import re
from math import floor

from lxml import etree

import Fourier
from Curve import Curve, Category

arguments_count = dict()
for each in 'M2,m2,L2,l2,H1,h1,V1,v1,C6,c6,S4,s4,Q4,q4,T2,t2,A7,a7,Z0,z0'.split(','):
    arguments_count[each[0]] = int(each[1:])


class SVG:
    def __init__(self, path: str) -> None:
        self.path = path
        self.raw_curves = self.__parse()
        self.curves = self.__get_curves()
        pass

    def __parse(self) -> tuple[tuple[str, tuple[int, ...]], ...]:
        parser = etree.HTMLParser()
        tree = etree.parse(self.path, parser=parser)
        svg = tree.xpath('//path/@d')[0]

        # args = tuple(map(lambda x: (x[0], int(x[1])), 'M2,m2,L2,l2,H1,h1,V1,v1,C6,c6,S4,s4,Q4,q4,T2,t2,A7,a7,Z0,z0'.split(',')))
        # args = tuple(map(lambda x: (x[0] + ('' if x[1] <= 0 else ('-?\\d+' + ('\\s-?\\d+' * (x[1] - 1))))), args))
        args = '[MmLlHhVvCcSsQqTtAaZz][^A-Za-z]{0,}'

        pattern = re.compile(args)
        elements = pattern.findall(svg)
        elements = tuple(map(lambda x: ((x,) if len(x) <= 1 else (x[0], tuple(map(int, x[1:].split(' '))))), elements))
        return elements

    def __get_curves(self) -> tuple[Curve, ...]:
        result = []
        current = 0 + 0j
        start = 0 + 0j
        pre_operation = ''
        controller = 0 + 0j
        for each_element in self.raw_curves:
            if each_element[0] in ('Z', 'z'):
                result.append(Curve(Category.SEG, current, start))
                continue
            operation, arguments = each_element
            for argument in list(
                    arguments[idx * arguments_count[operation]: (idx + 1) * arguments_count[operation]]
                    for idx in range(len(arguments) // arguments_count[operation])
            ):
                match operation:
                    case 'M':
                        x, y = argument
                        current = complex(x, y)
                        start = current
                    case 'm':
                        dx, dy = argument
                        current = current + complex(dx, dy)
                        start = current
                    case 'L':
                        x, y = argument
                        result.append(Curve(Category.SEG, current, complex(x, y)))
                        current = complex(x, y)
                    case 'l':
                        dx, dy = argument
                        result.append(Curve(Category.SEG, current, current + complex(dx, dy)))
                        current = complex(dx, dy)
                    case 'H':
                        x, = argument
                        result.append(Curve(Category.SEG, current, complex(x, current.imag)))
                        current = complex(x, current.imag)
                    case 'h':
                        dx, = argument
                        result.append(Curve(Category.SEG, current, current + complex(dx, 0)))
                        current = current + complex(dx, 0)
                    case 'V':
                        y, = argument
                        result.append(Curve(Category.SEG, current, complex(current.real, y)))
                        current = complex(current.real, y)
                    case 'v':
                        dy, = argument
                        result.append(Curve(Category.SEG, current, current + complex(0, dy)))
                        current = current + complex(0, dy)
                    case 'C':
                        x1, y1, x2, y2, x, y = argument
                        result.append(
                            Curve(Category.CBC, current, complex(x, y), p1=complex(x1, y1), p2=complex(x2, y2)))
                        controller = complex(x2, y2)
                        current = complex(x, y)
                    case 'c':
                        dx1, dy1, dx2, dy2, dx, dy = argument
                        result.append(
                            Curve(Category.CBC, current, current + complex(dx, dy), p1=(current + complex(dx1, dy1)),
                                  p2=(current + complex(dx2, dy2))))
                        controller = current + complex(dx2, dy2)
                        current = current + complex(dx, dy2)
                    case 'S':
                        x2, y2, x, y = argument
                        p1 = current if pre_operation not in ('C', 'c', 'S', 's') else (2 * current - controller)
                        result.append(Curve(Category.CBC, current, complex(x, y), p1=p1, p2=complex(x2, y2)))
                        controller = complex(x2, y2)
                        current = complex(x, y)
                    case 's':
                        dx2, dy2, dx, dy = argument
                        p1 = current if pre_operation not in ('C', 'c', 'S', 's') else (2 * current - controller)
                        result.append(Curve(Category.CBC, current, current + complex(dx, dy), p1=p1,
                                            p2=(current + complex(dx2, dy2))))
                        controller = current + complex(dx2, dy2)
                        current = current + complex(dx, dy)
                    case 'Q':
                        x1, y1, x, y = argument
                        result.append(Curve(Category.QBC, current, complex(x, y), p1=complex(x1, y1)))
                        controller = complex(x1, y1)
                        current = complex(x, y)
                    case 'q':
                        dx1, dy1, dx, dy = argument
                        result.append(
                            Curve(Category.QBC, current, current + complex(dx, dy), p1=(current + complex(dx1, dy1))))
                        controller = current + complex(dx1, dy1)
                        current = current + complex(dx, dy)
                    case 'T':
                        x, y = argument
                        p1 = current if pre_operation not in ('Q', 'q', 'T', 't') else (2 * current - controller)
                        result.append(Curve(Category.QBC, current, complex(x, y), p1=p1))
                        controller = p1
                        current = complex(x, y)
                    case 't':
                        dx, dy = argument
                        p1 = current if pre_operation not in ('Q', 'q', 'T', 't') else (2 * current - controller)
                        result.append(Curve(Category.QBC, current, current + complex(dx, dy), p1=p1))
                        controller = p1
                        current = current + complex(dx, dy)
                    case 'A':
                        rx, ry, angle, large_arc_flag, sweep_flag, x, y = argument
                        result.append(
                            Curve(Category.ECC, current, complex(x, y), angle=angle, large_arc_flag=large_arc_flag,
                                  sweep_flag=sweep_flag))
                        current = complex(x, y)
                    case 'a':
                        rx, ry, angle, large_arc_flag, sweep_flag, dx, dy = argument
                        result.append(Curve(Category.ECC, current, current + complex(dx, dy), angle=angle,
                                            large_arc_flag=large_arc_flag, sweep_flag=sweep_flag))
                        current = current + complex(dx, dy)
                    case _:
                        raise RuntimeError('Unknown SVG Command')
                pre_operation = operation
        return tuple(result)

    def get_value(self, lmd: float) -> complex:
        lmd -= floor(lmd)
        tm = lmd * len(self.curves)
        idx = floor(tm)
        return self.curves[idx].get_value(tm)

    def fitting_parameters(self, level: int = 200, delta: float = None) -> tuple[complex, ...]:

        def _integration(power: int, lmd: complex) -> complex:
            _inv1 = 1 / lmd
            _inv2 = _inv1 * _inv1
            _inv3 = _inv1 * _inv2
            _inv4 = _inv2 * _inv2
            _rot = Fourier.rotation(lmd)
            match power:
                case 0:
                    return _inv1 * _rot - _inv1
                case 1:
                    return (_inv1 - _inv2) * _rot + _inv2
                case 2:
                    return (_inv1 - 2 * _inv2 + 2 * _inv3) * _rot - 2 * _inv3
                case 3:
                    return (_inv1 - 3 * _inv2 + 6 * _inv3 - 6 * _inv4) * _rot + 6 * _inv4

        def _a(k: int, m: int) -> complex:
            _current_curve = self.curves[k]
            _points = self.curves[k].get_points()
            if m == 0:
                points = _current_curve.get_points()
                return sum(points) / len(points)
            _lmd = -2j * math.pi * m / len(self.curves)
            match _current_curve.category:
                case Category.SEG:
                    p0, p1 = _points
                    return _integration(1, _lmd) * (p1 - p0) + _integration(0, _lmd) * p0
                case Category.CBC:
                    p0, p1, p2, p3 = _points
                    return _integration(3, _lmd) * (p3 - 3 * p2 + 3 * p1 - p0) + 3 * _integration(2, _lmd) * (
                                p2 - 2 * p1 + p0) + 3 * _integration(1, _lmd) * (p1 - p0) + _integration(0, _lmd) * p0
                case Category.QBC:
                    p0, p1, p2 = _points
                    return _integration(2, _lmd) * (p2 - 2 * p1 + p0) + 2 * _integration(1, _lmd) * (
                                p1 - p0) + _integration(0, _lmd) * p0
                case Category.CBC:
                    return 0 + 0j
        if delta is not None:
            n = floor(1 / delta)
            return tuple(
                sum((delta * self.get_value(k * delta) * Fourier.rotation(-2j * math.pi * m * k * delta)) for k in range(n)) for m in
                range(-level, level + 1))
        else:
            res = []
            for _ in range(-level, level + 1):
                sm = 0 + 0j
                for k in range(len(self.curves)):
                    sm = sm + _a(k, _) * Fourier.rotation(-2j * math.pi * _ * k / len(self.curves))
                sm = sm / len(self.curves)
                res.append(sm)
            return tuple(res)

    def __repr__(self) -> str:
        return f'SVG({self.curves})'
