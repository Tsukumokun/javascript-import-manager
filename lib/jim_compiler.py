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

import jim_cacher as cacher

repeat_set = Set();

def _compile_error(message):
    print("jim: compile error: " + message)
    exit(1)

def _compile_import(line):
    vals = re.match("^[ ]*(//|/\*|\*)?[ ]*@[a-zA-Z]+( *?\((['](?P<f>([^']|\\')+)[']|[\"](?P<g>([^\"]|\\\")+)[\"]|(?P<h>([^\()'\"]|\\\"|\\')+))[\)]| +(['](?P<i>([^']|\\')+)[']|[\"](?P<j>([^\"]|\\\")+)[\"])) *$",line).groupdict().values()
    for val in vals:
        if val != None:
            return val
    _compile_error("import syntax error: "+line)

def _compile_recurse(in_file,out_fd,force,loop_set):
    if in_file in loop_set:
        error = "dependency loop encountered"
        for f in loop_set:
            error += "\n\t"+f
        error += "\n\t"+in_file
        _compile_error(error)
    else:
        loop_set.add(in_file)
    if in_file in repeat_set:
        return
    else:
        repeat_set.add(in_file)
    if not os.path.isfile(in_file):
        in_file = cacher._cache_get(in_file,force)
    out_fd.write("//File: "+in_file+"\n")
    with open(in_file, 'r') as fp:
        data = fp.read()
    for line in data.split('\n'):
        if line.find("@import") < 0:
            out_fd.write(line+"\n")
        else:
            nset = Set()
            nset.update(loop_set)
            _compile_recurse(_compile_import(line),out_fd,force,nset)
    out_fd.write("//End File: "+in_file+"\n")

def _compile(in_file,out_file,force):
    repeat_set = Set()
    with open(out_file, 'w') as fp:
        _compile_recurse(in_file,fp,force,Set())

def _compile_rebuild():
    cacher._cache_rebuild()
def _compile_clearcache():
    cacher._cache_clear()

