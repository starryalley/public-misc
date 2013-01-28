#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from collections import defaultdict

if __name__ == '__main__':
    try:
        f = open(sys.argv[1])
    except:
        print "A www.tiki-toki.com timeline json search tool\n"
        print "Usage: %s timeline_json\n\n" % sys.argv[0]
        sys.exit(1)

    # read json data
    data = f.read()
    data = data.replace('var TLTimelineData = ', '')

    # if strict is False (True is the default), 
    # then control characters will be allowed inside strings.
    j = json.loads(data, strict = False) 

    # statistics about categories
    cat = defaultdict(int)
    for s in j['stories']:
        cat[ s['category'] ] += 1

    # print information
    print "Total Story Count:%d" % len(j['stories'])
    print "Categories:"
    for c in sorted(j['categories'], key = lambda s: cat[str(s['id'])], reverse = True):
        print " -[%s]: %d (%.2f%%)" % \
                (c['title'], cat[str(c['id'])], \
                float(cat[str(c['id'])])/len(j['stories'])*100)

    # do search
    term = raw_input("Search:")
    term = term.lower()
    term = unicode(term, 'utf-8')

    result = []
    for s in sorted(j['stories'], key = lambda s: s['startDate']):
        if term in s['title'].lower():
            result.append("[%s]: %s (found in title)" % (s['startDate'].split(' ')[0], s['title']))
            continue
        if term in s['text'].lower() or term in s['fullText'].lower():
            result.append("[%s]: %s (found in text)" % (s['startDate'].split(' ')[0], s['title']))
            continue
        for m in s['media']:
            if term in m['caption'].lower():
                result.append("[%s]: %s (found in media caption)" % (s['startDate'].split(' ')[0], s['title']))
                break
    if len(result) == 0:
        print "Not found!"
        sys.exit(0)
    print "Total %d Found:" % len(result)
    for r in result:
        print " - %s" % r
           
    
