#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import optparse
import os
import codecs
from cstruct2xml import *


def _process_dir(dir_path):
    print("Processing directory: " + dir_path)
    for path in os.listdir(dir_path):
        full_path = os.path.join(dir_path, path)
        if os.path.isdir(full_path):
            _process_dir(full_path)
        elif os.path.isfile(full_path):
            _process_file(full_path)


def _process_file(file_path):
    print("Processing: " + file_path + "... ", end='')
    definitions = [definition for definition in Extractor(file_path)]
    lexed_defs = [Lexer(definition) for definition in definitions]
    # TODO: parse and convert to xml (not implemented atm)
    print("Done.")


_encoding = 'utf-8'
_output_directory = ''
opt_parser = optparse.OptionParser()
opt_parser.add_option('-e', '--encoding', dest='encoding',
                      help='Use specific encoding for files. Default is utf-8.', metavar='ENCODING')
opt_parser.add_option('-d', dest='directory',
                      help='Output XML-file to specific directory.', metavar='DIR')
options, args = opt_parser.parse_args()
if options.encoding is not None:
    try:
        codecs.lookup(options.encoding)
    except LookupError:
        print("Encoding " + options.encoding + " is not supported!")
        print(opt_parser.usage)
        exit(1)
    _encoding = options.encoding
if options.directory is not None:
    if not os.path.isdir(options.directory):
        print("Directory '" + options.directory + "' doesn't exists")
        exit(1)
    _output_directory = options.directory
else:
    _output_directory = 'DEFAULT ([file-dir]/cstruct2xml-output/)'
print("Using encoding: " + _encoding)
print("Using output directory: " + _output_directory)
print("Converting files: " + str(args))
if len(args) == 0:
    print("No files provided, exiting.")
    exit(0)
for arg in args:
    if os.path.isdir(arg):
        _process_dir(arg)
    elif os.path.isfile(arg):
        _process_file(arg)
    else:
        print("Wrong argument: '" + arg + "'! Skipping...")







