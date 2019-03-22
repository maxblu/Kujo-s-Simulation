
import random

def uniforme(a,b):
    x=random.randint(a,b)
    return x

def normal(miu,landa):
    return random.normalvariate(miu,landa)
    

def exponencial(landa):
    return random.expovariate(landa)

def bernoulli(p):
    return random.randint(0,1)