#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
from pprint import pprint
from geopy.distance import vincenty


URL='http://opendata.epa.gov.tw/ws/Data/RainTenMin/?$orderby=PublishTime%20desc&$skip=0&$top=1000&format=json'


# TWD67 X: 310040
# TWD67 Y: 2775444
# TWD67: 121.595214707211,25.0859913590691
# GPS:   121.6035488, 25.0860434
current_loc = (121.595214707211,25.0859913590691)
data = json.loads(urllib2.urlopen(URL).read())
dist = {}

# find nearest site:
for e in data:
    loc = (e['TWD67Lon'], e['TWD67Lat'])
    dist[e['SiteId']] = vincenty(current_loc, loc)

min_val = min(dist.itervalues())
nearest = [k for k, v in dist.iteritems() if v == min_val]
nearest_site = [k for k in data if k['SiteId'] == nearest[0]]

print "Nearest site ID:", nearest[0]
for k, v in nearest_site[0].iteritems():
    print "%s: %s" % (k, v)

