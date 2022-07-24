#!/bin/bash

docker rm midi-relay-client

docker run -it \
  --name midi-relay-client \
  --device /dev/snd \
  --device /dev/bus/usb \
  -p 9999:9999 \
  midi-relay \
  python /src/client.py
