import math


def rotation(value: complex) -> complex:
    return complex(math.cos(value.imag), math.sin(value.imag)) * math.exp(value.real)


class Fourier:
    def __init__(self, factors: list[complex, ...] | tuple[complex, ...]):
        self.factors = tuple(factors)
        self.level = len(self.factors) // 2

    def get_vectors(self, t: float) -> tuple[complex, ...]:
        return tuple((self.factors[i] * rotation(2j * math.pi * (i - self.level) * t)) for i in range(len(self.factors)))

    def get_value(self, t: float) -> complex:
        return sum(self.get_vectors(t))
    
    def __repr__(self) -> str:
        return f'{self.factors}'
