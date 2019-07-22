import multiprocessing
import random
import traceback
import time

def worker():
    i = random.randint(0,4)
    if i<1:
        return 0
    else:
        return i

def f(x):
    try:
        time.sleep(random.randint(0,4))
        return 1 / worker()
    except Exception as e:
        print('Caught exception in worker thread (x = %d):' % x)
    
        # This prints the type, value, and stack trace of the
        # current exception being handled.
        traceback.print_exc()
    
#        print()
        raise e

if __name__ == '__main__':
    try:
      with multiprocessing.Pool(5) as pool:
        print(pool.map(f, range(5)))
    except Exception as e:
        print (e.__str__)
