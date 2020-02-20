import os
import time
import argparse
import sounddevice as sd
import numpy as np


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-i', '--input-device', type=int,
    help='input device (numeric ID or substring)')
args = parser.parse_args(remaining)

BIKE_WHEEL_DIAMETER = 0.622

is_active = False
rotation = 0
last_rotation_date = None
speed = None
distance = 0


def print_info():
    def clear(): return os.system('clear')
    clear()
    print(str(rotation) + " rotations")
    print(str(distance) + " m")
    print(str(speed) + " m/s")


def sound_callback(indata, _frames, _time, _status):
    global is_active
    global rotation
    global last_rotation_date
    global distance
    global speed

    volume_norm = int(np.linalg.norm(indata)*10)
    if volume_norm >= 4 and not is_active:
        is_active = True
    elif volume_norm == 0 and is_active:
        is_active = False
        rotation += 1
        distance += BIKE_WHEEL_DIAMETER
        current_date = time.time()
        if last_rotation_date is not None:
            speed = BIKE_WHEEL_DIAMETER / (current_date - last_rotation_date)
        last_rotation_date = current_date
        print_info()


with sd.InputStream(device=(args.input_device, None), callback=sound_callback):
    while True:
        pass
