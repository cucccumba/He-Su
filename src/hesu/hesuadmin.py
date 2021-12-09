from src.utils.hesuutils import *

class Admin(object):
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.auth_voters = []

    def sign(self, auth, name):
        self.auth_voters.append(name)
        return mod_exp(auth, self.private_key[1], self.private_key[0])