from simple_calculator_renatomarianoo.calculator import Calculator


def main():
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
    main()

