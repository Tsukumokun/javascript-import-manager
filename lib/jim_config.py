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

truth = ['true', 't', 'True', 'T', 'on', 'yes', 'y']
#lies  = ['false', 'f', 'False', 'F', 'off', 'no', 'n']
toggle = ['toggle', 'Toggle']

def _global_name():
    return '/var/cache/jim/jim-configuration.json'

def _global_default():
    return {'nocache':False,'nominify':False}

def _global_error(message):
    print('jim: global error: ' + message)
    exit(1)

# Ensures the globals file is present
def _global_ensure():
    _file = _global_name()
    # If there is no configuration file create one
    if not os.path.exists(_file):
        os.access(os.path.dirname(_file), os.W_OK) \
        or _global_error('configuration is not writable, something went wrong')
        # Dump a default json object into the file
        with open(_file, 'wb') as fp:
            fp.write(json.dumps(_global_default() ) )

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
    if value in toggle:
        _global_toggle_setting(setting)
        return
    data = _global_read()
    if setting in data:
        data[setting] = value in truth
        _global_write(data)
    else:
        _global_error('setting '+setting+' not found')

# Toggles a global setting variable
def _global_toggle_setting(setting):
    data = _global_read()
    if setting in data:
        data[setting] = not data[setting]
        _global_write(data)
    else:
        _global_error('setting '+setting+' not found')

# Gets a global setting variable
def _global_get_setting(setting):
    data = _global_read()
    if setting in data:
        return data[setting]

# Resets a global setting variable
def _global_reset_setting(setting):
    data = _global_read()
    if setting in data:
        data[setting] = _global_default()[setting]
        _global_write(data)
    else:
        _global_error('setting '+setting+' not found')

def _global_list_settings():
    data = _global_read()
    print json.dumps(data,sort_keys=True,
        indent=4, separators=(',', ': '))

