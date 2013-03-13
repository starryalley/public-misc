#!/bin/bash
#
# Directory checksum script
#
# It computes md5sum of all files in one directory
# recursively and saved to a checksum file under it.
# Second execution on that directory will compare
# last checksum with current one and report missed/
# added/modified files.
#
# =======================================
#
# Author: Mark Kuo (starryalley@gmail.com)
# Date:   2013.3.13
#

#
# Original Requirements:
#
# 可以把所有的hash data都放在一個文字檔案裡面
# 在檔案名稱永遠相同的前提之下
# 程式提式的訊息基本上只需要
# 1 match
# 2 modified
# 3 disappeared
#

#
# Dependent commands:
# md5sum, diff, comm, xargs, find, sort
# grep, egrep, echo, sed, rm, mv, wc, pv
#
# Notes:
#  only tested under Ubuntu 12.04
#


# GLOBAL CONFIG
# ==============

# checksum filename (old checksum will have same filename with .old suffix)
CHECKSUM_NAME=".dir_checksum"

# number of parallel process (will be updated to core count + 1 when script runs)
PARALLEL_COUNT=2


# === get core count ===
function core_count()
{
    echo `grep -c ^processor /proc/cpuinfo`
}


# === create checksum ===
# $1 target dir
# $2 target checksum filename
function create_checksum()
{
    local path=$1
    local checksum=$2

    echo "Count files..."
    local count=`find -L $path ! -name $CHECKSUM_NAME ! -name $CHECKSUM_NAME.old \
         -type f | wc -l`
    echo "$count files found"

    echo "Computing checksum..."
    # the long pipeline of 'find | xargs md5sum | pv | sort'
    find -L $path ! -name $CHECKSUM_NAME ! -name $CHECKSUM_NAME.old \
         -type f -print0 |       #find every file under $path (follow symbolic links)
        xargs -0 -n 1 -P $PARALLEL_COUNT md5sum |   # parallel create md5sum
        #xargs -0 -n 1 -P $PARALLEL_COUNT sh -c 'md5sum $1' sh | # with another shell command example

        pv -cN MD5SUM --line-mode -s $count |       #showing nice progress bar using pv

        sort --parallel=$PARALLEL_COUNT -k 2 |      #should sort or diff will fail badly
        #pv -cN SORT --line-mode -s $count |        #showing nice progress bar using pv
        sed '' > $checksum                          #save to checksume file only
        #tee $checksum                              #save to checksume file and output to screen

    echo "Done. Checksum file written to $checksum"
}


# === compare checksum ===
# $1 target dir
# $2 old checksum file
# $3 new checksum file
function compare_checksum()
{
    # diff filename
    local DIFF_NAME="${CHECKSUM_NAME}.diff"

    local path=$1
    local old=$2
    local new=$3

    #echo "comparing $old and $new..."
    diff --suppress-common-lines --unified=0 $old $new |    #diff
        egrep -v "\-\-\-|\+\+\+|\@\@" |                     #remove other info
        sed '' > $path/$DIFF_NAME

    # example output here:
    #   -0dea76f1d4581b591409bffe8fe6f722  ../tmp/test_enum/main.c
    #   +330a71bf82c38415860d19490cec2648  ../tmp/test_enum/main.c
    #   -d41d8cd98f00b204e9800998ecf8427e  ../tmp/test_enum/test1
    #   +d41d8cd98f00b204e9800998ecf8427e  ../tmp/test_enum/test3

    # grep - and + respectively into 2 sets (miss and new)
    grep ^- $path/$DIFF_NAME | cut -d' ' -f3 | sort > $path/$DIFF_NAME.miss
    grep ^+ $path/$DIFF_NAME | cut -d' ' -f3 | sort > $path/$DIFF_NAME.new

    echo "=== Report ==="
    echo "Modified:"    # the intersection
    comm -12 $path/$DIFF_NAME.miss $path/$DIFF_NAME.new | sed '/^$/d'
    echo "--------------"
    echo "Missed:"      #in miss but not in new
    comm -2 $path/$DIFF_NAME.miss $path/$DIFF_NAME.new | cut -f 1 | sed '/^$/d'
    echo "--------------"
    echo "Added:"       #in new but not in miss
    comm -2 $path/$DIFF_NAME.new $path/$DIFF_NAME.miss | cut -f 1 | sed '/^$/d'
    echo "--------------"

    # clean up tmp files
    rm $path/$DIFF_NAME*
}


# === usage ===
function usage()
{
    local E_BADARGS=65
    echo "Usage: $0 [directory]"
    echo "  directory: the directory to check (default: current directory)"
    exit $E_BADARGS
}


# === main ===

# check arguments
if [ $# -gt 1 ]; then
    echo "Wrong arguments"
    usage
fi

# default: current working directory
dir=${1:-`pwd`}
if [ ! -e $dir ]; then
    echo "$1 doesn't exist or is not a directory. Exiting.."
    exit 1
fi

echo "Target directory: $dir"

# set parallel count
PARALLEL_COUNT=$(($(core_count) + 1)) #core+1
echo "Parallel process: $PARALLEL_COUNT"

# check if checksum already exist
checksum_path="$dir/$CHECKSUM_NAME"
if [ -e $checksum_path ]; then
    echo "Old checksum exists. Renamed: $checksum_path.old"
    mv $checksum_path $checksum_path.old
fi

# create_checksum
create_checksum $dir $checksum_path

# see if we need to compare
if [ -e $checksum_path.old ]; then
    compare_checksum $dir $checksum_path.old $checksum_path
    # keep old copy for reference?
    #rm $checksum_path.old
fi

# progress example: (may work only in linux)
#echo -ne '#####                     (33%)\r'; sleep 1
#echo -ne '#############             (66%)\r'; sleep 1
#echo -ne '#######################   (100%)\r'
#echo -ne '\n'

exit

