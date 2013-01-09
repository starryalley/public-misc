#!/usr/bin/env python

"""

CMUS status update program using notify-send

example status update as program's parameter list
    status playing
    file /data/music/Zeb-Jesterized/12-Zeb-Spy From Cairo.mp3
    artist Zeb
    album Jesterized
    tracknumber 12
    title Spy From Cairo
    date 2000
    duration 322
"""

import sys, os
from subprocess import call

if __name__ == '__main__':
    # basic checking
    if len(sys.argv) % 2 != 1 or len(sys.argv) < 2 \
            or sys.argv[1] != 'status':
        raise Exception('please set this program as CMUS status update program')

    # make it a dict
    s = sys.argv[1:]
    status = dict(zip(s[::2], s[1::2]))

    osd_info = "[%s] %s (%s-%s)" % \
            ( status['status'], os.path.basename(status['file']),
              status['artist'], status['title'] )

    # --hint parameter is for gnome-shell's buggy notification.. anyway
    call(['notify-send', '--hint=int:transient:1', osd_info])

