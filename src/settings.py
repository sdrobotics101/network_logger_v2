import sys
sys.path.append("./dependencies/python-shared-buffers/shared_buffers/")

from master import ControlInput, SensorReset, DropperInput
from sensor import Angular, Linear, Data
from navigation import Kill, Outputs, Health, PhysicalOutput, RawOutputs
from vision import DetectionArray

MAS_IP = "10.0.0.42"
SEN_IP = "10.0.0.43"
NAV_IP = "10.0.0.44"
VIS_IP = "10.0.0.45"

# MAS_IP = "127.0.0.1"
# SEN_IP = "127.0.0.1"
# NAV_IP = "127.0.0.1"
# VIS_IP = "127.0.0.1"

MAS_SID = 42
SEN_SID = 43
NAV_SID = 44
VIS_SID = 45

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
    ("droppers", MAS_IP, MAS_SID, DropperInput,
        (
            ("dropper0", "droppers[0]"),
            ("dropper1", "droppers[1]"),
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
    ("outputs", NAV_IP, NAV_SID, Outputs,
        (
            ("motor0", "motors[0]"),
            ("motor1", "motors[1]"),
            ("motor2", "motors[2]"),
            ("motor3", "motors[3]"),
            ("motor4", "motors[4]"),
            ("motor5", "motors[5]"),
            ("motor6", "motors[6]"),
            ("motor7", "motors[7]"),
        )
    ),
    ("raw_outputs", NAV_IP, NAV_SID, RawOutputs,
        (
            ("raw_motor0", "motors[0]"),
            ("raw_motor1", "motors[1]"),
            ("raw_motor2", "motors[2]"),
            ("raw_motor3", "motors[3]"),
            ("raw_motor4", "motors[4]"),
            ("raw_motor5", "motors[5]"),
            ("raw_motor6", "motors[6]"),
            ("raw_motor7", "motors[7]"),
        )
    ),
    ("nav_linear", NAV_IP, NAV_SID, PhysicalOutput,
        (
            ("nl_fx", "force[0]"),
            ("nl_fy", "force[1]"),
            ("nl_fz", "force[2]"),
            ("nl_tx", "torque[0]"),
            ("nl_ty", "torque[1]"),
            ("nl_tz", "torque[2]"),
        )
    ),
    ("nav_angular", NAV_IP, NAV_SID, PhysicalOutput,
        (
            ("na_fx", "force[0]"),
            ("na_fy", "force[1]"),
            ("na_fz", "force[2]"),
            ("na_tx", "torque[0]"),
            ("na_ty", "torque[1]"),
            ("na_tz", "torque[2]"),
        )
    ),
    ("forwarddetection", VIS_IP, VIS_SID, DetectionArray,
        (
            ("d0x", "detections[0].x"),
            ("d0y", "detections[0].y"),
            ("d0w", "detections[0].w"),
            ("d0h", "detections[0].h"),
            ("d0s", "detections[0].cxt"),
            ("d0s", "detections[0].cnf"),
            ("d0c", "detections[0].cls"),
            ("d0c", "detections[0].id"),
            ("d0c", "detections[0].id"),
            ("d1x", "detections[1].x"),
            ("d1y", "detections[1].y"),
            ("d1w", "detections[1].w"),
            ("d1h", "detections[1].h"),
            ("d1s", "detections[1].cxt"),
            ("d0s", "detections[1].cnf"),
            ("d1c", "detections[1].cls"),
            ("d0c", "detections[1].id"),
            ("d2x", "detections[2].x"),
            ("d2y", "detections[2].y"),
            ("d2w", "detections[2].w"),
            ("d2h", "detections[2].h"),
            ("d2s", "detections[2].cxt"),
            ("d0s", "detections[2].cnf"),
            ("d2c", "detections[2].cls"),
            ("d0c", "detections[2].id"),
            ("d3x", "detections[3].x"),
            ("d3y", "detections[3].y"),
            ("d3w", "detections[3].w"),
            ("d3h", "detections[3].h"),
            ("d3s", "detections[3].cxt"),
            ("d0s", "detections[3].cnf"),
            ("d3c", "detections[3].cls"),
            ("d0c", "detections[3].id"),
            ("d4x", "detections[4].x"),
            ("d4y", "detections[4].y"),
            ("d4w", "detections[4].w"),
            ("d4h", "detections[4].h"),
            ("d4s", "detections[4].cxt"),
            ("d0s", "detections[4].cnf"),
            ("d4c", "detections[4].cls"),
            ("d0c", "detections[4].id"),
            ("d5x", "detections[5].x"),
            ("d5y", "detections[5].y"),
            ("d5w", "detections[5].w"),
            ("d5h", "detections[5].h"),
            ("d5s", "detections[5].cxt"),
            ("d0s", "detections[5].cnf"),
            ("d5c", "detections[5].cls"),
            ("d0c", "detections[5].id"),
            ("d6x", "detections[6].x"),
            ("d6y", "detections[6].y"),
            ("d6w", "detections[6].w"),
            ("d6h", "detections[6].h"),
            ("d6s", "detections[6].cxt"),
            ("d0s", "detections[6].cnf"),
            ("d6c", "detections[6].cls"),
            ("d0c", "detections[6].id"),
            ("d7x", "detections[7].x"),
            ("d7y", "detections[7].y"),
            ("d7w", "detections[7].w"),
            ("d7h", "detections[7].h"),
            ("d7s", "detections[7].cxt"),
            ("d0s", "detections[7].cnf"),
            ("d7c", "detections[7].cls"),
            ("d0c", "detections[7].id"),
        )
    ),
]
