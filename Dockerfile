# syntax=docker/dockerfile:1
FROM --platform=linux/s390x s390x/ubuntu as build
RUN echo deb-src http://archive.ubuntu.com/ubuntu/ jammy main >> /etc/apt/sources.list
# RUN echo deb-src http://archive.ubuntu.com/ubuntu/ jammy main restricted universe multiverse >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install --yes gcc clang
# RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install --yes tzdata
ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Singapore
RUN apt-get build-dep --yes python3

RUN apt-get install --yes build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev

RUN apt-get install --yes python3-pip
RUN apt-get install --yes pkg-config

WORKDIR /bitfields

RUN python3 -m pip install hypothesis

# ADD test.c ./
# RUN clang -o test test.c
# CMD ./test
# CMD bash -c "lscpu | grep 'Byte Order:'"
