# made by keszinaj
import hashlib

# generate random polynomial
# f(0) = secret
# so f(x)=a_k*x^k +... +a1*x^0
import random
def random_polynomial(k):
    list_of_A = []
    for _ in range(k+1):
        list_of_A.append(random.randint(1,10000))
    print(list_of_A)
    return list_of_A

#  get random point in polynomial for secret
def calculate_random_point_in_polynomial(list_of_A, k):
    x=random.randint(1, 10000)
    y=0
    for i in range(k+1):
        y+=pow(x,i)*list_of_A[i]
    return (x,y)

# I was thiking how to multiply two polynomials.
# The idea that came to my mind was to represent them as arrays.
# For example, 10x^3+7x^2-2x+67 can be represented as [67, -2, 7, 10].
# then such an operation (2x + 7)*(6x+10) is the multiplication of [7,2,0] * [10,6,0] and then each element from the array on the left is multiplied
# by the element on the right and inserted into the array at i+1, unless we are multiplying a free element, in which case we leave it in the free space

# Note:
# for simplicity, let us assume that len(w1)>len (w2)
# and we assume that w2 will always be of the second degree, then this degree of the polynomial can change by a maximum of 1 forward
# in general, there would be more edge cases, but it is not worth implementing them
# in my example, I will multiply from left to right
def polynomial_multiplation(w1, w2):
    if len(w2) > len(w1):
        print("ERROR")
        return [0]
    w1_size = len(w1)
    w2_size = len(w2)
    solution = [0 for _ in range(w1_size + 1)]
    for i in range(w1_size):
        for j in range(w2_size):
            if i==0 and j==0:
                solution[0]=w1[i]*w2[j]
            else:
                solution[i+j]+=w1[i]*w2[j]
    if solution[w1_size] == 0:
        solution.pop() 
    return solution

# determine a_n coefficients of polynomial from Newton Polynomial form
def determining_an(a, x):
    arr = [0 for _ in range(len(a))]
    arr[0] = a[0]
    for i in range(len(x)-1):
        temp_sol = [-1*x[i], 1] # x - x_n
        for j in range(i):
           temp_sol = polynomial_multiplation(temp_sol, [-1*x[j], 1])
        for o in range(len(temp_sol)):
            arr[o] += temp_sol[o] *a[i+1]
    arr = [int(num) for num in arr]
    return(arr)    

# Lagrange interpolation to find coefficients of polynomial it uses Newton's divided differences method
# https://en.wikipedia.org/wiki/Newton_polynomial
def lagrange_polynomial(x_arr, y_arr):
    number_of_points = len(x_arr)
    arr = [[0.0 for _ in range(number_of_points)] for _ in range(number_of_points)]
    # Fullfill first column with y values
    for i in range(number_of_points):
        arr[i][0] = y_arr[i]
    # Fulfill rest colums różnicami dzielonymi
    for j in range(1, number_of_points):
        for i in range(number_of_points - j):
            numerator = arr[i+1][j-1] - arr[i][j-1]
            denominator = x_arr[i+j] - x_arr[i]
            arr[i][j] = numerator / denominator
    # Zwróć współczynniki postaci Newtona
    return arr[0]

   

# Math thoughts
# czy to ma znaczenie ze moje wspolczynniki sa zawsze liczbami calkowitymi? czy 
# przez to atakujacy moze latwiej odzyskac sekret?
# przy losowaniu x i y to ze sa one zawsze calkowite nie ma znaczenia