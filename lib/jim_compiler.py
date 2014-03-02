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

import jim_cacher as cacher

def _compile_error(message):
    print("jim: compile error: " + message)
    exit(1)

def _compile_import(line):
    vals = re.match("^[ ]*(//|/\*|\*)?[ ]*@[a-zA-Z]+( *?\((['](?P<f>([^']|\\')+)[']|[\"](?P<g>([^\"]|\\\")+)[\"]|(?P<h>([^\()'\"]|\\\"|\\')+))[\)]| +(['](?P<i>([^']|\\')+)[']|[\"](?P<j>([^\"]|\\\")+)[\"])) *$",line).groupdict().values()
    for val in vals:
        if val != None:
            return val
    _compile_error("import syntax error: "+line)

def _compile_recurse(in_file,out_fd,force):
    if not os.path.isfile(in_file):
        in_file = cacher._cache_get(in_file,force)
    with open(in_file, 'r') as fp:
        data = fp.read()
    for line in data.split('\n'):
        if line.find("@import") < 0:
            out_fd.write(line+"\n")
        else:
           _compile_recurse(_compile_import(line),out_fd,force)

def _compile(in_file,out_file,force):
    with open(out_file, 'w') as fp:
        _compile_recurse(in_file,fp,force)

def _compile_rebuild():
    cacher._cache_rebuild()

