# Training bike to WebSocket

A websocket server who send real time informations about [this bike](https://www.amazon.fr/gp/product/B00FZM5W3I/). The bike is connected to the raspberry pi with an usb sound card.

## Installation

You need Python2 and pip

```bash
sudo apt-get install libportaudio2

pip install sounddevice
pip install numpy
```

## Usage

### List devices

```
python tbtws.py -l
```

### Run with a selected device

```
python tbtws.py -i 0
```
