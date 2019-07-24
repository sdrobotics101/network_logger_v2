import time
import os
from datetime import datetime
import sys
import logging
from logging.handlers import RotatingFileHandler
from ctypes import sizeof
sys.path.append("./dependencies/python-shared-buffers/shared_buffers/")

import pydsm

from master import ControlInput, SensorReset
from sensor import Angular, Linear, Data
from navigation import Kill, Outputs, Health, PhysicalOutput
from vision import DetectionArray
from serialization import pack, unpack

from settings import (
    MAS_IP,
    MAS_SID,
    SEN_IP,
    SEN_SID,
    NAV_IP,
    NAV_SID,
    VIS_IP,
    VIS_SID
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
    var_names.append("active")
    return " ".join(var_names)

def create_string(key):
    active, obj = get_buffer(key)
    values = map(lambda x: "obj."+x[1], contents(key))
    values = map(eval, values)
    values = map(float, values)
    values = map(lambda x: round(x,4), values)
    values = map(str, values)
    values = list(values)
    values.append(str(int(active)))
    return " ".join(values)

keys = [
    ("control", MAS_IP, MAS_SID, ControlInput,
        (
            ("m_lvx", "linear[0].vel"),
            ("m_lvy", "linear[1].vel"),
            ("m_lpz", "linear[2].pos[0]"),
            ("m_apx", "angular[0].pos[0]"),
            ("m_apy", "angular[1].pos[0]"),
            ("m_apz", "angular[2].pos[0]"),
        )
    ),
    ("linear", SEN_IP, SEN_SID, Linear,
        (
            ("s_lpz", "pos[2]"),
        )
    ),
    ("angular", SEN_IP, SEN_SID, Angular,
        (
            ("s_apx", "acc[0]"),
            ("s_apy", "acc[1]"),
            ("s_apz", "acc[2]")
        )
    ),
    ("kill", NAV_IP, NAV_SID, Kill,
        (
            ("killed", "isKilled"),
        )
    ),
    ("forwarddetection", VIS_IP, VIS_SID, DetectionArray,
        (
            ("d0x", "detections[0].x"),
            ("d0y", "detections[0].y"),
            ("d0w", "detections[0].w"),
            ("d0h", "detections[0].h"),
            ("d0s", "detections[0].size"),
            ("d0c", "detections[0].cls"),
            ("d1x", "detections[1].x"),
            ("d1y", "detections[1].y"),
            ("d1w", "detections[1].w"),
            ("d1h", "detections[1].h"),
            ("d1s", "detections[1].size"),
            ("d1c", "detections[1].cls"),
            ("d2x", "detections[2].x"),
            ("d2y", "detections[2].y"),
            ("d2w", "detections[2].w"),
            ("d2h", "detections[2].h"),
            ("d2s", "detections[2].size"),
            ("d2c", "detections[2].cls"),
            ("d3x", "detections[3].x"),
            ("d3y", "detections[3].y"),
            ("d3w", "detections[3].w"),
            ("d3h", "detections[3].h"),
            ("d3s", "detections[3].size"),
            ("d3c", "detections[3].cls"),
            ("d4x", "detections[4].x"),
            ("d4y", "detections[4].y"),
            ("d4w", "detections[4].w"),
            ("d4h", "detections[4].h"),
            ("d4s", "detections[4].size"),
            ("d4c", "detections[4].cls"),
            ("d5x", "detections[5].x"),
            ("d5y", "detections[5].y"),
            ("d5w", "detections[5].w"),
            ("d5h", "detections[5].h"),
            ("d5s", "detections[5].size"),
            ("d5c", "detections[5].cls"),
            ("d6x", "detections[6].x"),
            ("d6y", "detections[6].y"),
            ("d6w", "detections[6].w"),
            ("d6h", "detections[6].h"),
            ("d6s", "detections[6].size"),
            ("d6c", "detections[6].cls"),
            ("d7x", "detections[7].x"),
            ("d7y", "detections[7].y"),
            ("d7w", "detections[7].w"),
            ("d7h", "detections[7].h"),
            ("d7s", "detections[7].size"),
            ("d7c", "detections[7].cls"),
        )
    ),
]

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
    title.insert(0, "# date time")
    title = " ".join(title)
    logger.info(title)

    print("starting")
    while True:
        try:
            data = list(map(create_string, keys))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            data.insert(0, timestamp)
            data = " ".join(data)
            logger.info(data)
            time.sleep(0.01)
        except KeyboardInterrupt:
            print("Caught control-C, exiting")
            break

if __name__ == "__main__":
    main(sys.argv)
