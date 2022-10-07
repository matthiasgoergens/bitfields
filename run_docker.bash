#!/bin/bash
set -e
set -u
set -o pipefail
# set -x

# --detach \
#   --interactive --tty \

docker run --platform linux/s390x \
  --rm \
  --name big_endian_test \
  --mount type=bind,source="$(pwd)",target=/bitfields \
  big-endian \
  lscpu

# file=$1
# echo File: $file

# CC=clang

# echo
# echo -mms-bitfields
# rm -f a.out
# ${CC} -mms-bitfields -fsanitize=undefined -Wall -Os ${file}
# ./a.out

# echo
# echo -mno-ms-bitfields
# rm -f a.out
# ${CC} -mno-ms-bitfields -fsanitize=undefined -Wall -Os ${file}
# ./a.out

# echo
# echo no option
# rm -f a.out
# ${CC} -fsanitize=undefined -Wall -Os ${file}
# ./a.out
