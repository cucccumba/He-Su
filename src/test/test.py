from src import hesuuser as hesuuser
import resources.response as res



def tst():
    voting_controller = hesuuser.VotingController(10)
    for i in range(0, len(res.test_types)):
        resp = voting_controller.test_vote(res.voter_unique_names[i], res.test_types[i])
        assert resp.err == res.exception_types[i]

# test_all runs unit-tests
def test_all():
    voting_controller = hesuuser.VotingController(10)
    voting_controller.test_all()