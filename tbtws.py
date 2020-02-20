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

is_active = False
rotation = 0

def print_sound(indata, frames, time, status):
    global is_active
    global rotation
    volume_norm = int(np.linalg.norm(indata)*10)
    if volume_norm >= 4 and not is_active:
        is_active = True
    elif volume_norm == 0 and is_active:
        is_active = False
        rotation += 1
        print rotation

with sd.InputStream(device=(args.input_device, None), callback=print_sound):
    while True:
        pass
