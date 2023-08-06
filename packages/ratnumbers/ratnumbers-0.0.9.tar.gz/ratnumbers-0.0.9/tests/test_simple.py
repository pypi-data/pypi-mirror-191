
from ratnumber import RationalNumber


def test_simplify_numerator() -> None:

    rational_num_1 = RationalNumber(6, 8)

    assert (
        rational_num_1.numerator == 3 and rational_num_1.denominator == 4
    ), 'Simplification is wrong'
