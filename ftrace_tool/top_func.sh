#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: `basename $0` [filename to process]"
    exit 65 #BAD_ARGS
fi

cat $1 | cut -d] -f2 | cut -d: -f2 | cut -d\< -f1 | sort | uniq -c | sort -rn
