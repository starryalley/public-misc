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
REGIST_URL='https://registrano.com/events/coscup2012-regist/registrations/new'
EMAIL='starryalley@gmail.com'

if __name__ == '__main__':
    try:
        soup = BeautifulSoup(urllib2.urlopen(URL))
        res = soup.findAll('li', {'class': 'status'})
        m = re.search('尚餘(\d+)名額', str(res[0]))
        left = int(m.group(1))

        # send messages
        message = "Coscup 2012 Registration: %d seat(s) left!" % left
        mail_content= "%s\nGo to %s immediately!\n" % (message, REGIST_URL)
        print message
        if left > 0:
            call('notify-send "%s"' % message, shell = True)
            call('echo "%s" | mutt -s "COSCUP 2012 Registration available" %s' % \
                    (mail_content, EMAIL), shell = True)
    except:
        call('notify-send "Error checking available seats!"', shell = True)

