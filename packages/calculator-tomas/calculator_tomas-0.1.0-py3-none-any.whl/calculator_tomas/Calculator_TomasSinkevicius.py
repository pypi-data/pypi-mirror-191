class Calculator:
    """
    A class to perform basic calculator operations

    ...

    Attributes
    ----------
    memory : float
        Calculator memory

    Methods
    ----------
    add(number):
        Takes the number and adds it to calculator memory
    subtract(number):
        Takes the number and subtracts it from calculator memory
    multiply(number):
        Takes number from Calculators memory and multiplies it by a given number
    divide(number):
        Takes number from Calculators memory and divides it by a given number
    root(number):
        Takes number from Calculators memory and takes the root of it by a given number
    reset():
        Resets calculator memory
    """

    @classmethod
    def __int__(cls):
        cls.memory = 0.0

    @classmethod
    def add(cls, number=float) -> float:
        """Takes the number and adds it to calculator memory

            For example:

            >>> Calculator.memory = 0.0
            >>> Calculator.add(5)
            5.0
        """
        cls.memory += number
        return cls.memory

    @classmethod
    def subtract(cls, number=float) -> float:
        """Takes the number and subtracts it from calculator memory

            For example:

            >>> Calculator.memory = 5.0
            >>> Calculator.subtract(2)
            3.0
        """
        cls.memory -= number
        return cls.memory

    @classmethod
    def multiply(cls, number=float) -> float:
        """Takes number from Calculators memory and multiplies it by a given number

            For example:

            >>> Calculator.memory = 1.3
            >>> Calculator.multiply(10)
            13.0
        """
        cls.memory *= number
        return cls.memory

    @classmethod
    def divide(cls, number=float) -> float:
        """Takes number from Calculators memory and divides it by a given number

            For example:

            >>> Calculator.memory = 13.0
            >>> Calculator.divide(2)
            6.5
        """
        if number == 0:
            print('Can not divide by 0')
        else:
            cls.memory /= number
            return cls.memory

    @classmethod
    def root(cls, root: float) -> float:
        """Takes number from Calculators memory and takes the root of it by a given number

            For example:

            >>> Calculator.memory = 25
            >>> Calculator.root(2)
            5.0
        """
        if cls.memory < 0:
            # Test to see if we are not taking root of a negative number
            print("Can't take a root of negative number")
            return cls.memory
        else:
            try:
                cls.memory = cls.memory ** (1/root)
            except OverflowError:
                print("Result is too large")
                return cls.memory

        return cls.memory

    @classmethod
    def reset(cls) -> float:
        """Resets calculator memory

            For example:

            >>> Calculator.memory = 5.0
            >>> Calculator.reset()
            0.0
        """
        cls.memory = 0.0
        return cls.memory


if __name__ == '__main__':

    import doctest
    print(doctest.testmod())
