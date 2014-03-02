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

import os
import json

def _global_name():
    return '/var/cache/jim/jim-configuration.json'

def _global_error(message):
    print("jim: global error: " + message)
    exit(1)

# Ensures the globals file is present
def _global_ensure():
    _file = _global_name()
    # If there is no configuration file create one
    if not os.path.exists(_file):
        os.access(os.path.dirname(_file), os.W_OK) \
        or _cache_error("configuration is not writable, something went wrong")
        # Dump a default json object into the file
        with open(_file, 'wb') as fp:
            fp.write(json.dumps({
                "nocache":False,
                "nominify":False
            }))

# Returns the globals as an associative array
def _global_read():
    _global_ensure()
    # Load the file into data and return it
    with open(_global_name(), 'rb') as fp:
        data = json.load(fp)
    return data

# Writes the associative array out to the globals
def _global_write(data):
    with open(_global_name(), 'wb') as fp:
        fp.write(json.dumps(data))

# Sets a global setting variable
def _global_set_setting(setting,value):
    data = _global_read()
    data[setting] = bool(value)
    _global_write(data)

# Toggles a global setting variable
def _global_toggle_setting(setting):
    data = _global_read()
    data[settting] = not data[setting]
    _global_write(data)

