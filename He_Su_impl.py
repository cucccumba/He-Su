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

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def mmi(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def _hash(x):
    return hash(x) % 200

class Voter(object):
    def __init__(self, name, public_key, private_key, mask_factor, public_adm_key):
        self.name = name
        self.public_key = public_key
        self.private_key = private_key
        self.mask_factor = mask_factor
        self.public_adm_key = public_adm_key
        self.signed_public_key = None
        self.hash_key = None
        self.secret_key = None
        
    def authorization(self):
        self.hash_key = _hash(self.public_key)
        f = mod_exp(self.mask_factor, self.public_adm_key[1], self.public_adm_key[0]) * self.hash_key
        return f
        
    def getSignedKey(self, sign):
        inverse =  mmi(self.mask_factor, self.public_adm_key[0])
        self.signed_public_key = sign * inverse
        encrypted = mod_exp(self.signed_public_key, self.public_adm_key[1], self.public_adm_key[0])
        if (encrypted == self.hash_key):
            print(self.name + ": Signed key is OK")
        return (self.public_key, self.signed_public_key)
        
    def make_vote(self, vote, secret_key):
        self.secret_key = secret_key
        encrypt_vote = mod_exp(vote, self.secret_key[1], self.secret_key[0])
        sign_vote = mod_exp(_hash(encrypt_vote), self.private_key[1], self.private_key[0])
        return (self.public_key, encrypt_vote, sign_vote)
    
    def confirm_vote(self):
        sign = mod_exp(_hash(self.secret_key), self.private_key[1], self.private_key[0])
        return (self.public_key, self.secret_key, sign)
class Admin(object):
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.auth_voters = []
    
    def sign(self, auth, name):
        self.auth_voters.append(name)
        return mod_exp(auth, self.private_key[1], self.private_key[0])
        
class Counter(object):
    def __init__(self, public_adm_key):
        self.public_adm_key = public_adm_key
        self.auth_keys = []
        self.secret_key = None
        self.votes = []
        
    def registrate(self, pair):
        signed_public_key = pair[1]
        encrypted = mod_exp(signed_public_key, self.public_adm_key[1], self.public_adm_key[0])
        if (encrypted == _hash(pair[0])):
            self.auth_keys.append(pair[0])
            print("Key registrated: ", pair[0])
            return 1
        else:
            return 0
    
    def generateSecretKey(self):
        secret_key = generateKeys(5)
        self.secret_key = secret_key
        return secret_key[0]
    
    def public_vote(self, vote):
        if (self.auth_keys.__contains__(vote[0])):
            print("Key auth: ", vote[0])
            encrypted = mod_exp(vote[2], vote[0][1], vote[0][0])
            if (encrypted == _hash(vote[1])):
                self.votes.append(vote)
                print("Initial vote ", vote)
                return 1
        return 0
    
    def public_final_vote(self, confirm):
        encrypt = mod_exp(confirm[2], confirm[0][1], confirm[0][0])
        if (encrypt == _hash(confirm[1])):
            vote = None
            print("Confirm is OK")
            for i in self.votes:
                if (i[0] == confirm[0]):
                    vote = i
            if (vote != None):
                encrypted_vote = mod_exp(vote[1], self.secret_key[1][1], self.secret_key[1][0])
                print("Vote: ", (encrypted_vote, vote[1], self.secret_key[0], vote[2], confirm[2], vote[0]))
    
def getMaskFactor():
    return random.randint(1, 50)

def vote():
    admin_keys = generateKeys(5)
    print("admin keys: ", admin_keys)
    admin = Admin(admin_keys[0], admin_keys[1])
    
    counter = Counter(admin_keys[0])
   
    voter1_keys = generateKeys(5)
    voter2_keys = generateKeys(5)
    print("voter1 keys:", voter1_keys)
    print("voter2 keys:", voter2_keys)
    mask_factor1 = getMaskFactor()
    print("mask_factor1: ", mask_factor1)
    mask_factor2 = getMaskFactor()
    print("mask_factor2: ", mask_factor2)
    voter1 = Voter("Voter1", voter1_keys[0], voter1_keys[1], mask_factor1, admin_keys[0])
    voter2 = Voter("Voter2", voter2_keys[0], voter2_keys[1], mask_factor2, admin_keys[0])
    
    f1 = voter1.authorization()
    print("f1: ", f1)
    f2 = voter2.authorization()
    print("f2: ", f2)
   
    sign1 = admin.sign(f1, voter1.name)
    print("sign1: ", sign1)
    sign2 = admin.sign(f2, voter2.name)
   
    print("sign2: ", sign2)
    print("Auth voters: ", admin.auth_voters)
    
    pair1 = voter1.getSignedKey(sign1)
    print("pair1: ", pair1)
    pair2 = voter2.getSignedKey(sign2)
    print("pair2: ", pair2)
    
    res1 = counter.registrate(pair1)
    print("res1: ", res1)
    res2 = counter.registrate(pair2)
    print("res2: ", res2)
    
    print("Auth keys: ", counter.auth_keys)
    
    secret_key = counter.generateSecretKey()
    
    vote1 = voter1.make_vote(2, secret_key)
    print("vote1: ", vote1)
    vote2 = voter2.make_vote(3, secret_key)
    print("vote2: ", vote2)
    
    if(counter.public_vote(vote1) == 1):
        confirm1 = voter1.confirm_vote()
        print("confirm1: ", confirm1)
        
        counter.public_final_vote(confirm1)
    if(counter.public_vote(vote2) == 1):
        confirm2 = voter2.confirm_vote()
        print("confirm2: ", confirm2)
        
        counter.public_final_vote(confirm2)
