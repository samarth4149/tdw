#!/bin/bash

VERSION=$(python tdw_version.py)

# Allow x server to accept local connections
xhost +local:root

# Run the container
docker run -it \
  --gpus all \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /data/samarth:/data/samarth \
  -e DISPLAY=$DISPLAY \
  --network host \
  tdw_latest:latest\
  ./TDW/TDW.x86_64 $@
  # /bin/bash -c "Xorg :2 -config /etc/X11/xorg-2.conf & nvidia-smi;TDW/TDW.x86_64 -port=$1;"
