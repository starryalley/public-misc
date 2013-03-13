#!/bin/bash
#
# Under construction - Not working yet!
#
#
# Author: Mark Kuo (starryalley@gmail.com)
# Date:   2013.3.13
#

#
# Requirements:
#
# 可以把所有的hash data都放在一個文字檔案裡面
# 在檔案名稱永遠相同的前提之下
# 程式提式的訊息基本上只需要
# 1 match
# 2 modified
# 3 disappeared 
#

# GLOBAL CONFIG
# ==============

# checksum filename
CHECKSUM_NAME=".dir_checksum"

# number of parallel process (should be core count + 1)
PARALLEL_COUNT=8


# === get core count ===
function core_count()
{
    echo `grep -c ^processor /proc/cpuinfo`
}

# === create checksum ===
# $1 target dir
# $2 number of process to run
function create_checksum()
{
    local path=$1  # target dir

    echo "[Run]"
    find $path -type f -print0 | #find every file under $path
        #pv --line-mode |
        xargs -0 -n 1 -P $PARALLEL_COUNT md5sum | # parallel create md5sum
        #xargs -0 -n 1 -P $PARALLEL_COUNT sh -c 'md5sum $1' sh | # with another shell command example

        #sed -f '' >  $path/$CHECKSUM_NAME #save to checksume file only
        tee $path/$CHECKSUM_NAME #save to checksume file and output to screen
    echo "[End]"

}

# === usage ===
function usage()
{
    E_BADARGS=65
    echo "Usage: $0 [directory]"
    echo "  directory: the directory to check (default: current directory"
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

# print info before doing things
echo "Target directory: $dir"

# set parallel count
PARALLEL_COUNT=$(($(core_count) + 1)) #core+1
echo "Parallel process: $PARALLEL_COUNT"

# check if checksum already exist
checksum_path="$dir/$CHECKSUM_NAME"
if [ -e $checksum_path ]; then
    echo "Checksum exists: $checksum_path"
fi

# create_checksum
create_checksum $dir

#echo -ne '#####                     (33%)\r'; sleep 1
#echo -ne '#############             (66%)\r'; sleep 1
#echo -ne '#######################   (100%)\r'
#echo -ne '\n'


exit
