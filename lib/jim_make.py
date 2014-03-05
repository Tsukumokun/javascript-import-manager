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
import uuid

import jim_cache as cacher

repeat_set = Set()

package_set = Set()
package_dict = {}

def _compile_error(message):
    print('jim: compile error: ' + message)
    exit(1)

# Check for repeated or looping dependencies
def _compile_data(_file,nocache):
    data = None
    try:
        if not nocache:
            with open(_file, 'r') as fp:
                data = fp.read()
        else:
            with urllib.urlopen(_file) as fp:
                data = fp.read()
    except:
        _compile_error('failed to read file: '+in_file)
    return data

# Check for import or include
def _compile_check(line,out_fd,nocache,force):
    # Check for import
    vals = re.match("^ *(//|/\*|\*)? *import +(?P<c>(nocache:)?)(?P<f>[^ ]+)( +as +(?P<a>[^ ]+))? *$",line)
    if vals != None:
        if vals.group('c') != None:
            nocache = True
        _as = vals.group('a')
        if _as == None:
            _as = os.path.splitext(\
                  os.path.basename(\
                  vals.group('f')))[0]\
                  .replace('-','_')
        _compile_import(vals.group('f'),out_fd,_as,nocache,force)
        return ''
    # Check for include
    vals = re.match("^ *(//|/\*|\*)? *include +(?P<c>(nocache:)?)(?P<f>[^ ]+) *$",line)
    if vals != None:
        if vals.group('c') != None:
            nocache = True
        _compile_include(_file,out_fd,nocache,force)
        return ''
    # Otherwise return the line to be printed
    return line+'\n'

# Includes a file without making it a module
def _compile_include(_file,out_fd,nocache,force):
    pass

# Imports a file as a module
def _compile_import(_file,out_fd,_as,nocache,force):
    # Buffer file to check for imports
    _buffer = ''
    for line in _compile_data(_file,nocache):
        _buffer += _compile_check(line)
    # Check for existing package alias
    if _as in package_set:
        _compile_error('package with this name already exists: '+_as)
    package_set.add(_as)
    # Check for existing package
    if _file in package_dict:
        out_fd.write('var '+_as+' = '+package_dict[_file])
    else:
    package = '_'+uuid.uuid4().hex
    # Add the package closure
    out_fd.write('(function('+package+'){\n')
    # Put the file in place
    out_fd.write(_buffer)
    # End the package closure
    out_fd.write('}('+package+'={}))\n')
    # Alias to the given name
    out_fd.write('var '+_as+' = '+package+'\n')
    return
    # Attempt to match the import for syntax
    #vals = re.match("^[ ]*(//|/\*|\*)?[ ]*@[a-zA-Z]+( *?\((['](?P<f>([^']|\\')+)[']|[\"](?P<g>([^\"]|\\\")+)[\"]|(?P<h>([^\()'\"]|\\\"|\\')+))[\)]| +(['](?P<i>([^']|\\')+)[']|[\"](?P<j>([^\"]|\\\")+)[\"])) *$",line).groupdict().values()
    vals = re.match("^ *(//|/\*|\*)? *import +(?P<c>(nocache:)?)(?P<f>[^ ]+)( +as +(?P<a>[^ ]+))? *$",line)

    #for val in vals:
    #    if val != None:
    #        return val
    # If nothing was found alert a compile error
    _compile_error('import syntax error: '+line)

# Recursively build the output file
def _compile_recurse(in_file,out_fd,force,nocache,module,loop_set):
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
        if not is_nocache:
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
            _compile_recurse(_compile_import(line),out_fd,force,is_nocache,Set(loop_set))
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

