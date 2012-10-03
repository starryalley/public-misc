#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: `basename $0` [filename to process]"
    exit 65 #BAD_ARGS
fi

DIR="$( dirname "${BASH_SOURCE[0]}" )"
echo $DIR

if [ ! -f ${DIR}/split.py ] || [ ! -f ${DIR}/draw_functrace.py ]; then
    echo "split.py or draw_functrace.py is absent. Exit.."
    exit 1
fi

echo "Spliting by CPU..."
python ${DIR}/split.py tmp < $1

echo "Creating function trace trees for all CPUs..."
python ${DIR}/draw_functrace.py < $1 > $1-tree

echo "Creating function trace trees for separate CPU..."
python ${DIR}/draw_functrace.py < tmp-cpu0.log > $1-cpu0-tree
python ${DIR}/draw_functrace.py < tmp-cpu1.log > $1-cpu1-tree
python ${DIR}/draw_functrace.py < tmp-cpu2.log > $1-cpu2-tree
python ${DIR}/draw_functrace.py < tmp-cpu3.log > $1-cpu3-tree

echo "Done!"
rm -f tmp-cpu?.log
