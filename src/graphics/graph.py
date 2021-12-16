import time
from src import hesuuser

def timer():
  time_array = []
  for i in range(2, 20, 1):
    t_start = time.time()
    hesuuser.vote0(i)
    time_array.append(time.time() - t_start)
  return time_array
