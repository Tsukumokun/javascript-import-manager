#
# JIM - a javascript import manager
# Copyright (C) 2014 Christopher Kelley   <tsukumokun(at)icloud.com>
# 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 
# International License. To view a copy of this license, visit 
# http://creativecommons.org/licenses/by-nc-nd/4.0/deed.en_US.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# 

import json
import os

def _cache_error(message):
    print("jim: caching error: " + message)
    exit(1)

def _cache_read():
    if not os.path.exists('/var/cache/jim/jim-dependencies.json')
        with open('/var/cache/jim/jim-dependencies.json', 'wb') as fp:
            fp.write(json.dumps({'count':0,'files':[ ]}))
    with open('/var/cache/jim/jim-dependencies.json', 'rb') as fp:
        data = json.load(fp)
    return data

def _cache_get(_file):
    # Read in cache count
    data = _cache_read();
    print data;
    # Attempt to retrieve file and place in cache
    #print "Retrieving file: "+_file
    #os.system("curl -# -o") > 0 \
    #and die("minification process failed")

