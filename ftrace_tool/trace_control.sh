#!/bin/bash

if [ $# -ne 1 ] && [ $# -ne 2 ]; then
    echo "Usage: `basename $0` [command]"
    exit 65 #BAD_ARGS
fi

if [ $1 = "help" ]; then
    echo "available operations: "
    echo "  start [tracer name]: start ftrace with tracer name"
    echo "  start: start ftrace with nop tracer"
    echo "  start function: start ftrace with function tracer"
    echo "  stop:  stop  ftrace"
    echo "  clear: clear trace buffer"
    echo "  fetch: fetch trace buffer to current directory"
    exit
fi

if [ $1 = "start" ]; then
    if [ $# -eq 2 ]; then
        adb shell "echo $2 >/d/tracing/current_tracer"
    else
        adb shell "echo nop >/d/tracing/current_tracer"
    fi
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
