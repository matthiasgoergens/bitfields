# syntax=docker/dockerfile:1
FROM --platform=linux/s390x s390x/ubuntu as build
RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install --yes gcc clang
WORKDIR /bitfields
# ADD test.c ./
# RUN clang -o test test.c
# CMD ./test
CMD bash -c "lscpu | grep 'Byte Order:'"
