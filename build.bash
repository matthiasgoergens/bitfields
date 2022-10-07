#!/bin/bash
docker build --tag big-endian .
docker build --platform linux/amd64 --tag big-endian .
docker run --platform linux/s390x big-endian
