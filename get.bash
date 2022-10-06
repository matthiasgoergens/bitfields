#!/bin/bash
# docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker run --rm -it --platform linux/s390x s390x/ubuntu bash

# root@30dbe9c6b99a:/# lscpu | grep Endian
# Byte Order:                      Big Endian
