
import random
import math

def uniforme(a,b):
    # x=random.randint(a,b)
    return random.uniform(a,b)

def exponencial(lanbda):
    U = random.uniform(0,1)
    res =  -math.log(U) / lanbda

    return res
    
def bernoulli(p):
    u=random.uniform(0,1)
    if u<p:
        return 0
    return 1    

