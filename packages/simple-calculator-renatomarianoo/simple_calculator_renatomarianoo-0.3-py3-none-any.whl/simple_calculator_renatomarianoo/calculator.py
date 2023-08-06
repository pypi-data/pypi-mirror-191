class Calculator:
    """ A calculator that asks the user for the desired mathematical operation and a value.
        The calculator possesses a memory which is initially set to 0.
        The operations will be performed between the current memory value and the input value.
        A validation process is carried out for the input values.
    """
    memory_value = float()

    def __init__(self, n) -> None:
        self.n = n

    @staticmethod
    def validate_arguments(user_entry: str) -> float:
        """ Verifies the user entry """
        try:
            user_entry = float(user_entry)
        except ValueError:
            print(f'\n\033[91m\033[1mThe input value is not a number!\033[0m')
        return float(user_entry)

    @staticmethod
    def reset_memory():
        """ Sets the value in the memory to zero
            This value should be passed without arguments: Calculator.reset_memory()
        """
        Calculator.memory_value = float(0)

    def set_memory(self):
        """ Sets the memory to a value specified by the user
            Calculator(desired_value).set_memory()
        """
        self.n = self.validate_arguments(self.n)
        Calculator.memory_value = self.n

    def add(self):
        """ Adds the current value in memory to desired value:
            Calculator(desired_value).add()
        """
        self.n = self.validate_arguments(self.n)
        result = Calculator.memory_value + self.n
        print(f'\033[1m{Calculator.memory_value} + {self.n} = \033[36m{result}\033[0m'.center(85))
        Calculator.memory_value = result
        return Calculator.memory_value

    def subtract(self):
        """ Subtracts the current value in memory to desired value:
            Calculator(desired_value).subtract()
        """
        self.n = self.validate_arguments(self.n)
        result = Calculator.memory_value - self.n
        print(f'\033[1m{Calculator.memory_value} - {self.n} = \033[36m{result}\033[0m'.center(85))
        Calculator.memory_value = result
        return Calculator.memory_value

    def multiply(self):
        """ Multiplies the current value in memory to desired value:
            Calculator(desired_value).multiply()
        """
        self.n = self.validate_arguments(self.n)
        result = Calculator.memory_value * self.n
        print(f'\033[1m{Calculator.memory_value} * {self.n} = \033[36m{result}\033[0m'.center(85))
        Calculator.memory_value = result
        return Calculator.memory_value

    def divide(self):
        """ Divides the current value in memory to desired value:
            Calculator(desired_value).divide()
        """
        self.n = self.validate_arguments(self.n)
        if self.n != 0:
            result = Calculator.memory_value / self.n
            print(f'\033[1m{Calculator.memory_value} / {self.n} = \033[36m{result}\033[0m'.center(85))
            Calculator.memory_value = result
            return Calculator.memory_value
        else:
            print(f'\033[91mCannot divide by zero!\033[0m\n')
            return Calculator.memory_value

    def expon(self):
        """ Value in memory is exponentiated to the user input
            Calculator(desired_value).expon()
        """
        self.n = self.validate_arguments(self.n)
        result = Calculator.memory_value ** self.n
        print(f'\033[1m{Calculator.memory_value} ^ {self.n} = \033[36m{result}\033[0m'.center(85))
        Calculator.memory_value = result
        return Calculator.memory_value

    def n_root(self):
        """ Generate the n Root for the value in memory (n: desired value provided by the user)
            Calculator(desired_value).n_root()
        """
        self.n = self.validate_arguments(self.n)
        result = Calculator.memory_value ** (1 / self.n)
        print(f'\033[1m{Calculator.memory_value} ^ (1/{self.n}) = \033[36m{result}\033[0m'.center(85))
        Calculator.memory_value = result
        return Calculator.memory_value


def menu_calculator():
    print(88 * '_')
    print(25 * ' ' + '\033[1mCALCULATOR PROGRAM\033[0m' + '\n'
                     'The calculator possesses a memory which is initially set to 0.\n'
                     'The operations will be performed between the current memory value and the input value.')

    while True:
        # Menu selection
        print(88 * '_')
        print('Operation:\n(+) Addition          (-) Subtraction\n(*) Multiplication    (/) Division'
              '\n(e) Exponential       (r) n Root\n(0) Reset Memory      (1) Set Memory Value     (9) Exit program')
        print(f'(Current Memory Value: \033[94m{Calculator.memory_value}\033[0m)')
        print(88 * '_')
        menu = input('Select Operation: ')

        if menu in ['+', '-', '*', '/', 'e', 'r', '0', '1', '9']:
            if menu not in ['0', '1', '9']:
                num: str = input('Enter the number: ')

            if menu == '9':
                break
            elif menu == '1':
                Calculator(input('Set Memory Value: ')).set_memory()
            elif menu == '0':
                Calculator.reset_memory()

            # Call for class functions
            elif menu == '+':
                Calculator(num).add()
            elif menu == '-':
                Calculator(num).subtract()
            elif menu == '*':
                Calculator(num).multiply()
            elif menu == '/':
                Calculator(num).divide()
            elif menu == 'e':
                Calculator(num).expon()
            elif menu == 'r':
                Calculator(num).n_root()

        else:
            print('\033[91mInvalid Menu Operation\033[0m')


if __name__ == "__main__":
    menu_calculator()


