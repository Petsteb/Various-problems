def solve_equations(equation: str, possible_variables: list[str]) -> str:
    def validate_input() -> bool:
        if not equation:
            return False
        if '=' not in equation:
            return False
        return True

    def break_string(s: str) -> list[str]:
        # breaking a part of an equation into its components
        components: list[str] = []
        i = 0
        while i < len(s):
            components.append(s[i])
            if components[-1] not in ['+', '-']:
                components[-1] = '+' + s[i]
            while i < len(s) - 1 and s[i + 1] not in ['+', '-']:
                components[-1] += s[i + 1]
                i += 1
            i += 1
        return components

    def parse_components(components: list[str], nth_equation: int, side: str) -> None:
        # parsing the components of an equation
        for component in components:
            letter = [i for i in component if i.isalpha()]
            if letter:
                letter = letter[0]
                factor = int(component.split(letter)[0][1:] or '1')
                factor *= -1 if component[0] == '-' else 1
                factor *= -1 if letter in constants else 1
                factor *= -1 if side == 'right' else 1
                matrix[nth_equation][variables_and_constants.index(letter)] += factor
            else:
                matrix[nth_equation][-1] += -int(component) if side == 'left' else int(component)

    def gauss_jordan_elimination() -> None:
        for i in range(len(matrix)):
            if matrix[i][i] == 0:
                for j in range(i + 1, len(matrix)):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
            if matrix[i][i] != 0:
                matrix[i] = [matrix[i][j] / matrix[i][i] for j in range(len(matrix[0]))]
                for j in range(len(matrix)):
                    if j != i:
                        matrix[j] = [matrix[j][k] - matrix[i][k] * matrix[j][i] for k in range(len(matrix[0]))]

    def get_result() -> str:
        result = ''
        for var in variables:
            res = ''
            line_of_var = [i for i in range(len(matrix)) if matrix[i][variables_and_constants.index(var)] == 1]
            if line_of_var != []:
                line_of_var = line_of_var[0]
                if matrix[line_of_var][-1] != 0.0:
                    res += str(int(matrix[line_of_var][-1]))
                for c in constants:
                    if matrix[line_of_var][variables_and_constants.index(c)] != 0.0:
                        if int(matrix[line_of_var][variables_and_constants.index(c)]) == -1:
                            res += '-' + c
                        elif int(matrix[line_of_var][variables_and_constants.index(c)]) == 1:
                            if res == '':
                                res += c
                            else:
                                res += '+' + c
                        else:
                            if res == '':
                                res += str(int(matrix[line_of_var][variables_and_constants.index(c)])) + c
                            else:
                                if '-' not in str(int(matrix[line_of_var][variables_and_constants.index(c)])):
                                    res += '+' + str(int(matrix[line_of_var][variables_and_constants.index(c)])) + c
                                else:
                                    res += str(int(matrix[line_of_var][variables_and_constants.index(c)])) + c
                if res == '':
                    res = '0'
            result += var + '=' + res + ', '
        return result[:-2]

    if not validate_input():
        return 'Invalid input'
    
    variables = [i for i in possible_variables if i in equation]
    constants = sorted(list(set([i for i in equation if i.isalpha() and i not in possible_variables])))
    variables_and_constants = variables + constants
    no_variables = len(variables)
    no_constants = len(constants)

    equation = equation.replace('\n', '')
    equation = equation.replace(' ', '')
    equations = equation.split(';')
    # in matrix[ntx_equation] are stored first the factors of variables and consttants and lastly the result
    # constants are the letters in the equation that are not x or y
    matrix: list[list[int]] = [[0 for _ in range(no_variables + no_constants + 1)] for _ in range(len(equations))]
    
    for eq, nth_equation in zip(equations, range(len(equations))):
        eq = eq.strip()
        eq = eq.split('=') 

        # parsing the left part of the equation
        left = break_string(eq[0])
        parse_components(left, nth_equation, 'left')

        # parsing the second part of the equation
        right = break_string(eq[1])
        parse_components(right, nth_equation, 'right')


    # gauss jordan elimination
    gauss_jordan_elimination()

    # getting the result
    return get_result()
    
# these letters can only be variables, the other letters are considered constants
possible_variables = ['x', 'y']

equation1 = 'x+y=10 ; x-y=4'
equation2 = 'x+a=4'
equation3 = 'y-6b=0'
equation4 = 'x+y=c ; 2x-y=2c'
equation5 = 'x+y=2a-3b ; x+2y=0'


# print(solve_equations(equation1))
assert solve_equations(equation1, possible_variables) == 'x=7, y=3'
# print(solve_equations(equation2))
assert solve_equations(equation2, possible_variables) == 'x=4-a'
# print(solve_equations(equation3))
assert solve_equations(equation3, possible_variables) == 'y=6b'
# print(solve_equations(equation4))
assert solve_equations(equation4, possible_variables) == 'x=c, y=0'
# print(solve_equations(equation5))
assert solve_equations(equation5, possible_variables) == 'x=4a-6b, y=-2a+3b'