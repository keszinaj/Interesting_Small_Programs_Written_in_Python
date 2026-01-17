# define full secret
secret="alamakota"
secret_as_numer=''.join(str(x) for x in list(map(lambda x: ord(x), list(secret))))

#define minimal number of shared secrets nessesary to put

m=4

# stopien wielomianu polynomial
degree = m-1

# secrets to genereate(must be bigger or equal m)

ss = 5

# generate random polynomial
# f(0) = secret
# so f(x)=a_k*x^k +... +a1*x^0
import random
def random_polynomial(k):
    list_of_A = []
    for q in range(k+1):
        list_of_A.append(random.randint(1,10000))
    print(list_of_A)
    return list_of_A

#a = random_polynomial(degree)


def calculate_random_point_in_polynomial(list_of_A, k):
    x=random.randint(1,10000)
    y=0
    for i in range(k+1):
        y+=pow(x,i)*list_of_A[i]
    return y




# zastanawialem sie jak pomnozyc dwa wielomiany
# pomysl ktory mi przyszedl do glowy to przedstawic je jako tablice
# np. 10x^3+7x^2-2x+67 mozna przedstawic jako [67, -2, 7, 10]
# wtedy takie działanie (2x + 7)*(6x+10) to mnożenie [7,2,0] * [10,6,0] i wtedy kazdy element z tej tablicy z lewej mnozymy
# przez element z prawej i wstawiamy to tablei w i+1 chyba ze mnożymy element wolny wtedy zostawiamy to na wolnym miejscu

#UWAGA
# na chwile dla latwosci przyjmijmy ze len(w1)>len(w2)
# no i zakladamy ze w2 zawsze bedzie drugiego stopnia wtedy ten stopien wilomianu moze sie zemienic max 1 do przedy
# w ogolnym przypadku byloby wiecej edge casow, ale no nie oplaca sie teog implementowac
# w moim przykladzie bede mnozyl od lewej do prawej
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
   # print(solution)
    return solution

#print(polynomial_multiplation([2, -3, 1], [-3, 1]))

def determining_an(a, x):
    arr = [0 for _ in range(len(a))]
    arr[0] = a[0]
    for i in range(len(x)-1):
        temp_sol = [-1*x[i], 1] #x -x_n
        for j in range(i):
           temp_sol = polynomial_multiplation(temp_sol, [-1*x[j], 1])
        print(temp_sol)
        for o in range(len(temp_sol)):
            arr[o] += temp_sol[o] *a[i+1]
        print(arr)
    return(arr)    


#test determining_an()
#determining_an([1, 1, 1], [1, 2,100])
#determining_an([1, 1, 1, 1], [1, 2, 3, 4])
determining_an([4, 5, 1], [1, 2, 3])


def lagrange_polynomial(x_arr, y_arr):
    number_of_points = len(x_arr)
    arr = [[0 for _ in range(number_of_points)] for _ in range(number_of_points)]
    print(arr)
    #wypelnij skos
    for i in range(number_of_points):
        arr[i][i] = y_arr[i]
    print(arr)
    # wypelniamy nastepne skosy
    for j in range(1, number_of_points):
        for i in range(number_of_points-1):
            print("i:", i, "j:", j)
            numerator = arr[i+1][j]-arr[i][j-1]
            denominator = x_arr[j] - x_arr[i]
            sol= numerator/denominator
            print("numerator",numerator, "denominator:",denominator)
            arr[i][j]=sol
            j+=1
            if j==len(x_arr):
                break
    print(arr)
   



#test Lagrange_polynomia
#lagrange_polynomial([1, 2, 3], [4, 9, 16])