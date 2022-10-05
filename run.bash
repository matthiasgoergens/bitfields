#!/bin/bash
set -e
set -u
set -o pipefail
# set -x

file=$1
echo File: $file

CC=clang

echo
echo -mms-bitfields
rm -f a.out
${CC} -mms-bitfields -fsanitize=undefined -Wall -Os ${file}
./a.out

echo
echo -mno-ms-bitfields
rm -f a.out
${CC} -mno-ms-bitfields -fsanitize=undefined -Wall -Os ${file}
./a.out

echo
echo no option
rm -f a.out
${CC} -fsanitize=undefined -Wall -Os ${file}
./a.out
