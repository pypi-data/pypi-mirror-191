from calculator import Calculator
import pytest
from hypothesis import given, settings, HealthCheck, assume, strategies as st


def test_calculator():
    calc = Calculator(9)
    calc.root(2)
    assert calc.memory == 3.0
    calc.multiply(11.1)
    assert calc.memory == 33.3


def test_calculator_types_1():
    with pytest.raises(TypeError):
        Calculator("a", 4)


def test_calculator_types_2():
    with pytest.raises(TypeError):
        Calculator(2, "b")


@given(
    st.floats(),
    st.floats(),
    st.floats(),
    st.floats(),
    st.integers(),
)
@settings(suppress_health_check=(HealthCheck.filter_too_much,))
def test_calculator_hypo(num1, num2, num3, num4, num5):
    assume(-1000 < num1 < 1000)
    assume(-1000 < num2 < 1000)
    assume(-1000 < num3 < 1000)
    assume(0.001 < abs(num4) < 1000)
    assume(num5 > 0.001)

    calc = Calculator()
    calc.add(num1)
    assert calc.memory == num1
    calc.subtract(num2)
    assert calc.memory == num1 - num2
    calc.multiply(num3)
    assert calc.memory == (num1 - num2) * num3
    calc.divide(num4)
    assert calc.memory == (num1 - num2) * num3 / num4
    if calc.memory >= 0:
        calc.root(num5)
        assert calc.memory == ((num1 - num2) * num3 / num4) ** (1 / num5)
