# Instruction hot to use calculatorGS Module

calculatorGS is a state-of-the-art calculator module for Python. It lets you perform calculation tasks
not only by adding or subtracting numbers, but also by using advanced techniques such as multiplication,
division or even taking an nth root of the number.

e.g.

```python
> from calculatorGS import Calculator

> calc = Calculator()
> calc.add(8)
> calc.divide(2)
> calc.root(2)
> calc.display()

Current calculator value: 2
```

## Installation

Install calculatorGS module using pip:
python -m pip install calculatorGS

## Testing

Testing of the modules requires pytest and hypothesis. Tests can be run after installation with:
pytest test_calculator.py
