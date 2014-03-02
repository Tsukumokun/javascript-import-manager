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
import fileinput
import os
import re

import jim_compiler as compiler

def die(message):
    print("jim: error: " + message)
    exit(1)

parser = argparse.ArgumentParser(prog="jim",description='Javascript Import Manager')
parser.add_argument('file', type=str,
                   help='a file for the compiler', nargs="?")
parser.add_argument('-M', '--no-minify', dest='no_minify', action='store_true',
                   default=False,
                   help='do not minify, only compile the file')
parser.add_argument('-r', '--rebuild', dest='rebuild', action='store_true',
                   default=False,
                   help='forces a rebuild of the local caches - note: if used with '+
                   'a file this will only rebiuld the associated files, if used '+
                   'alone this will rebuild the entire cache')
parser.add_argument('-c', '--clear-cache', dest='clear', action='store_true',
                   default=False,
                   help='removes all of the local caches - note: if used with '+
                   'a file this will rebiuld the associated files, if used '+
                   'alone this will only empty the cache')
parser.add_argument('-o', '--output', metavar='output', dest='output', type=str,
                   help='destination to output to, may be a file or directory')

args = parser.parse_args()

if args.file == None:
    if args.rebuild:
        compiler._compile_rebuild()
    elif args.clear:
        compiler._compile_clearcache()
    else:
        die("no file specified, and rebuild not requested")
    exit(0)
if args.clear:
    compiler._compile_clearcache()

#Set up where the file should go, will be saved to dest
dest = os.getcwd()+"/"
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
            dest += fileName + ".o"
        else:
            dest += fileName + ".min"
        if fileExtension != "":
            dest += fileExtension
# If not, add an input file variation to the cwd
else:
    if args.no_minify:
        dest += fileName + ".o"
    else:
        dest += fileName + ".min"
    if fileExtension != "":
            dest += fileExtension
# Check if the new file location is writable
os.access(os.path.dirname(dest), os.W_OK) or die("destination is not writable")
# Now ensure all directories to that file exist
if not os.path.exists(os.path.dirname(dest)):
    os.makedirs(os.path.dirname(dest))

def _minify(_file):
    os.system("java -jar "+os.path.dirname(os.path.realpath(__file__))+'/yuicompressor.jar --type js '+_file+' -o '+_file) > 0 \
    and die("minification process failed")

compiler._compile(args.file,dest,args.rebuild)

