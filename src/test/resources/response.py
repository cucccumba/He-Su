from src.utils.hesuutils import *


NORMAL_TEST_TYPE = 'normal'
ADMIN_SIGN_FAILED_TEST_TYPE = 'admin_sign_failed'
VOTER_KEY_FAILED_TEST_TYPE = 'voter_key_failed'
VOTER_ALREADY_REGISTERED_TEST_TYPE = 'voter_already_registered'
REGISTRATION_FAILED_TEST_TYPE = 'registration_failed'
#PUBLIC_VOTE_FAILED_TEST_TYPE = 'public_vote_failed'
PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_TEST_TYPE = 'public_vote_auth_hash_failed'
PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_TEST_TYPE = 'public_vote_auth_key_does_not_present'
FINAL_VOTE_FAILED_TEST_TYPE = 'final_vote_failed'
RABIN_MILLER_FAILED_EXCEPTION = 'Rabin miller failed'

test_types = [NORMAL_TEST_TYPE, VOTER_ALREADY_REGISTERED_TEST_TYPE, VOTER_KEY_FAILED_TEST_TYPE,
              REGISTRATION_FAILED_TEST_TYPE, PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_TEST_TYPE,
              PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_TEST_TYPE, FINAL_VOTE_FAILED_TEST_TYPE]

exception_types = [NO_EXCEPTION, VOTER_ALREADY_REGISTERED_EXCEPTION, VOTER_KEY_FAILED_EXCEPTION,
                   REGISTRATION_FAILED_EXCEPTION, PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_EXCEPTION,
                   PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_EXCEPTION, FINAL_VOTE_FAILED_EXCEPTION]

voter_unique_names = ['1', '1', '2', '3', '4', '5', '6']

class Response(object):
    is_admin_sign_ok = False
    is_registration_ok = False
    is_public_vote_ok = False
    is_final_vote_ok = False
    is_voter_key_signed_ok = False
    err = ''


