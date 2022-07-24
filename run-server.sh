#!/bin/bash

docker rm midi-relay-client

docker run -it \
  --name midi-relay-server \
  --device /dev/snd \
  --device /dev/bus/usb \
  -p 9999:9999 \
  midi-relay \
  python /src/server.py
