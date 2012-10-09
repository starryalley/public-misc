"""
Auto uploader

Requirement:
    apt-get install python-poster

Author:
    Mark Kuo (starryalley@gmail.com)

"""

import urllib2, urllib
import json
import cookielib
import getpass
import sys
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


class LoginFailed(Exception):
    pass


class XplovaUploader:
    auth_url = 'http://tour.xplova.com/userAccount/login.php'
    upload_url = 'http://tour.xplova.com/inc/uploadActivity.php'

    def send_file(self, filename):
        values = {'upload_activity': open(filename) }
        data, headers = multipart_encode(values)
        headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        request = urllib2.Request(XplovaUploader.upload_url, data, headers)
        request.unverifiable = True
        response = urllib2.urlopen(request)
        ret = response.read()
        """
    <script type="text/javascript" src="../js/json2.js"></script>
    <script language="javascript">
        var retParse = JSON.parse("{\"CRC32\":597374500,\"activity_id\":18304,\"ret\":\"RET_OK\",\"retDescription\":\"Success\",\"startDatetime\":\"2012-09-27 22:49:16\"}");
        window.top.window.retUploadActivityComplete(retParse);
    </script>
        """
        print "Upload result:", ret


    def authenticate(self, user, passwd):
        login_data = urllib.urlencode( [('user',user),('pwd',passwd)] )

        cj = cookielib.CookieJar()
        opener = register_openers()
        opener.add_handler(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request(XplovaUploader.auth_url, login_data)
        login_ret = urllib2.urlopen(req).read()
        login_ret = json.loads(login_ret)
        if login_ret['ret'] == 'RET_OK':
            print "Login successful! UserId: %s, UserName: %s" % \
                (login_ret["userId"], login_ret["userName"])
            return opener
        # error
        else:
            err = "Login failed [%s]. Detailed info:" % \
                (login_ret['ret'], login_ret)
            raise LoginFailed(err)
    pass


if __name__ == '__main__':

    uploader = XplovaUploader()
    try:
        user = raw_input("Xplova Username: ")
        password = getpass.getpass("Xplova Password:")
        uploader.authenticate(user, password)
        uploader.send_file('test.gpx')
    except LoginFailed as e:
        print e
        sys.exit(1)

