import numpy as np
import random as rd
from datetime import datetime

def is_prime(x):
    if x < 2:
        return False

    for n in range(2, int(np.sqrt(x) + 1)):
        if x % n == 0:
            return False

    return True

def primes_in_range(x, y):
    prime_list = []

    for n in range(x, y):
        if is_prime(n):
            prime_list.append(n)
    
    return prime_list

def get_two_random_primes(x, y):
    prime_list = primes_in_range(x, y)
    return rd.sample(prime_list, 2)