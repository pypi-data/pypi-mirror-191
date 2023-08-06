'''Dummy package for rational Numbers
'''
from __future__ import annotations
import math


class RationalNumber:
    '''Dummy RationalNumber Class'''

    def __init__(self, x: int, y: int) -> None:
        common_divisor = math.gcd(x, y)
        self.numerator = x / common_divisor
        self.denominator = y / common_divisor

    def __add__(self, other: RationalNumber) -> RationalNumber:
        common_denominator = math.lcm(
            self.denominator, other.denominator)  # type: ignore[arg-type]

        result_numerator = int(
            self.numerator * (common_denominator/self.denominator) +
            other.numerator * (common_denominator/other.denominator)
        )

        return RationalNumber(result_numerator, common_denominator)

    def __str__(self) -> str:
        return f'{self.numerator}/{self.denominator}'
