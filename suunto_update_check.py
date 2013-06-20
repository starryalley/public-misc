#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  A simple one to check for Suunto Ambit2 software releases
#
#  set up mutt first, and put this one in a cron job and you're ready to go
#
#  Install before use:
#  $> sudo apt-get install libnotify-bin
#

import urllib2, re, sys, pickle
from subprocess import call
from time import strftime

URL='http://d1c229iib3zm7m.cloudfront.net/release_notes/SuuntoAmbit2_ReleaseNotes.txt'
EMAIL='starryalley@gmail.com'
VERSION_FILE='/tmp/ambit2.ver'

def dump_ver(version):
    try:
        with open(VERSION_FILE, 'w') as f:
            pickle.dump(version, f)
    except Exception, e:
        print "Error writing version file: %s" % e

def get_ver():
    try:
        with open(VERSION_FILE, 'r') as f:
            return pickle.load(f)
    except:
        return None

if __name__ == '__main__':
    version = ""
    try:
        page = urllib2.urlopen(URL).read()
        m = re.search('Suunto\sAmbit2\s(\d\.\d+\.\d+)', page)
        if m is not None: version = m.group(1)
        last_version = get_ver()
        dump_ver(version)

        if last_version is None:
            print "No last version found."
            sys.exit(1)
        message = "%s: last version: %s, new version: %s" % \
                (strftime("%Y-%m-%d %H:%M:%S"), last_version, version)
        print message

        # found new version
        if version != last_version:
            print "Found new version!"
            call('notify-send "%s"' % message, shell = True)
            call('echo "%s" | mutt -s "New Suunto Ambit2 software: %s" %s' % \
                    (message, version, EMAIL), shell = True)
    except Exception, e:
        print "%s: %s" % (strftime("%Y-%m-%d %H:%M:%S"), e)

