from src.hesu.hesuadmin import *
from src.hesu.hesucounter import Counter
from src.hesu.hesuvoter import *
from src.utils.hesugen import generate_keys, get_mask_factor


def vote():
    admin_keys = generate_keys(9)
    print("admin keys: ", admin_keys)
    admin = Admin(admin_keys[0], admin_keys[1])

    counter = Counter(admin_keys[0])

    voter1_keys = generate_keys(9)
    voter2_keys = generate_keys(9)
    print("voter1 keys:", voter1_keys)
    print("voter2 keys:", voter2_keys)
    mask_factor1 = get_mask_factor()
    print("mask_factor1: ", mask_factor1)
    mask_factor2 = get_mask_factor()
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

    pair1 = voter1.get_signed_key(sign1)
    print("pair1: ", pair1)
    pair2 = voter2.get_signed_key(sign2)
    print("pair2: ", pair2)

    res1 = counter.registrate(pair1)
    print("res1: ", res1)
    res2 = counter.registrate(pair2)
    print("res2: ", res2)

    print("Auth keys: ", counter.auth_keys)

    secret_key = counter.generate_secret_key()

    vote1 = voter1.make_vote(2, secret_key)
    print("vote1: ", vote1)
    vote2 = voter2.make_vote(3, secret_key)
    print("vote2: ", vote2)

    if (counter.public_vote(vote1) == 1):
        confirm1 = voter1.confirm_vote()
        print("confirm1: ", confirm1)

        counter.public_final_vote(confirm1)
    if counter.public_vote(vote2) == 1:
        confirm2 = voter2.confirm_vote()
        print("confirm2: ", confirm2)

        counter.public_final_vote(confirm2)