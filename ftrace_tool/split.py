#!/usr/bin/python
import sys, re

class CommentLineException(Exception):
    pass

class BrokenLineException(Exception):
    pass

def parseLine(line):
    line = line.strip()
    if line.startswith("#"):
        raise CommentLineException
    #<idle>-0     [002]  1094.874132: ttwu_do_activate.clone.2 <-sched_ttwu_do_pending
    m = re.match("[^[]+ +\\[(\d+)\\] +([0-9.]+): ([\\w\\.]+) <-([\\w\\.]*)", line)
    if m is None:
        raise BrokenLineException
    return int(m.group(1))


def main():
    name = "default"
    cpu_count = 4 # hard-coded
    try:
        name = sys.argv[1]
    except:
        print "Usage: %s [filename prefix]"
        sys.exit(1)
    fds = []
    for i in range(cpu_count):
        fds.append(open("%s-cpu%d.log" % (name, i), "w"))

    for line in sys.stdin:
        try:
            cpu = parseLine(line)
            fds[cpu].write(line)
        except (BrokenLineException, CommentLineException):
            continue
        except Exception:
            #skip errors
            pass

    for fd in fds:
        fd.close()

if __name__ == "__main__":
    main()
