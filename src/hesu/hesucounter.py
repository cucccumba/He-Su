from src.utils.hesugen import generateKeys
from src.utils.hesuutils import *

class Counter(object):
    def __init__(self, public_adm_key):
        self.public_adm_key = public_adm_key
        self.auth_keys = []
        self.secret_key = None
        self.votes = []

    def registrate(self, pair):
        signed_public_key = pair[1]
        encrypted = mod_exp(signed_public_key, self.public_adm_key[1], self.public_adm_key[0])
        if (encrypted == huhash(pair[0])):
            self.auth_keys.append(pair[0])
            print("Key registrated: ", pair[0])
            return 1
        else:
            return 0

    def generateSecretKey(self):
        secret_key = generateKeys(9)
        self.secret_key = secret_key
        return secret_key[0]

    def public_vote(self, vote):
        if (self.auth_keys.__contains__(vote[0])):
            print("Key auth: ", vote[0])
            encrypted = mod_exp(vote[2], vote[0][1], vote[0][0])
            if (encrypted == huhash(vote[1])):
                self.votes.append(vote)
                print("Initial vote ", vote)
                return 1
        return 0

    def public_final_vote(self, confirm):
        encrypt = mod_exp(confirm[2], confirm[0][1], confirm[0][0])
        if (encrypt == huhash(confirm[1])):
            vote = None
            print("Confirm is OK")
            for i in self.votes:
                if (i[0] == confirm[0]):
                    vote = i
            if (vote != None):
                encrypted_vote = mod_exp(vote[1], self.secret_key[1][1], self.secret_key[1][0])
                print("Vote: ", (encrypted_vote, vote[1], self.secret_key[0], vote[2], confirm[2], vote[0]))