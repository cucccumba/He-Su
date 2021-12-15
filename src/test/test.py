from src import hesuuser as hesuuser
import time
import resources.response as res



def load_test(test_num = 100):
    voting_controller = hesuuser.VotingController(100)
    testname = 1
    t_start = time.time()
    for i in range(0, test_num):
        voting_controller.test_normal(f'{testname}')
        testname += 1
    print()
    print(f'Time for {test_num} is {time.time() - t_start}s')

# test_load performs load tests
def test_load():
    range_test = [10, 100, 1000, 2000, 5000]
    for test_num in range_test:
        load_test(test_num)
# test_all runs unit-tests
def test_all():
    voting_controller = hesuuser.VotingController(10)
    voting_controller.test_all()