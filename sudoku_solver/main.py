# made by keszinaj
'''
    It's simple sudoku solver.
'''
import math
from testy import sudoku_input_hard, sudoku_input_wrong, invalidBoard

'''
    Row can only contain each number from 1 to 9 once. This function check it.
'''
def valid_row(n, sudoku_arr, row):
    return not n in sudoku_arr[row]

'''
    Collumn can only contain each number from 1 to 9 once. This functions check it.
'''
def column_as_array(sudoku_arr, num):
    r = []
    for i in range(9):
        r.append(sudoku_arr[i][num])
    return r
def valid_column(n, sudoku_arr, column):
    return not n in column_as_array(sudoku_arr, column)

'''
    Square can only contain each number from 1 to 9 once. This functions check it.
'''
def square_as_arr(sudoku_arr, r, c):
    c = math.floor(c / 3) 
    r = math.floor( r / 3)
    arr = []
    for i in range(3):
        for j in range(3):
            arr.append(sudoku_arr[i + (3 * r)][j + ( 3 * c)])
    return arr
def valid_square(n, sudoku_arr, row, column):
    return not n in square_as_arr(sudoku_arr, row, column)

'''
    Backtracking algorithm which tries to complete sudoku.
'''
def backtracking_algorithm(sudoku, row, column):
    if row == 9:
        return True
    if sudoku[row][column] == 0:
            for n in range(1, 10):
                if valid_column(n, sudoku, column) and valid_row(n, sudoku, row) and valid_square(n, sudoku, row, column):
                    sudoku[row][column] = n
                    column += 1
                    if column == 9:
                        column = 0
                        row += 1
                    if backtracking_algorithm(sudoku, row, column):
                        return True
                    if column == 0:
                        row -= 1
                        column = 8
                    else:
                        column-=1
                    if n == 9:
                        sudoku[row][column] = 0
                        return False
                elif n == 9:
                    sudoku[row][column] = 0
                    return False
    else:
        column += 1
        if column == 9:
            column = 0
            row += 1
        return backtracking_algorithm(sudoku, row, column)

'''
    Pretty print sudoku in console.
'''
def prettyprint(sudoku):
    if sudoku is None:
        print("Solution doesn't exist.")
    else:
        print("+---" * 9 + "+")
        for row in sudoku:
            print(("|" + " {} |" * 9 + "\n" + "+---" * 9 + "+").format(*[i for i in row]))
        
'''
    main function 
'''
def sudoku_solver(sudoku):
    s = backtracking_algorithm(sudoku, 0, 0)
    if s:
      return sudoku
    else:
        return None

    
if __name__ == "__main__":
    prettyprint(sudoku_solver(sudoku_input_hard))
    prettyprint(sudoku_solver(sudoku_input_wrong))
    prettyprint(sudoku_solver(invalidBoard))
      