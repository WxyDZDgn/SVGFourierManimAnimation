from enum import Enum
from math import floor
from unittest import case


class Category(Enum):
    SEG = 'Segment'
    CBC = 'Cubic Bezier Curve'
    QBC = 'Quadratic Bezier Curve'
    ECC = 'Euclidean Curve'


class Curve:
    def __init__(self, category: Category, start: complex, end: complex, **kwargs) -> None:
        self.category = category
        # 均为绝对坐标
        self.start = start
        self.end = end
        self.kwargs = kwargs

    def get_value(self, lmd: float) -> complex:
        lmd -= floor(lmd)
        match self.category:
            case Category.SEG:
                return self.start + lmd * (self.end - self.start)
            case Category.CBC:
                p0, p1, p2, p3 = self.start, self.kwargs['p1'], self.kwargs['p2'], self.end
                t = lmd
                t1 = 1 - lmd
                return (t1 ** 3) * p0 + 3 * (t1 ** 2) * t * p1 + 3 * t1 * (t ** 2) * p2 + (t ** 3) * p3
            case Category.QBC:
                p0, p1, p2 = self.start, self.kwargs['p1'], self.end
                t = lmd
                t1 = 1 - lmd
                return (t1 ** 2) * p0 + 2 * t1 * t * p1 + (t ** 2) * p2
            case Category.ECC:
                return 0 + 0j
            case _:
                raise TypeError(f'未识别的类型{self.category}')

    def get_points(self) -> tuple[complex, ...]:
        match self.category:
            case Category.SEG:
                return self.start, self.end
            case Category.CBC:
                return self.start, self.kwargs['p1'], self.kwargs['p2'], self.end
            case Category.QBC:
                return self.start, self.kwargs['p1'], self.end
            case _:
                return 0 + 0j,

    def __repr__(self) -> str:
        match self.category:
            case Category.SEG:
                return f'SEG(start={self.start}, end={self.end})'
            case Category.CBC:
                return f'CBC(start={self.start}, p1={self.kwargs["p1"]}, p2={self.kwargs["p2"]}, end={self.end}'
            case Category.QBC:
                return f'QBC(start={self.start}, p1={self.kwargs["p1"]}, end={self.end})'
            case Category.ECC:
                return f'ECC(start={self.start}, rx={self.kwargs["rx"]}, ry={self.kwargs["ry"]}, angle={self.kwargs["angle"]}, large-arc-flag={self.kwargs["large-arc-flag"]}, sweep-flag={self.kwargs["sweep-flag"]}, end={self.end})'
            case _:
                return f'{self.category}(???)'
