import threading
import time


num_iterations = 100

current_iteration = 0

lock = threading.Lock()

def thread_function():
    global current_iteration
    while current_iteration < num_iterations: # 第一次验证
        with lock:
            if current_iteration < num_iterations: # 第二次验证
                iteration = current_iteration
                current_iteration += 1
                # using iteration
                # Long running time code 
                time.sleep(0.1)

num_threads = 4
threads = []
for i in range(num_threads):
    t = threading.Thread(target=thread_function)
    threads.append(t)

tic = time.time()
# Fire all threads up
for t in threads:
    t.start()

# wait for all threads
for t in threads:
    t.join()
toc = time.time()
print("Time elapsed %.2f" % (toc - tic))