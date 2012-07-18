#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
#  Install before use:
#  $> sudo apt-get install libnotify-bin python-beautifulsoup
#

import urllib2
import re
from subprocess import call
from BeautifulSoup import BeautifulSoup

URL='http://registrano.com/events/coscup2012-regist'

if __name__ == '__main__':
    try:
        soup = BeautifulSoup(urllib2.urlopen(URL))
        res = soup.findAll('li', {'class': 'status'})
        m = re.search('尚餘(\d+)名額', str(res[0]))
        left = int(m.group(1))
        if left > 0:
            message = "Coscup 2012 Registration: %d seats left!" % left
            call('notify-send "%s"' % message, shell = True)
    except:
        pass

