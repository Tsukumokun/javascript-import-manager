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

import jim_config as config

def _cache_name():
    return '/var/cache/jim/jim-dependencies.json'

def _cache_default():
    return {}

def _cache_error(message):
    print('jim: caching error: ' + message)
    exit(1)

# Ensures the cache file is present
def _cache_ensure():
    _file = _cache_name()
    # If there is no configuration file create one
    if not os.path.exists(_file):
        os.access(os.path.dirname(_file), os.W_OK) \
        or _cache_error('cache is not writable, something went wrong')
        # Dump a default json object into the file
        with open(_file, 'wb') as fp:
            fp.write(json.dumps(_cache_default() ) )

# Returns the cache as an associative array
def _cache_read():
    _cache_ensure()
    # Load the file into data and return it
    with open(_cache_name(), 'rb') as fp:
        data = json.load(fp)
    return data

# Writes the associative array out to the cache
def _cache_write(data):
    with open(_cache_name(), 'wb') as fp:
        fp.write(json.dumps(data))

# Stores a file in the cache
def _cache_store(data,_file):
    print 'no cache found, retrieving file: ' + _file
    # Make a uuid name for the new file
    uuid_name = '/var/cache/jim/'+uuid.uuid4().hex+'.jim_cache'
    # Attempt to retrieve file and place in cache
    os.system('curl -# '+_file+' -o '+uuid_name) > 0 \
    and _cache_error('failed to download file for caching')
    # Update the file table
    data[_file] = uuid_name
    return data

# Restores a file in the cache, file must have been stored already
def _cache_restore(remote_file,cached_file):
    print 'forced rebuild, retrieving file: ' + remote_file
    # Attempt to retrieve file and place in cache
    os.system('curl -# '+remote_file+' -o '+cached_file) > 0 \
    and _cache_error('failed to download file for caching')

# Gets a file name from the cache
def _cache_get(_file,force):
    # Read in cache data
    data = _cache_read()
    # If the file was not found, load it
    if not _file in data:
        data = _cache_store(data,_file)
    # If the file was found but told to force, restore the file
    elif force:
        _cache_restore(_file,data[_file])
    # Save new cache data
    _cache_write(data)
    return data[_file]

# Rebuilds the entire cache
def _cache_rebuild():
    # Read in cache data
    data = _cache_read()
    # Restore every file in the cache
    for _file in data:
        _cache_restore(_file,data[_file])
    print 'cache was rebuilt'

# Rebuilds only one file
def _cache_rebuild_one(_file):
    # Read in cache data
    data = _cache_read()
    # Restore every file in the cache
    if _file in data:
        _cache_restore(_file,data[_file])
    else:
        _cache_error('file not found in cache')
    print _file+' was rebuilt'

# Clears the entire cache
def _cache_clear():
    folder = '/var/cache/jim/'
    for _file in os.listdir(folder):
        if _file != config._global_name():
            file_path = os.path.join(folder,_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    print 'cache was cleared'

# Adds a specific file to the cache
def _cache_add(_file):
    _cache_get(_file,False)

# Removes a specific file from the cache
def _cache_remove(_file):
    # Read in cache data
    data = _cache_read()
    if not _file in data:
        _cache_error('file not found in cache')
    os.unlink(data[_file])
    del data[_file]
    # Save new cache data
    _cache_write(data)
    print 'file removed from cache'

# Lists all files in the cache
def _cache_list():
    # Read in cache data
    data = _cache_read()
    for _file in data:
        print _file

