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
import re
import argparse
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"


class LoginException(Exception): pass
class UploadException(Exception): pass
class ExportException(Exception): pass


class XplovaUtility:
    """
    utility class for uploading/exporting activity file through xplova's website
    """

    # necessary URLs
    auth_url = 'http://tour.xplova.com/userAccount/login.php'
    upload_url = 'http://tour.xplova.com/inc/uploadActivity.php'
    export_url = 'http://tour.xplova.com/inc/exportActivity.php?activity_id=%s&format=gpx'


    def authenticate(self, user, passwd):
        login_data = urllib.urlencode( [('user', user),('pwd', passwd)] )

        opener = register_openers()
        opener.add_handler(urllib2.HTTPCookieProcessor( \
                cookielib.CookieJar()))
        try:
            req = urllib2.Request(self.auth_url, login_data)
            login_ret = json.loads(urllib2.urlopen(req).read())
        except Exception, e:
            raise LoginException("Authentication error: %s" % e)

        if login_ret['ret'] == 'RET_OK':
            print "Login successful! UserId: %s, UserName: %s" % \
                (login_ret["userId"], login_ret["userName"])
        else:
            raise LoginException( "Login failed [%s]. Detailed info: %s" % \
                (login_ret['ret'], login_ret) )


    def upload(self, f):
        values = {'upload_activity': f}
        data, headers = multipart_encode(values)
        headers['User-Agent'] = USER_AGENT

        req = urllib2.Request(self.upload_url, data, headers)
        req.unverifiable = True

        print "Uploading..."
        try:
            res= urllib2.urlopen(req)
            ret = res.read()

            if "RET_OK" not in ret:
                raise UploadException("Upload failed. Full response: \n%s" % ret)
        except Exception, e:
            raise UploadException("Cannot upload: %s" % e)

        print "Upload successful!"
        r = re.search("activity_id\\\\\"\:(\d+)", ret)
        if r:
            activity_id = int(r.group(1))
            print "Activity ID: %d" % activity_id
            return activity_id
        else:
            raise UploadException("Cannot determine activity_id! Full response: \n%s" % ret)
        

    def export(self, act_id, export_filename):
        req = urllib2.Request(self.export_url % act_id)
        req.add_header('Referer', 'http://tour.xplova.com/userActivity/')
        req.add_header('User-Agent', USER_AGENT)
        try:
            res = urllib2.urlopen(req)
            with open(export_filename, 'w') as f:
                f.write(res.read())
            print "GPX file successfully exported to %s!" % export_filename
        except Exception as e:
            raise ExportException("Exporting error: %s" % e)

    pass


if __name__ == '__main__':
    # build argument parser
    parser = argparse.ArgumentParser(\
            description = 'Auto uploader script for sport activity sites')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-a', '--activity', help = 'activity_id to export to gpx file')
    group.add_argument('-i', '--import-file', type = argparse.FileType('r'), \
            help = 'file to upload')
    parser.add_argument('-o', '--export-gpx', help = 'exported gpx filename')
    parser.add_argument('-u', '--user', help = 'Login username')
    parser.add_argument('-p', '--passwd', help = 'Login password')
    parser.add_argument('-v', '--version', action='version', \
            version='%(prog)s 1.0')
    args = parser.parse_args()

    # additional parameter checking (don't know how to do that in argparse)
    if args.activity and args.export_gpx is None:
        parser.error("-a and -o should be specified together")

    # prompt user/passwd
    if args.user is None:
        args.user = raw_input("Username: ")
    if args.passwd is None:
        args.passwd = getpass.getpass("Password: ")

    # do the job
    xplova = XplovaUtility()
    try:
        xplova.authenticate(args.user, args.passwd)
        if args.activity is None:
            args.activity = xplova.upload(args.import_file)
        if args.export_gpx:
            xplova.export(args.activity, args.export_gpx)
    except Exception as e:
        print e
        sys.exit(1)
    pass

