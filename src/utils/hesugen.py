from src.utils.hesuutils import *
import random


def generate_large_prime(keysize=1024):
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        if is_prime(num):
            return num


def generate_keys(key_size):
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    p = generate_large_prime(key_size)
    q = generate_large_prime(key_size)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** (key_size))
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    d = find_mod_inverse(e, (p - 1) * (q - 1))
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


def get_mask_factor():
    return random.randint(1, 50)
