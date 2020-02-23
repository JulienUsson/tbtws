# Training bike to WebSocket

A websocket server who send real time informations about [this bike](https://www.amazon.fr/gp/product/B00FZM5W3I/). The bike is connected to the raspberry pi with an usb sound card.

## Installation

You need Python3, pip3 and NodeJS

```bash
sudo apt-get install libportaudio2 redis-server
pip3 install -r requirements.txt
npm install
```

## Usage

### List devices

```
python3 training_bike_listener.py -l
```

### Run listener

```
python3 training_bike_listener.py -i 0
```

### Run websocket sender

```
node training_bike_sender.js
```
