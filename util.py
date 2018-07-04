import time

limit_1 = 20
limit_2 = 100

registered_keys = {}

def do_slowly(key=None, initial_count=0):
    started = time.time()

    if key in registered_keys:
        count, delta = registered_keys[key]
    else:
        count = initial_count
        delta = []

    if delta:
        #print(count, len(delta), max(delta[-limit_1:]) - min(delta[-limit_1:]), '/1 \t', max(delta[-limit_2:]) - min(delta[-limit_2:]), '/120')

        if max(delta[-limit_1:]) - min(delta[-limit_1:]) < 1 and len(delta) >= limit_1:
            print('nap')
            time.sleep(1)
            delta[-1] += 1
        if max(delta[-limit_2:]) - min(delta[-limit_2:]) < 120 and len(delta) >= limit_2:
            print('sleep')
            sleep_time = 120 - (max(delta[-limit_2:]) - min(delta[-limit_2:])) + 1
            time.sleep(sleep_time)
            delta[-1] += sleep_time
        if len(delta) > max(limit_1, limit_2):
            delta.remove(delta[0])

    registered_keys[key] = count + 1, delta
    delta.append(time.time())
