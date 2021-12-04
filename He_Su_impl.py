import numpy as np
import random

def rmspp(number, attempts=28):
    """
    rmspp(n, attempts=28) -> True if n appears to be primary, else False
    rmspp: Rabin-Miller Strong Pseudoprime Test
    http://mathworld.wolfram.com/Rabin-MillerStrongPseudoprimeTest.html
    """
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    # Given an odd integer n, let n = 2**r*s+1, with s odd... 
    s = number - 1
    r = 0
    while s % 2 == 0:
        r += 1
        s /= 2
    while attempts:
        # ... choose a random integer a with 1 ≤ a ≤ n-1
        a = random.randint(1, number-1)
        # Unless a**s % n ≠ 1 ...
        if mod_exp(a, s, number) != 1:
            # ... and a**((2**j)*s) % n ≠ -1 for some 0 ≤ j ≤ r-1 
            for j in range(0, r):
                if mod_exp(a, (2**j)*s, number) == number-1:
                    break
            else:
                return False
        attempts -= 1
        continue
    # A prime will pass the test for all a.
    return True

def mod_exp(base, exponent, modulus):
    """
    mod_exp(b, e, m) -> value of b**e % m
    Calculate modular exponentation using right-to-left binary method.
    http://en.wikipedia.org/wiki/Modular_exponentiation#Right-to-left_binary_method
    """
    result = 1
    while exponent > 0:
        if (exponent & 1) == 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus
    return result

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
   
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def rabinMiller(num):
    s = num - 1
    t = 0
   
    while s % 2 == 0:
        s = s // 2
        t += 1
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                return False
            else:
                i = i + 1
                v = (v ** 2) % num
        return True
def isPrime(num):
    if (num < 2):
        return False
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
   67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
   157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 
   251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,317, 331, 337, 347, 349, 
   353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 
   457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 
   571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 
   673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
   797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 
   911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
	
    if num in lowPrimes:
        return True
    for prime in lowPrimes:
        if (num % prime == 0):
            return False
    return rabinMiller(num)
def generateLargePrime(keysize = 1024):
    while True:
    num = random.randrange(2**(keysize-1), 2**(keysize))
    if isPrime(num):
        return num

def generateKeys(keySize):
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print('Generating p prime...')
    p = generateLargePrime(keySize)
    print('Generating q prime...')
    q = generateLargePrime(keySize)
    n = p * q
	
    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break
   
    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...')
    d = findModInverse(e, (p - 1) * (q - 1))
    publicKey = (n, e)
    privateKey = (n, d)
    print('Public key:', publicKey)
    print('Private key:', privateKey)
    return (publicKey, privateKey)

def egcd(a, b):
    """
    egcd(a, b) -> d, x, y, such as d == gcd(a, b) == ax + by
    egcd is an Extended Greatest Common Divisor
    http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
    if b == 0:
        return (a, 1, 0)
    else:
        d, x, y = egcd(b, a % b)
        return d, y, x - y * (a / b)

def mmi(a, m):
    """
    mmi(a, m) -> x, such as ax % m = 1
    mmi is a Modular Multiplicative Inverse
    See http://en.wikipedia.org/wiki/Modular_multiplicative_inverse
    """
    gcd, x, q = egcd(a, m)
    if gcd != 1:
        # The a and m are not coprimes, so the inverse doesn't exist
        return None
    else:
        return (x + m) % m

class Voter(object):
    def __init__(self):
        self.open_key = None
        self.secret_key = None
        self.mask_factor = None
        
class Admin(object):
    def __init__(self):
        self.open_key = None
        self.secret_key = None
        self.mask_factor = None
        
def authorization(admin_key, key, mask):
    return admin_key * mask * hash(key)

print(generateKeys(4))