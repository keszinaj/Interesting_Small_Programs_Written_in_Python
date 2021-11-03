import math
# hard input
sudoku_input = ([8, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 3, 6, 0, 0, 0, 0, 0],
               [0, 7, 0, 0, 9, 0, 2, 0, 0],
               [0, 5, 0, 0, 0, 7, 0, 0, 0],
               [0, 0, 0, 0, 4, 5, 7, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 3, 0],
               [0, 0, 1, 0, 0, 0, 0, 6, 8],
               [0, 0, 8, 5, 0, 0, 0, 1, 0],
               [0, 9, 0, 0, 0, 0, 4, 0, 0])
def valid_row(n, sudoku_arr, row):
    return not n in sudoku_arr[row]

# take number in row
def column_as_array(sudoku_arr, num):
    r = []
    for i in range(9):
        r.append(sudoku_arr[i][num])
    return r

def valid_column(n, sudoku_arr, column):
    return not n in column_as_array(sudoku_arr, column)

def square_as_arr(sudoku_arr, r, c):
    c = math.floor(c / 3) # sprawdz czzy nie ma błedu typu chyba nie
    r = math.floor( r / 3)
    arr = []
    for i in range(3):
        for j in range(3):
            arr.append(sudoku_arr[i + (3 * r)][j + ( 3 * c)])
    return arr
def valid_square(n, sudoku_arr, row, column):
    return not n in square_as_arr(sudoku_arr, row, column)
def sol(sudoku, row, column):
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
                    if sol(sudoku, row, column):
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
        return sol(sudoku, row, column)
 
def solver(sudoku):
    s = sol(sudoku, 0, 0)
    print(sudoku)
    return s

print(solver(sudoku_input))
   