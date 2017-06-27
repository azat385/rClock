# -*- coding: utf-8 -*-

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

data = ["CO2", "T", "ts"]

value = mc.get_multi(data)

for k,v in value.iteritems():
    print "{} = {}".format(k,v)