#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import optparse
import os
import codecs
from cstruct2xml.extractor import Extractor
from cstruct2xml.lexer import Lexer
from cstruct2xml.parser import Parser, ParserError
from cstruct2xml.convert import convert, convert_file
import cstruct2xml.resolver as resolver


def process_dir(dir_path):
    print("Processing directory: " + dir_path)
    for path in os.listdir(dir_path):
        full_path = os.path.join(dir_path, path)
        if os.path.isdir(full_path):
            process_dir(full_path)
        elif os.path.isfile(full_path):
            process_file(full_path)


def process_file(file_path):
    print("Processing: " + file_path + "...")
    extractor = Extractor(file_path, _encoding)
    original_file_name = os.path.splitext(os.path.basename(file_path))[0]
    structures = []
    root_dir_name = _output_directory if _output_directory \
                    else os.path.join(os.path.dirname(file_path), 'cstruct2xml-output')
    if not os.path.exists(root_dir_name):
        os.mkdir(root_dir_name)
    for definition in extractor:
        lexer = Lexer(definition)
        parser = Parser(lexer)
        try:
            structure = parser.parse()
        except ParserError as e:
            print("Coudln't parse structure {}.\nError message: {}".format(
                    parser.structure.name if parser.structure.name else '%no_name%',
                    e.message))
        else:
            print("Found structure named {}".format(structure.name))
            structures.append(structure)
            if not _one_output_per_file:
                xml = convert(structure)
                dir_name = os.path.join(root_dir_name, original_file_name)
                if not os.path.exists(dir_name):
                    os.mkdir(dir_name)
                with open(os.path.join(dir_name, structure.name + '.xml'), 'w', encoding=_encoding) as f:
                    f.write(xml)
    xml = convert_file(original_file_name, structures)
    xml = resolver.resolve(xml, extractor.defines())
    with open(os.path.join(root_dir_name, original_file_name + '.xml'), 'w', encoding=_encoding) as f:
        f.write(xml)
    print("Done.")


_encoding = 'utf-8'
_output_directory = ''
_one_output_per_file = False
opt_parser = optparse.OptionParser()
opt_parser.add_option('-e', '--enc', dest='encoding',
                      help='Use specific encoding for files. Default is utf-8.', metavar='ENC')
opt_parser.add_option('-d', dest='directory',
                      help='Output XML-file to specific directory.', metavar='DIR')
opt_parser.add_option('--file-only', action='store_true', dest='file_only', default=False,
                      help='Generate only one xml per file')
options, args = opt_parser.parse_args()
if options.encoding:
    try:
        codecs.lookup(options.encoding)
    except LookupError:
        print("Encoding " + options.encoding + " is not supported!")
        print(opt_parser.usage)
        exit(1)
    _encoding = options.encoding
if options.directory:
    if not os.path.isdir(options.directory):
        print("Directory '" + options.directory + "' doesn't exists")
        exit(1)
    _output_directory = options.directory
    _output_directory = 'DEFAULT ([file-dir]/cstruct2xml-output/)'
if options.file_only:
    _one_output_per_file = True

print("Using encoding: " + _encoding)
print("Using output directory: " +
        _output_directory if _output_directory else 'DEFAULT ([file-dir]/cstruct2xml-output/)')
print("Converting files: " + str(args))
if _one_output_per_file:
    print("Generating one output xml per file")
else:
    print("Generating xml file for each structure + overall for file")

if len(args) == 0:
    print("No files provided, exiting.")
    exit(0)
for arg in args:
    if os.path.isdir(arg):
        process_dir(arg)
    elif os.path.isfile(arg):
        process_file(arg)
    else:
        print("Wrong argument: '" + arg + "'! Skipping...")
