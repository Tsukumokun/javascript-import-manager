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

import jim_config as config
import jim_cache as cache

# Print and error message and exit
def _dispatcher_error(message):
    print('jim: dispatcher error: ' + message)
    exit(1)

# Dispatch from arguments sub parsers
def _dispatcher_dispatch(args):
    if args.which == 'config':
        _dispatcher_config(args)
    elif args.which == 'cache':
        _dispatcher_cache(args)
    else:
        _dispatcher_make(args)

# Dispatch to configuration
def _dispatcher_config(args):
    if args.config_get != None:
        print config._global_get_setting(args.config_get[0])
    elif args.config_global != None:
        config._global_set_setting(args.config_global[0],args.config_global[1])
    elif args.config_reset != None:
        config._global_reset_setting(args.config_reset[0])

# Dispatch to caching
def _dispatcher_cache(args):
    if args.cache_clear:
        cache._cache_clear()
    elif args.cache_rebuild:
        cache._cache_rebuild()
    elif args.cache_list:
        cache._cache_list()
    elif args.cache_add != None:
        cache._cache_add(args.cache_add[0])
    elif args.cache_remove != None:
        cache._cache_remove(args.cache_remove[0])

# Get a variant of the input file
def _dispatcher_get_input_variant(args):
    fileName, fileExtension = os.path.splitext(args.file)
    if args.no_minify:
        fileName += '.o'
    else:
        fileName += '.min'
    if fileExtension != '':
        fileName += fileExtension
    return fileName

# Get destination file
def _dispatcher_get_dest(args):
    dest = os.getcwd()+'/'
    if args.output != None:
        # If the output was absolute, retain it
        if os.path.isabs(args.output):
            dest = args.output
        # If not add it to the cwd
        else:
            dest = os.path.join(dest,args.output)
        # If the new output is a directory
        if os.path.isdir(dest):
            dest = os.path.join(dest,_dispatcher_get_input_variant(args))
    else:
        dest = os.path.join(dest,_dispatcher_get_input_variant(args))
    # Check if the new file location is writable
    os.access(os.path.dirname(dest), os.W_OK) or _dispatcher_error('destination is not writable')
    # Now ensure all directories to that file exist
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    return dest

# Dispatch to making
def _dispatcher_make(args):
    nocache = config._global_get_setting('nocache')
    if args.no_cache:
        nocache = True
    nominify = config._global_get_setting('nominify')
    if args.no_minify:
        nominify = True
    compiler._compile_make(args.file,dest,args.rebuild,nocache)
    if not nominify:
        compiler._compile_minify(dest)



