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

import argparse
import sys

##SHOULD REMOVE
import fileinput
import os
import re


import jim_dispatcher as dispatcher

def die(message):
    print('jim: error: ' + message)
    exit(1)

parser = argparse.ArgumentParser(prog='jim',description='Javascript Import Manager')
sp = parser.add_subparsers()

# Sub parser for configuration
sp_config = sp.add_parser('config', help='manage configuration')
mgroup = sp_config.add_mutually_exclusive_group(required=True)
mgroup.add_argument('--global', type=str, dest='config_global',
                        help='use global config file', nargs=2,
                        metavar=('name','value'))
mgroup.add_argument('--get', type=str, dest='config_get',
                        help='get value: name', nargs=1,
                        metavar='name')
mgroup.add_argument('--reset', type=str, dest='config_reset',
                        help='reset value: name', nargs=1,
                        metavar='name')
sp_config.set_defaults(which='config')

sp_cache = sp.add_parser('cache', help='manage cache')
mgroup = sp_cache.add_mutually_exclusive_group(required=True)
mgroup.add_argument('--clear', dest='cache_clear', action='store_true',
                        default=False, help='clear the cache')
mgroup.add_argument('--rebuild', dest='cache_rebuild', action='store_true',
                        default=False, help='rebuild the cache')
mgroup.add_argument('--list', dest='cache_list', action='store_true',
                        default=False, help='list all files in the cache')
mgroup.add_argument('--add', dest='cache_add', type=str,
                        nargs=1, metavar='file', help='add a remote file to the cache')
mgroup.add_argument('--remove', dest='cache_remove', type=str,
                        nargs=1, metavar='file', help='remove a remote file from to the cache')
sp_cache.set_defaults(which='cache')

sp_make = sp.add_parser('make', help='compile a file')
sp_make.add_argument('file', type=str,
                   help='a file for the compiler')
sp_make.add_argument('-M', '--no-minify', dest='no_minify', action='store_true',
                   default=False,
                   help='do not minify, overrides global')
sp_make.add_argument('-C', '--no-cache', dest='no_cache', action='store_true',
                   default=False,
                   help='do not cache, overrides global')
sp_make.add_argument('-o', '--output', metavar='output', dest='output', type=str,
                   help='destination to output to, may be a file or directory')
sp_make.set_defaults(which='make')

# Set default subparser
if  sys.argv[1] != 'config' and \
    sys.argv[1] != 'cache' and  \
    sys.argv[1] != 'make' and \
    not sys.argv[1].startswith('-'):
        sys.argv.insert(1,'make')
args = parser.parse_args()

dispatcher._dispatcher_dispatch(args)

exit(0)


#Set up where the file should go, will be saved to dest
dest = os.getcwd()+'/'
fileName, fileExtension = os.path.splitext(args.file)
# If output is specified make it the destination file
if args.output != None:
    # If the output was absolute, retain it
    if os.path.isabs(args.output):
        dest = args.output
    # If not add it to the cwd
    else:
        dest += args.output
    # If the new output is a directory
    if os.path.isdir(dest):
        # Add an input file variation to it
        if args.no_minify:
            dest += fileName + '.o'
        else:
            dest += fileName + '.min'
        if fileExtension != '':
            dest += fileExtension
# If not, add an input file variation to the cwd
else:
    if args.no_minify:
        dest += fileName + '.o'
    else:
        dest += fileName + '.min'
    if fileExtension != '':
            dest += fileExtension
# Check if the new file location is writable
os.access(os.path.dirname(dest), os.W_OK) or die('destination is not writable')
# Now ensure all directories to that file exist
if not os.path.exists(os.path.dirname(dest)):
    os.makedirs(os.path.dirname(dest))



compiler._compile(args.file,dest,args.rebuild)

