# Training bike to WebSocket

A websocket server who send real time informations about [this bike](https://www.amazon.fr/gp/product/B00FZM5W3I/). The bike is connected to the raspberry pi with an usb sound card.

## Installation

You need Python3 and pip3

```bash
sudo apt-get install libportaudio2 redis-server

pip3 install -r requirements.txt
```

## Usage

### List devices

```
python3 tbtws.py -l
```

### Run with a selected device

```
python3 tbtws.py -i 0
```
