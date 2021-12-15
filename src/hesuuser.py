from src.hesu.hesuadmin import *
from src.hesu.hesucounter import Counter
from src.hesu.hesuvoter import *
from src.utils.hesugen import generate_keys, get_mask_factor
from src.test.resources.response import *


# VotingController contains general functions to imitate HeSu process
# Covers it with unit-tests and adds an ability to test random inputs
# vote(self, voter_name, test_type = 'normal') simulates voting.
# If input information is flawed, returns Respone with .err field filled with error data.
# You can use test_type field to emulate certain error.
# test_all() starts unit-tests
# test_{test_name} can be used to trigger certain unit-test type.
class VotingController(object):
    def __init__(self, key_gen_num):
        self.key_gen_num = key_gen_num
        self.admin_keys = generate_keys(key_gen_num)
        self.admin = Admin(self.admin_keys[0], self.admin_keys[1])
        self.voter_count = 0
        self.counter = Counter(self.admin_keys[0])

    def vote(self, voter_name, test_type = 'normal') -> Response: # vote_type is for test purpose only
        assert isinstance(voter_name, str), "Voter name should be string"
        #self.admin = Admin(self.admin_keys[0], self.admin_keys[1])
        #self.counter = Counter(self.admin_keys[0])
        resp = Response
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])

        auth = voter.authorization()
        try:
            sign = self.admin.sign(auth, voter_name)
            resp.is_admin_sign_ok = True

            resp.sign = sign
            voter_signed_key = voter.get_signed_key(sign)
            resp.is_voter_key_signed = True


            self.counter.registrate(voter_signed_key)
            resp.is_registration_ok = True

            secret_key = self.counter.generate_secret_key()
            resp.secret_key = secret_key
            voting_keys = voter.make_vote(self.voter_count, secret_key)
            self.voter_count += 1

            resp.voting_keys = voting_keys
            self.counter.public_vote(voting_keys)
            resp.is_public_vote_ok = True

            voter_confirmation = voter.confirm_vote()
            resp.voter_confirmation = voter_confirmation
            encrypted = self.counter.public_final_vote(voter_confirmation)
            resp.is_final_vote_ok = True
            resp.encrypted = encrypted
        except BaseException as err:
            resp.err = err

        return resp

    def main_block(self, test_type, voter, voter_name):
        resp = Response
        auth = voter.authorization()
        try:
            if test_type == VOTER_ALREADY_REGISTERED_TEST_TYPE:
                self.admin.sign(auth, voter_name)
            sign = self.admin.sign(auth, voter_name)
            resp.is_admin_sign_ok = True

            if test_type == VOTER_KEY_FAILED_TEST_TYPE:
                sign += 1
            resp.sign = sign
            voter_signed_key = voter.get_signed_key(sign)
            resp.is_voter_key_signed = True

            if test_type == REGISTRATION_FAILED_TEST_TYPE:
                voter_signed_key = tuple([tuple([voter_signed_key[0][0] + 1, voter_signed_key[0][1] + 1]), voter_signed_key[1] + 1])

            if not test_type == PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_TEST_TYPE:
                self.counter.registrate(voter_signed_key)
            resp.is_registration_ok = True

            secret_key = self.counter.generate_secret_key()
            resp.secret_key = secret_key
            voting_keys = voter.make_vote(self.voter_count, secret_key)
            self.voter_count += 1
            if test_type == PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_TEST_TYPE:
                voting_keys = tuple([tuple([voting_keys[0][0], voting_keys[0][1]]), voting_keys[1] + 5, voting_keys[2] + 5])

            resp.voting_keys = voting_keys
            self.counter.public_vote(voting_keys)
            resp.is_public_vote_ok = True

            voter_confirmation = voter.confirm_vote()
            resp.voter_confirmation = voter_confirmation
            if test_type == FINAL_VOTE_FAILED_TEST_TYPE:
                voter_confirmation = tuple([tuple([voter_confirmation[0][0] + 1, voter_confirmation[0][1] + 1]), tuple([voter_confirmation[1][0] + 1, voter_confirmation[1][1] + 1]), voter_confirmation[2]])
            encrypted = self.counter.public_final_vote(voter_confirmation)
            resp.is_final_vote_ok = True
            resp.encrypted = encrypted
        except BaseException as err:
            resp.err = err
        return resp

    # runs all unit tests at once
    def test_all(self):
        self.test_normal('1')
        self.test_voter_already_registered('2')
        self.test_voter_key_failed('3')
        self.test_registration_failed('4')
        self.test_public_vote_auth_key_hash_failed('5')
        self.test_public_vote_auth_key_not_present('6')
        self.test_final_vote_failed('7')


    def test_normal(self, voter_name):
        assert isinstance(voter_name, str), "Voter name should be string"
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])
        err = self.main_block(NORMAL_TEST_TYPE, voter, voter_name).err
        if err != '':
            print(err)
        #assert self.main_block(NORMAL_TEST_TYPE, voter, voter_name).err == ''

    def test_voter_already_registered(self, voter_name):
        assert isinstance(voter_name, str), "Voter name should be string"
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])
        assert self.main_block(VOTER_ALREADY_REGISTERED_TEST_TYPE, voter, voter_name).err.__str__() == VOTER_ALREADY_REGISTERED_EXCEPTION

    def test_voter_key_failed(self, voter_name):
        assert isinstance(voter_name, str), "Voter name should be string"
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])
        assert self.main_block(VOTER_KEY_FAILED_TEST_TYPE, voter, voter_name).err.__str__() == VOTER_KEY_FAILED_EXCEPTION

    def test_registration_failed(self, voter_name):
        assert isinstance(voter_name, str), "Voter name should be string"
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])
        assert self.main_block(REGISTRATION_FAILED_TEST_TYPE, voter, voter_name).err.__str__() == REGISTRATION_FAILED_EXCEPTION

    def test_public_vote_auth_key_hash_failed(self, voter_name):
        assert isinstance(voter_name, str), "Voter name should be string"
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])
        assert self.main_block(PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_TEST_TYPE, voter, voter_name).err.__str__() == PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_EXCEPTION

    def test_public_vote_auth_key_not_present(self, voter_name):
        assert isinstance(voter_name, str), "Voter name should be string"
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])
        assert self.main_block(PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_TEST_TYPE, voter, voter_name).err.__str__() == PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_EXCEPTION

    def test_final_vote_failed(self, voter_name):
        assert isinstance(voter_name, str), "Voter name should be string"
        voter_keys = generate_keys(self.key_gen_num)
        mask_factor = get_mask_factor()
        voter = Voter(voter_name, voter_keys[0], voter_keys[1], mask_factor, self.admin_keys[0])
        assert self.main_block(FINAL_VOTE_FAILED_TEST_TYPE, voter, voter_name).err.__str__() == FINAL_VOTE_FAILED_EXCEPTION

