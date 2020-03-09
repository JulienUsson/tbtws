import time
import argparse
import sounddevice as sd
import numpy as np
import json


# __________Constants__________
BIKE_WHEEL_DIAMETER = 0.622


# __________Arguments parser__________
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


class bikeRecorder:
    def __init__(self):
        self.is_active = False
        self.last_rotation_date = None

    def sound_handler(self, indata, _frames, _time, _status):
        volume_norm = int(np.linalg.norm(indata)*10)

        if volume_norm >= 4 and not self.is_active:
            self.is_active = True

        elif volume_norm == 0 and self.is_active:
            self.is_active = False
            current_date = time.time()

            if self.last_rotation_date is not None:
                delta = current_date - self.last_rotation_date
                speed = BIKE_WHEEL_DIAMETER / delta

            self.last_rotation_date = current_date
            message = json.dumps({"speed": speed})
            print(message)

    def run(self):
        with sd.InputStream(device=(args.input_device, None), callback=self.sound_handler):
            while True:
                pass


if __name__ == '__main__':
    bike_recorder = bikeRecorder()
    bike_recorder.run()
