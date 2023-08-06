import doctest


class Calculator:
    """This module replicates a handheld calculator, which performs
    simple mathematical tasks with the number stored in calculator's memory.
    The calculator can add, subtract, multplty with, divide by and take an
    nth root of the number stored in memory.

    For example:
    >>> calc = Calculator(memory = 0.0, precision = 3)
    >>> calc.add(3)
    >>> calc.display()
    Current calculator value:  3.000
    >>> calc.subtract(5)
    >>> calc.display()
    Current calculator value: -2.000
    >>> calc.multiply(7.14)
    >>> calc.display()
    Current calculator value: -14.280
    >>> calc.reset()
    >>> calc.display()
    Current calculator value:  0.000
    """

    def __init__(self, memory: float = 0.0, precision: int = 1):
        # Run validations to received arguments
        if not isinstance(memory, float) and not isinstance(memory, int):
            raise TypeError("The calculator can only accept float or integer numbers.")
        if not isinstance(precision, int):
            raise TypeError(
                "The precision of the displayed value can be set with an integer number."
            )
        if precision < 0:
            raise ValueError(
                "The precision of the calculator display can only be a non-negative integer."
            )

        # Asign inputs to self object
        self.__memory = memory
        self.precision = precision

    @property
    def memory(self) -> float:
        """Allow the user to read the current memory of the calculator."""
        return self.__memory

    def add(self, number: float):
        """Perform addition operation: add input number to the self.memory variable."""
        self.__memory += number

    def subtract(self, number: float):
        """Perform subtraction operation: subtract input number from the self.memory variable."""
        self.__memory -= number

    def multiply(self, number: float):
        """Perform multiplication operation: multiplie self.memory variable with the input number."""
        self.__memory *= number

    def divide(self, number: float):
        """Perform division operation: divide the self.memory variable by the input number."""
        if number == 0:
            raise ValueError("Division by zero is forbidden.")
        self.__memory /= number

    def root(self, number: int):
        """Perform root operation: take the nth root of the self.memory variable, where n is the input number."""
        if number == 0 or not isinstance(number, int):
            raise ValueError(
                "The calculator does not support 0th root (or non-integer root) calculation."
            )
        if self.__memory >= 0.0:
            self.__memory = self.__memory ** (1 / number)
        else:
            raise ValueError(
                f"The root operation can only be performed on non-negative numbers. Current memory value: {self.__memory}."
            )

    def reset(self):
        """Reset the self.memory variable, i.e. set its value to 0.0."""
        self.__memory = 0

    def set_precision(self, precision: int):
        """Define the precision of the displayed result (self.memory variable)."""
        self.precision = precision

    def display(self):
        """Print the calculator result to the screen."""
        print(f"Current calculator value: {self.memory: .{self.precision}f}")


if __name__ == "__main__":
    print(doctest.testmod())
