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
a = random_polynomial(degree)
a[0] = secret_as_number

def calculate_random_point_in_polynomial(list_of_A, k):
    x=random.randint(1,10000)
    y=0
    for i in range(k+1):
        y+=pow(x,i)*list_of_A[i]
    return y






