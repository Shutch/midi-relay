docker run -it \
  --name midi-relay \
  --mount type=bind,source="$(pwd)"/src,destination=/src \
  --device /dev/snd \
  --device /dev/bus/usb \
  -p 9999:9999 \
  midi-relay \
  /bin/bash
