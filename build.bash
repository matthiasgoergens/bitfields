#!/bin/bash
set -e
set -u
set -o pipefail
# set -x
# docker build --platform linux/amd64 --tag big-endian .
docker build --platform linux/s390x --tag big-endian .
# docker run --rm --platform linux/s390x big-endian
