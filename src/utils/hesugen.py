from src.utils.hesuutils import *
import random

def generateLargePrime(keysize=1024):
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        if isPrime(num):
            return num


def generateKeys(keySize):
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    p = generateLargePrime(keySize)
    q = generateLargePrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    d = findModInverse(e, (p - 1) * (q - 1))
    publicKey = (n, e)
    privateKey = (n, d)
    return (publicKey, privateKey)


def getMaskFactor():
    return random.randint(1, 50)