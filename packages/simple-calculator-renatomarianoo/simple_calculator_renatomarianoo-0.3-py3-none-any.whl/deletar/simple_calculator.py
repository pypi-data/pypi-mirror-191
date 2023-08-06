class Calculator:
    """ A calculator that asks the user for the desired mathematical operation and a value.
        The calculator possesses a memory which is initially set to 0.
        The operations will be performed between the current memory value and the input value.
        A validation process is carried out for the input values.
    """

    def __init__(self, memory_value, n) -> None:
        self.memory_value = memory_value
        self.n = n

    @staticmethod
    def validate_arguments(user_entry: str) -> float:
        """ Verifies user entry: self.n - through each function
                                or self.memory_value - passed directly from main
        """
        try:
            user_entry = float(user_entry)
        except ValueError:
            print(f'\n\033[91m\033[1mThe input value is not a number!\033[0m')
        return float(user_entry)

    def add(self):
        self.n = self.validate_arguments(self.n)
        self.memory_value += self.n
        print(f'\033[1m{self.memory_value} + {self.n} = \033[36m{self.memory_value}\033[0m'.center(85))
        return self.memory_value

    def subtract(self):
        self.n = self.validate_arguments(self.n)
        self.memory_value -= self.n
        print(f'\033[1m{self.memory_value} - {self.n} = \033[36m{self.memory_value}\033[0m'.center(85))
        return self.memory_value

    def multiply(self):
        self.n = self.validate_arguments(self.n)
        self.memory_value = self.memory_value * self.n
        print(f'\033[1m{self.memory_value} * {self.n} = \033[36m{self.memory_value}\033[0m'.center(85))
        return self.memory_value

    def divide(self):
        self.n = self.validate_arguments(self.n)
        if self.n != 0:
            self.memory_value = self.memory_value / self.n
            print(f'|{self.memory_value} / {self.n} = \033[36m{self.memory_value}\033[0m'.center(85))
            return self.memory_value
        else:
            print(f'\033[91mCannot divide by zero!\033[0m\n')
            return self.memory_value

    def expon(self):
        """ Value in memory is exponentiated to the user input """
        self.n = self.validate_arguments(self.n)
        self.memory_value = self.memory_value ** self.n
        print(f'\033[1m{self.memory_value} ^ {self.n} = \033[36m{self.memory_value}\033[0m'.center(85))
        return self.memory_value

    def n_root(self):
        """ Generate the n Root for the value in memory """
        self.n = self.validate_arguments(self.n)
        self.memory_value = self.memory_value ** (1 / self.n)
        print(f'\033[1m{self.memory_value} ^ (1/{self.n}) = \033[36m{self.memory_value}\033[0m'.center(85))
        return self.memory_value


if __name__ == '__main__':
    print(88 * '_')
    print(25 * ' ' + '\033[1mCALCULATOR PROGRAM\033[0m' + '\n'
          'The calculator possesses a memory which is initially set to 0.\n'
          'The operations will be performed between the current memory value and the input value.')
    memory_num, num = float(), float()  # Start of variables

    while True:
        # Menu selection
        print(88 * '_')
        print('Operation:\n(+) Addition          (-) Subtraction\n(*) Multiplication    (/) Division'
              '\n(e) Exponential       (r) n Root\n(0) Reset Memory      (1) Set Memory Value     (9) Exit program')
        print(f'(Current Memory Value: \033[94m{memory_num}\033[0m)')
        print(88 * '_')
        menu = input('Select Operation: ')

        if menu in ['+', '-', '*', '/', 'e', 'r', '0', '1', '9']:
            if menu not in ['0', '1', '9']:
                num: str = input('Enter the number: ')

            if menu == '9':
                break
            elif menu == '1':
                memory_num: str = input('Set Memory Value: ')
                memory_num: float = Calculator.validate_arguments(memory_num)

            elif menu == '0':
                memory_num = float()

            # Call for class functions
            elif menu == '+':
                memory_num = Calculator(num).add()
            elif menu == '-':
                memory_num = Calculator(num).subtract()
            elif menu == '*':
                memory_num = Calculator(num).multiply()
            elif menu == '/':
                memory_num = Calculator(num).divide()
            elif menu == 'e':
                memory_num = Calculator(num).expon()
            elif menu == 'r':
                memory_num = Calculator(num).n_root()

        else:
            print('\033[91mInvalid Menu Operation\033[0m')
