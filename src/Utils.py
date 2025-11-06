import time

def sleep(t): # t: ms
    if t <= 0:
        return 0

    t0 = int(1000000 * t)
    t1 = time.perf_counter_ns()
    while True:
        t2 = time.perf_counter_ns()
        t3 = t2 - t1
        if t3 >= t0:
            break
