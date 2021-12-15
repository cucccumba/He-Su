from src.utils.hesugen import generate_keys
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
        if encrypted == huhash(pair[0]):
            self.auth_keys.append(pair[0])
            #print("Key registrated: ", pair[0])
            return 1
        else:
            raise Exception(REGISTRATION_FAILED_EXCEPTION)

    def generate_secret_key(self):
        secret_key = generate_keys(9)
        self.secret_key = secret_key
        return secret_key[0]

    def public_vote(self, vote):
        if self.auth_keys.__contains__(vote[0]):
            #print("Key auth: ", vote[0])
            encrypted = mod_exp(vote[2], vote[0][1], vote[0][0])
            if encrypted == huhash(vote[1]):
                self.votes.append(vote)
                #print("Initial vote ", vote)
                return 1
            print(f'Encrypted is {encrypted}, huhash is {huhash((vote[1]))}')
            raise Exception(PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_EXCEPTION) #PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_EXCEPTION
        raise Exception(PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_EXCEPTION)

    def public_final_vote(self, confirm):
        encrypt = mod_exp(confirm[2], confirm[0][1], confirm[0][0])
        if encrypt == huhash(confirm[1]):
            vote = None
            #print("Confirm is OK")
            for i in self.votes:
                if i[0] == confirm[0]:
                    vote = i
            if vote is not None:
                encrypted_vote = mod_exp(vote[1], self.secret_key[1][1], self.secret_key[1][0])
                return encrypted_vote
                #print("Vote: ", (encrypted_vote, vote[1], self.secret_key[0], vote[2], confirm[2], vote[0]))
        raise Exception(FINAL_VOTE_FAILED_EXCEPTION)