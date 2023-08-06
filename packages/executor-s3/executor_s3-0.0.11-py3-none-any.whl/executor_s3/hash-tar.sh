#!/bin/bash

tar -xf $1 --to-command='sh -c "echo $(md5sum | head -c 32) $TAR_FILENAME"'\
  | sort -u | md5sum | head -c 32