def vote():
    admin_keys = generate_keys(9) #
    print("admin keys: ", admin_keys)
    admin = Admin(admin_keys[0], admin_keys[1]) #

    counter = Counter(admin_keys[0])

    voter1_keys = generate_keys(9) # Ключи избирателя (1.0)
    voter2_keys = generate_keys(9)
    print("voter1 keys:", voter1_keys)
    print("voter2 keys:", voter2_keys)
    mask_factor1 = get_mask_factor() # Маскирующий множитель (1.1)
    print("mask_factor1: ", mask_factor1)
    mask_factor2 = get_mask_factor() #
    print("mask_factor2: ", mask_factor2)
    voter1 = Voter("Voter1", voter1_keys[0], voter1_keys[1], mask_factor1, admin_keys[0])
    voter2 = Voter("Voter2", voter2_keys[0], voter2_keys[1], mask_factor2, admin_keys[0])

    f1 = voter1.authorization()
    print("f1: ", f1)
    f2 = voter2.authorization()
    print("f2: ", f2)

    sign1 = admin.sign(f1, voter1.name) # Проверка приемлимости избирателя (2.2), возвращать
    print("sign1: ", sign1)
    sign2 = admin.sign(f2, voter2.name)

    print("sign2: ", sign2)
    print("Auth voters: ", admin.auth_voters) # Список авторизованных пользователей (2.3), возвращать

    pair1 = voter1.get_signed_key(sign1) # (3) - избиратель проверяет равенство
    print("pair1: ", pair1)
    pair2 = voter2.get_signed_key(sign2)
    print("pair2: ", pair2)

    res1 = counter.registrate(pair1) # 5
    print("res1: ", res1)
    res2 = counter.registrate(pair2)
    print("res2: ", res2)

    print("Auth keys: ", counter.auth_keys)

    secret_key = counter.generate_secret_key()

    vote1 = voter1.make_vote(2, secret_key)
    print("vote1: ", vote1)
    vote2 = voter2.make_vote(3, secret_key)
    print("vote2: ", vote2)

    if counter.public_vote(vote1) == 1:
        confirm1 = voter1.confirm_vote()
        print("confirm1: ", confirm1)

        counter.public_final_vote(confirm1)
    if counter.public_vote(vote2) == 1:
        confirm2 = voter2.confirm_vote()
        print("confirm2: ", confirm2)

        counter.public_final_vote(confirm2)