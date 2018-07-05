import threading
import time
import pandas as pd 
import matplotlib.pyplot as plt 

def feak_thread_function():
    global current_iteration
    while current_iteration < num_iterations: # 第一次验证
        with lock:
            if current_iteration < num_iterations: # 第二次验证
                iteration = current_iteration
                current_iteration += 1
                # using iteration
                # Long running time code 
                time.sleep(0.001)

def real_thread_function():
    global current_iteration
    while current_iteration < num_iterations: # 第一次验证
        with lock:
            if current_iteration < num_iterations: # 第二次验证
                iteration = current_iteration
                current_iteration += 1
            else:
                break

        # using iteration
        # Long running time code 
        time.sleep(0.001)

        with lock:
            pass

stats = {}

times_of_real = []
for num_threads in range(1, 33):
    num_iterations = 100
    current_iteration = 0
    lock = threading.Lock()
    threads = []
    tic = time.time()

    for i in range(num_threads):
        t = threading.Thread(target=real_thread_function)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    toc = time.time()
    times_of_real.append(toc-tic)

times_of_feak = []
for num_threads in range(1, 33):
    num_iterations = 100
    current_iteration = 0
    lock = threading.Lock()
    threads = []

    tic = time.time()
    for i in range(num_threads):
        t = threading.Thread(target=feak_thread_function)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    toc = time.time()
    times_of_feak.append(toc-tic)

stats["real_multi_threading"] = times_of_real
stats["feak_multi_threading"] = times_of_feak

fig = plt.figure(figsize=(10, 6))
ax = plt.subplot(111)
pd.DataFrame(stats).plot(ax=ax)
plt.xlabel("Number of threads")
plt.ylabel("Elapsed time /s")
# plt.show()
fig.savefig("compare.png")