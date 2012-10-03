#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: `basename $0` [command]"
    exit 65 #BAD_ARGS
fi

if [ $1 = "help" ]; then
    echo "available operations: "
    echo "  start: start ftrace (function tracer)"
    echo "  stop:  stop  ftrace"
    echo "  clear: clear trace buffer"
    echo "  fetch: fetch trace buffer to current directory"
    exit
fi

if [ $1 = "start" ]; then
    adb shell "echo function >/d/tracing/current_tracer"
    adb shell "echo 1 >/d/tracing/tracing_on"
elif [ $1 = "stop" ]; then
    adb shell "echo 0 >/d/tracing/tracing_on"
elif [ $1 = "clear" ]; then
    adb shell "echo 0 > /d/tracing/trace"
elif [ $1 = "fetch" ]; then
    adb pull /d/tracing/trace trace
else
    echo "Not recognized: $1"
fi
