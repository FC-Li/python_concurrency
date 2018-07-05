import threading
import numpy as np
from skimage import io
import os

directory = "images/"
filenames = [name for name in os.listdir(directory)]
num_images = len(filenames)

images = np.empty((num_images, 256, 256, 3))
current_image_index = 0
lock = threading.Lock()

def load_images(directory):
    global current_image_index
    global images
    while current_image_index < num_images: # 第一次验证
        with lock:
            if current_image_index < num_images: # 第二次验证
                index = current_image_index
                current_image_index += 1
            else:
                break

        image = io.imread(os.path.join(directory, filenames[index]))

        with lock:
            images[index] = image

num_threads = 4
threads = []
for i in range(num_threads):
    t = threading.Thread(target=load_images, args=(directory, ))
    threads.append(t)

# Fire all threads up
for t in threads:
    t.start()

# wait for all threads
for t in threads:
    t.join()