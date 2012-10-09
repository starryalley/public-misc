"""
Auto uploader

Requirement:
    apt-get install python-poster python-requests

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
import uuid, socket
import requests

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"

class LoginFailed(Exception):
    pass


# reference: https://github.com/isoteemu/sports-tracker-liberator/blob/master/endomondo.py
# TODO: not working
class EndomondoUploader:
    upload_url = ''

    # Some parameters what Endomondo App sends.
    country = 'GB'
    device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, socket.gethostname()))
    os = "Android"
    app_version="7.1"
    app_variant="M-Pro"
    os_version="2.3.7"
    model="HTC Vision"

    # Authentication url. Special case.
    URL_AUTH = 'https://api.mobile.endomondo.com/mobile/auth?v=2.4&action=PAIR'

    def __init__(self):
        # Using session - provides keep-alive in urllib3
        self.Requests = requests.session()
        # Auth token
        self.auth_token = None
        self.Requests.headers['User-Agent'] = "Dalvik/1.4.0 (Linux; U; %s %s; %s Build/GRI40)" % (self.os, self.os_version, self.model)


    def request_auth_token(self, email, password):
        params = {
            'email':        email,
            'password':     password,
            'country':      self.country,
            'deviceId':     self.device_id,
            'os'    :       self.os,
            'appVersion':   self.app_version,
            'appVariant':   self.app_variant,
            'osVersion':    self.os_version,
            'model':        self.model
        }

        r = self.Requests.get(self.URL_AUTH, params=params)
        lines = r.content.split("\n")
        if lines[0] != "OK":
            raise ValueError("Could not authenticate with Endomondo, Expected 'OK', got '%s'" % lines[0])

        lines.pop(0)
        for line in lines:
            key, value = line.split("=")
            if key == "authToken":
                return value

        return False

    def authenticate(self, user, passwd):
        self.auth_token = self.request_auth_token(user, passwd)
        print self.auth_token

    # Helper for generating requests - can't be used in athentication.
    def make_request(self, url, params={}):
        params.update({
            'authToken': self.auth_token,
            'language':    'EN'
        })
        r = self.Requests.get(url, params=params)

        if r.status_code != requests.codes.ok:
            print "Could not retrieve URL %s" % r.url
            r.raise_for_status()
        return r

    def upload(self, f):
        r = self.make_request("http://api.mobile.endomondo.com/mobile/api/workout/list?maxResults=5")
        print r.content
        pass

    pass


class XplovaUploader:
    auth_url = 'http://tour.xplova.com/userAccount/login.php'
    upload_url = 'http://tour.xplova.com/inc/uploadActivity.php'

    def upload(self, f):
        values = {'upload_activity': f}
        data, headers = multipart_encode(values)
        headers['User-Agent'] = USER_AGENT
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
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--xplova', action = 'store_true', \
            help = 'upload to xplova')
    group.add_argument('--endomondo', action = 'store_true', \
            help = 'upload to endomondo (not working!)')
    parser.add_argument('-i', '--import-file', required = True,\
            type = argparse.FileType('r'), \
            help = 'file to upload')
    parser.add_argument('-u', '--user', help = 'Login username')
    parser.add_argument('-p', '--passwd', help = 'Login password')
    parser.add_argument('-v', '--version', action='version', \
            version='%(prog)s 1.0')
    args = parser.parse_args()

    # do it
    if args.endomondo:
        uploader = EndomondoUploader()
    elif args.xplova:
        uploader = XplovaUploader()
    else:
        print "Unknown uploader type!"
        sys.exit(1)

    if args.user is None:
        args.user = raw_input("Username: ")
    if args.passwd is None:
        args.passwd = getpass.getpass("Password: ")
    try:
        uploader.authenticate(args.user, args.passwd)
        uploader.upload(args.import_file)
    except LoginFailed as e:
        print e
        sys.exit(1)
    except IOError as e:
        print e
        sys.exit(1)

