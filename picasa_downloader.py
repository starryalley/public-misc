#!/usr/bin/python
#
# This interactive script prompts the user for an album to download.
# modified from http://psung.blogspot.tw/2009/12/manipulating-picasa-web-albums.html
#
# NOTE: do not use directly... it downloads everything...
#
# Author: Mark Kuo
# Date: 2012/8/3
#

import gdata.photos.service
import urllib
import getpass
import os, sys

def main():
    # authenticating
    email = raw_input("Username (e-mail): ")
    password = getpass.getpass("Password (optional):")
    client = login(email, password)

    # get album list for the user
    albums = client.GetUserFeed(user = email).entry
    album_ids = []

    # print and get interested albums
    for album in sorted(albums, key=lambda a: a.title.text):
        #if not album.title.text.startswith('Day'): continue
        album_ids.append((album.title.text, album.gphoto_id.text))
        print '%s (%3d photos) id = %s' % \
            (album.title.text, int(album.numphotos.text), album.gphoto_id.text)

    # download them
    download_albums(client, email, album_ids)


def login(email, password):
    gd_client = gdata.photos.service.PhotosService()
    if password.rstrip() == '':
        print "Log in as anonymous"
        return gd_client
    gd_client.email = email
    gd_client.password = password
    gd_client.source = 'MyPicasaDownloader'
    try:
        gd_client.ProgrammaticLogin()
    except:
        print "Login error.. aborted."
        sys.exit(1)
    return gd_client


def download_albums(client, email, albums):
    prefix="photo"
    for name, album_id in albums:
        print "Downloading album: %s" % name
        photos = client.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo&imgmax=d'
                               % (email, album_id))
        path = os.path.join(prefix, name)
        try:
            os.makedirs(path)
        except OSError:
            pass
        for photo in photos.entry:
            download_file(photo.content.src, path)


def download_file(url, path):
    print "   Downloading photo:%s" % (basename,)
    basename = url[url.rindex('/') + 1:]
    urllib.urlretrieve(url, os.path.join(path, basename))

if __name__ == '__main__':
    main()

