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
import re
from sets import Set
import urllib

import jim_cache as cacher

repeat_set = Set();

def _compile_error(message):
    print('jim: compile error: ' + message)
    exit(1)

# Checks the line where an import was detected
def _compile_import(line):
    # Attempt to match the import for syntax
    vals = re.match("^[ ]*(//|/\*|\*)?[ ]*@[a-zA-Z]+( *?\((['](?P<f>([^']|\\')+)[']|[\"](?P<g>([^\"]|\\\")+)[\"]|(?P<h>([^\()'\"]|\\\"|\\')+))[\)]| +(['](?P<i>([^']|\\')+)[']|[\"](?P<j>([^\"]|\\\")+)[\"])) *$",line).groupdict().values()
    for val in vals:
        if val != None:
            return val
    # If nothing was found alert a compile error
    _compile_error('import syntax error: '+line)

# Recursively build the output file
def _compile_recurse(in_file,out_fd,force,nocache,loop_set):
    # If the file is already in the set alert a compile error
    if in_file in loop_set:
        error = 'dependency loop encountered'
        for f in loop_set:
            error += '\n\t'+f
        error += '\n\t'+in_file
        _compile_error(error)
    # Otherwise add it to the set
    else:
        loop_set.add(in_file)
    # Given the file was not a loop, check if
    #  it has already been included
    if in_file in repeat_set:
        return
    # If not add it to check against later
    else:
        repeat_set.add(in_file)
    # If the file is not located on the system
    #  attempt to download it if not nocache
    is_nocache = False
    if not os.path.isfile(in_file):
        if not in_file.startswith('nocache:'):
            if not nocache:
                in_file = cacher._cache_get(in_file,force)
            else:
                is_nocache = True
        else:
            in_file = in_file[8:]
            is_nocache = True

    # Print into the output file the name of the included one
    out_fd.write('//File: '+in_file+'\n')
    # Open the included one and parse all of it into 
    #  a string object to be split by line
    data = None
    try:
        if no is_nocache:
            with open(in_file, 'r') as fp:
                data = fp.read()
        else:
            with urllib.urlopen(in_file) as fp:
                data = fp.read()
    except:
        _compile_error('failed to read file: '+in_file)

    # For every new line in the file
    for line in data.split('\n'):
        # If an import statement is not found
        #  write the line into the output file
        if line.find('@import') < 0:
            out_fd.write(line+'\n')
        # Otherwise recursively call this function
        #  to include the imported file
        else:
            nset = Set()
            nset.update(loop_set)
            _compile_recurse(_compile_import(line),out_fd,force,nset)
    # Write out that the file has completed and been included
    out_fd.write('//End File: '+in_file+'\n')

# Actually compile the new file 
def _compile_make(in_file,out_file,force,nocache):
    repeat_set = Set()
    with open(out_file, 'w') as fp:
        _compile_recurse(in_file,fp,force,nocache,Set())

# Minify the input file inplace using yui
def _compile_minify(_file):
    os.system('java -jar '+os.path.dirname(os.path.realpath(__file__))+'/yuicompressor.jar --type js '+_file+' -o '+_file) > 0 \
    and die('minification process failed')

