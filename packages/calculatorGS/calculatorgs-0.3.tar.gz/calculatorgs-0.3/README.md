# calculatorGS

The calculatorGS is a state-of-the-art calculator module for Python. It lets you perform calculation tasks
not only by adding or subtracting numbers, but also by using advanced techniques such as multiplication,
division or even taking an nth root of the number.

This is by far not a complete module. Many more features could be included in the future versions. Some
of them are:
Markup : _ Add more operations, such as exp, ln, sin, cos, etc.
_ Tests could be more thorough. Current tests do not check every function. \* Instruction could probably be a bit clearer. Readme file needs some fine tuning.

## An example

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

```python
python -m pip install calculatorGS
```

## Testing

Testing of the modules requires pytest and hypothesis. Tests can be run after installation with:

```python
pytest test_calculator.py
```

## License

Copyright Holger Krekel and others, 2004.
Distributed under the terms of the MIT license, pytest is free and open source software.
