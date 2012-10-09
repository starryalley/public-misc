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
import argparse
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


class LoginFailed(Exception):
    pass


class XplovaUploader:
    auth_url = 'http://tour.xplova.com/userAccount/login.php'
    upload_url = 'http://tour.xplova.com/inc/uploadActivity.php'

    def send_file(self, f):
        values = {'upload_activity': f}
        data, headers = multipart_encode(values)
        headers['User-Agent'] = \
                'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        request = urllib2.Request(XplovaUploader.upload_url, data, headers)
        request.unverifiable = True
        print "Uploading..."
        response = urllib2.urlopen(request)
        ret = response.read()

        """
        example successful upload:
    <script type="text/javascript" src="../js/json2.js"></script>
    <script language="javascript">
        var retParse = JSON.parse("{\"CRC32\":597374500,\"activity_id\":18304,\"ret\":\"RET_OK\",\"retDescription\":\"Success\",\"startDatetime\":\"2012-09-27 22:49:16\"}");
        window.top.window.retUploadActivityComplete(retParse);
    </script>
        """
        # TODO: not yet handled
        if "RET_OK" in ret:
            print "Upload successful!"
        print "Full response:", ret


    def authenticate(self, user, passwd):
        login_data = urllib.urlencode( [('user', user),('pwd', passwd)] )

        opener = register_openers()
        opener.add_handler(urllib2.HTTPCookieProcessor( \
                cookielib.CookieJar()))
        req = urllib2.Request(XplovaUploader.auth_url, login_data)
        login_ret = json.loads(urllib2.urlopen(req).read())

        if login_ret['ret'] == 'RET_OK':
            print "Login successful! UserId: %s, UserName: %s" % \
                (login_ret["userId"], login_ret["userName"])
            return opener
        else:
            err = "Login failed [%s]. Detailed info: %s" % \
                (login_ret['ret'], login_ret)
            raise LoginFailed(err)
    pass


if __name__ == '__main__':
    # build argument parser
    parser = argparse.ArgumentParser(\
            description = 'Auto uploader script for sport activity sites')
    parser.add_argument('--xplova', action = 'store_true', \
            help = 'upload to xplova (default)', default = True)
    parser.add_argument('-i', '--import-file', required = True,\
            type = argparse.FileType('r'), \
            help = 'file to upload')
    parser.add_argument('-u', '--user', help = 'Login username')
    parser.add_argument('-p', '--passwd', help = 'Login password')
    parser.add_argument('-v', '--version', action='version', \
            version='%(prog)s 1.0')
    args = parser.parse_args()

    # do it
    if args.xplova:
        uploader = XplovaUploader()
        if args.user is None:
            args.user = raw_input("Username: ")
        if args.passwd is None:
            args.passwd = getpass.getpass("Password: ")
        try:
            uploader.authenticate(args.user, args.passwd)
            uploader.send_file(args.import_file)
        except LoginFailed as e:
            print e
            sys.exit(1)
        except IOError as e:
            print e
            sys.exit(1)

