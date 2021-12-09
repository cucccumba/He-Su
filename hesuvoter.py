from hesuutils import *

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
        self.hash_key = huhash(self.public_key)
        f = mod_exp(self.mask_factor, self.public_adm_key[1], self.public_adm_key[0]) * self.hash_key
        return f

    def getSignedKey(self, sign):
        inverse = mmi(self.mask_factor, self.public_adm_key[0])
        self.signed_public_key = sign * inverse
        encrypted = mod_exp(self.signed_public_key, self.public_adm_key[1], self.public_adm_key[0])
        if (encrypted == self.hash_key):
            print(self.name + ": Signed key is OK")
        else:
            raise Exception('Problem with signed key')
        return (self.public_key, self.signed_public_key)

    def make_vote(self, vote, secret_key):
        self.secret_key = secret_key
        encrypt_vote = mod_exp(vote, self.secret_key[1], self.secret_key[0])
        sign_vote = mod_exp(huhash(encrypt_vote), self.private_key[1], self.private_key[0])
        return (self.public_key, encrypt_vote, sign_vote)

    def confirm_vote(self):
        sign = mod_exp(huhash(self.secret_key), self.private_key[1], self.private_key[0])
        return (self.public_key, self.secret_key, sign)