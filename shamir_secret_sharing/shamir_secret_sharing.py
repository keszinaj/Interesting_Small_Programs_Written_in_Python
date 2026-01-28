import hashlib

# TODO: kod dziala ale trzeba go posprzatac i dodac komentarze
# define full secret

# global configuration 
#define minimal number of shared secrets nessesary to put

m=2

# stopien wielomianu polynomial
degree = m-1

# secrets to genereate(must be bigger or equal m)

ss = 5


secret="alamakota"
secret_as_numer=''.join(str(x) for x in list(map(lambda x: ord(x), list(secret))))



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

#a = random_polynomial(degree)
#print(a)

def calculate_random_point_in_polynomial(list_of_A, k):
    x=random.randint(1, 10000)
    y=0
    for i in range(k+1):
        y+=pow(x,i)*list_of_A[i]
    return (x,y)
#xxx = []
#yyy = []
#for _ in range(degree+1):
#    point = calculate_random_point_in_polynomial(a, degree)
#    xxx.append(point[0])
#    yyy.append(point[1])
#    print("Point:", point)
#print("x:", xxx)
#print("y:", yyy)


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
        temp_sol = [-1*x[i], 1] # x - x_n
        for j in range(i):
           temp_sol = polynomial_multiplation(temp_sol, [-1*x[j], 1])
        #print(temp_sol)
        for o in range(len(temp_sol)):
            arr[o] += temp_sol[o] *a[i+1]
        #print(arr)
    arr = [int(num) for num in arr]
    return(arr)    


#test determining_an()
#determining_an([1, 1, 1], [1, 2,100])
#determining_an([1, 1, 1, 1], [1, 2, 3, 4])
#determining_an([4, 5, 1], [1, 2, 3])

# no niby dziala ale to trzeba jeszcze chyba wiecej przykladow porobic do testow
# no i to wszystko trzeba teraz polaczyc


def lagrange_polynomial(x_arr, y_arr):
    number_of_points = len(x_arr)
    arr = [[0.0 for _ in range(number_of_points)] for _ in range(number_of_points)]
    # Wypełnij pierwszą kolumnę wartościami y
    for i in range(number_of_points):
        arr[i][0] = y_arr[i]
    # Wypełnij pozostałe kolumny różnicami dzielonymi
    for j in range(1, number_of_points):
        for i in range(number_of_points - j):
            numerator = arr[i+1][j-1] - arr[i][j-1]
            denominator = x_arr[i+j] - x_arr[i]
            arr[i][j] = numerator / denominator
    # Zwróć współczynniki postaci Newtona
    return arr[0]

   



#test Lagrange_polynomia
#lagrange_polynomial([1, 2, 3], [4, 9, 16])


# test wszystkiego razem
# okej to dobrze dziala dla wielomianow stopnia 1, 2, 3 dla 4 juz sie psuje
a = random_polynomial(degree)
secret_key = "".join(str(i) for i in a)
#to meke it 32 bytes as chacha20 require
res = hashlib.md5(secret_key.encode())
secret_key=res.hexdigest()

print(secret_key)
print(len(secret_key))  # 32
xxx = []
yyy = []
for _ in range(degree+1):
    point = calculate_random_point_in_polynomial(a, degree)
    xxx.append(point[0])
    yyy.append(point[1])
    print("Point:", point)



ta = lagrange_polynomial(xxx, yyy)
print(determining_an(ta, xxx))

#key format of the chacha20 will be
# n $ nonce $ x_coordinate $ y_coordinate


# Math thoughts
# czy to ma znaczenie ze moje wspolczynniki sa zawsze liczbami calkowitymi? czy 
# przez to atakujacy moze latwiej odzyskac sekret?
# przy losowaniu x i y to ze sa one zawsze calkowite nie ma znaczenia