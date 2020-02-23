import time
import argparse
import sounddevice as sd
import numpy as np
import redis
import json


# __________Constants__________
BIKE_WHEEL_DIAMETER = 0.622


# __________Global vars__________
redis_client = redis.Redis(host='localhost', port=6379,
                           db=0, decode_responses=True)
redis_pubsub = redis_client.pubsub()


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
        self.rotation = 0
        self.last_rotation_date = None
        self.speed = None
        self.distance = 0

    def sound_handler(self, indata, _frames, _time, _status):
        volume_norm = int(np.linalg.norm(indata)*10)
        if volume_norm >= 4 and not self.is_active:
            self.is_active = True
        elif volume_norm == 0 and self.is_active:
            self.is_active = False
            self.rotation += 1
            self.distance += BIKE_WHEEL_DIAMETER
            self.current_date = time.time()
            if self.last_rotation_date is not None:
                self.speed = BIKE_WHEEL_DIAMETER / \
                    (self.current_date - self.last_rotation_date)
            self.last_rotation_date = self.current_date
            message = json.dumps({"rotation": self.rotation,
                                  "distance": self.distance, "speed": self.speed})
            redis_client.publish('bike_stat', message)
            print("Listener: sending " + message)

    def run(self):
        redis_pubsub.subscribe('bike_reset')
        with sd.InputStream(device=(args.input_device, None), callback=self.sound_handler):
            while True:
                message = redis_pubsub.get_message()
                if message is not None and isinstance(message['data'], str) and message['data'].lower() == 'true':
                    self.reset()
                time.sleep(0.1)

    def reset(self):
        self.rotation = 0
        self.distance = 0
        print("Listener: Resetted")


if __name__ == '__main__':
    bike_recorder = bikeRecorder()
    print("Listener: Started")
    bike_recorder.run()
