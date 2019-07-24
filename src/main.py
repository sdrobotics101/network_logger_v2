import time
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

import pydsm

sys.path.append("./dependencies/python-shared-buffers/shared_buffers/")
from serialization import pack, unpack

from settings import (
    MAS_IP,
    MAS_SID,
    SEN_IP,
    SEN_SID,
    NAV_IP,
    NAV_SID,
    VIS_IP,
    VIS_SID,
    keys
)

def name(key):
    return key[0]

def ip(key):
    return key[1]

def sid(key):
    return key[2]

def obj(key):
    return key[3]

def contents(key):
    return key[4]

def register_buffer(key):
    client.registerRemoteBuffer(name(key), ip(key), sid(key))

def get_buffer(key):
    data, active = client.getRemoteBufferContents(name(key), ip(key), sid(key))
    return active, unpack(obj(key), data)

def create_title(key):
    var_names = list(map(lambda x: x[0], contents(key)))
    var_names.append(name(key)+"_active")
    return ",".join(var_names)

def create_string(key):
    active, obj = get_buffer(key)
    values = map(lambda x: "obj."+x[1], contents(key))
    values = map(eval, values)
    values = map(float, values)
    values = map(lambda x: round(x,4), values)
    values = map(str, values)
    values = list(values)
    values.append(str(int(active)))
    return ",".join(values)

client = pydsm.Client(254, 193, True)
def main(args):
    if len(args) > 1:
        log_dirname = args[1]
    else:
        log_dirname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = os.path.join(os.path.expanduser("~/robosub_logs"), log_dirname)
    os.makedirs(log_dir)
    log_filename = os.path.join(log_dir, "robosub.log")
    print("logging to file: ", log_filename)

    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_filename, maxBytes=100000000, backupCount=40)
    logger.addHandler(handler)

    list(map(register_buffer, keys))
    time.sleep(0.5)

    title = list(map(create_title, keys))
    title.insert(0, "date,time")
    title = ",".join(title)
    logger.info(title)

    print("starting")
    while True:
        try:
            data = list(map(create_string, keys))
            timestamp = datetime.now().strftime("%Y-%m-%d,%H:%M:%S.%f")
            data.insert(0, timestamp)
            data = ",".join(data)
            logger.info(data)
            time.sleep(0.01)
        except KeyboardInterrupt:
            print("Caught control-C, exiting")
            break

if __name__ == "__main__":
    main(sys.argv)
