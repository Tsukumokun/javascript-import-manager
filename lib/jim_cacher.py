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
import uuid

def _cache_error(message):
    print("jim: caching error: " + message)
    exit(1)

def _cache_read():
    if not os.path.exists('/var/cache/jim/jim-dependencies.json'):
        os.access(os.path.dirname('/var/cache/jim/jim-dependencies.json'), os.W_OK) \
        or _cache_error("cache is not writable, something went wrong")
        with open('/var/cache/jim/jim-dependencies.json', 'wb') as fp:
            fp.write(json.dumps({}))
    with open('/var/cache/jim/jim-dependencies.json', 'rb') as fp:
        data = json.load(fp)
    return data

def _cache_store(data,_file):
    print "No cache found, retrieving file: " + _file
    # Make a uuid name for the new file
    uuid_name = '/var/cache/jim/'+uuid.uuid4().hex+'.jim_cache'
    # Attempt to retrieve file and place in cache
    os.system('curl -# '+_file+' -o '+uuid_name) > 0 \
    and _cache_error("failed to download file for caching")
    # Update the file table
    data[_file] = uuid_name
    return data

def _cache_restore(_file):
    print "Forced rebuild, retrieving file: " + _file
    # Attempt to retrieve file and place in cache
    os.system('curl -# '+_file+' -o '+data[_file]) > 0 \
    and _cache_error("failed to download file for caching")

def _cache_get(_file,force):
    # Read in cache count
    data = _cache_read()
    # If the file was not found, load it
    if not _file in data:
        data = _cache_store(data,_file)
    # If the file was found but told to force, restore the file
    elif force:
        _cache_restore(_file)
    # Save new cache data
    with open('/var/cache/jim/jim-dependencies.json', 'wb') as fp:
        fp.write(json.dumps(data))
    return data[_file]

