
def huhash(x):
    return hash(x) % 200

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


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def mmi(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
