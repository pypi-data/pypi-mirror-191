from PIL import Image
import io
import json
import logging
from logging import FileHandler
import pickle 




def get_logger(logger_path: str = './logger',
               logger_name: str = 'video-fps',
               drop_console_handler: bool = False):

    # initialize logger
    logger = logging.getLogger(logger_name)
    # set level: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = FileHandler(filename=logger_path)


    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if not drop_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def multiprocess_pool(process_func: callable,
                      args: list,
                      num_parallel: int = 20):
    from multiprocessing import Process
    pool = {i: None for i in range(num_parallel)}

    for arg in args:
        while True:
            search = False
            for i in range(num_parallel):
                if (pool[i] is None) or (not pool[i].is_alive()):
                    pool[i] = Process(target=process_func, args=arg)
                    pool[i].start()
                    search = True
                    break
            if search:
                break

    for i in range(num_parallel):
        if pool[i] is not None:
            pool[i].join()


def read_bytes(file_name, start_num, size, is_image=True):
    with open(file_name, 'rb') as f:
        f.seek(start_num)
        image = f.read(size)
    if is_image:
        image = Image.open(io.BytesIO(image))
    return image

def read_json(file_path):
    d = open(file_path).read().split('\n')
    res = []
    for line in d:
        try:
            res.append(json.loads(line))
        except:
            continue
    print('all {} lines, success {} lines'.format(len(d), len(res)))

    return res

def write_json(file_path, dat, mode='a'):
    with open(file_path, mode) as f:
        for i in dat:
            f.write(json.dumps(i, ensure_ascii=False) + '\n')


def get_resolution(resolution):
    resolutions = [('16:9', 16./9), ('4:3', 4./3), ('1:1', 1), ('3:4', 3./4), ('9:16', 9./16)]
 
    Bmatch, Bdistance = '', 19
    ratio = resolution[0] / resolution[1]
    if True:
        for match, distance in resolutions:
            if abs(ratio - distance) < Bdistance:
                Bmatch = match
                Bdistance = abs(ratio - distance)
    return Bmatch


import os
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map.pkl')

en2ch = pickle.loads(open(d, 'rb').read())
def translate_tag(tag):
    return en2ch.get(tag, tag)


