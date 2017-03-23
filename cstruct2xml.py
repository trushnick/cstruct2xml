#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import optparse
import os
import codecs
import lxml.etree as et # xslt
from lib.extractor import Extractor
from lib.lexer import Lexer
from lib.parser import Parser, ParserError
from lib.convert import convert, convert_file
import lib.resolver as resolver


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
    extractor = Extractor(file_path, options.encoding)
    original_file_name = os.path.splitext(os.path.basename(file_path))[0]
    structures = []
    root_dir_name = options.directory if options.directory \
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
            print("Found structure {}".format(structure.name))
            structures.append(structure)
            if not options.file_only:
                xml = convert(structure)
                dir_name = os.path.join(root_dir_name, original_file_name)
                if not os.path.exists(dir_name):
                    os.mkdir(dir_name)
                with open(os.path.join(dir_name, structure.name + '.xml'), 'wb') as f:
                    f.write(et.tostring(xml, xml_declaration=True, encoding=_encoding, pretty_print=True))
    xml = convert_file(original_file_name, structures)
    xml = resolver.resolve(xml, extractor.defines())
    with open(os.path.join(root_dir_name, original_file_name + '.xml'), 'wb') as f:
        f.write(et.tostring(xml, encoding=_encoding, pretty_print=True))
    transformed = transform(xml) # tree
    transformed.write(os.path.join(root_dir_name, original_file_name + '-transformed.xml'),
                      xml_declaration=True, encoding=_encoding, pretty_print=True)
    print("Done.")


# Parse options and arguments
opt_parser = optparse.OptionParser()
opt_parser.add_option('-e', '--enc', dest='encoding', default='utf-8',
                      help='Use specific encoding for files', metavar='ENC')
opt_parser.add_option('-d', dest='directory', default='',
                      help='Output XML-file to specific directory', metavar='DIR')
opt_parser.add_option('--file-only', action='store_true', dest='file_only', default=False,
                      help='Generate only overall xml for each file')
opt_parser.add_option('--xslt', dest='xslt', default='',
                      help='XSLT file to transform XML to desired format', metavar='XSLT')
options, args = opt_parser.parse_args()

# Verify that options are correct
try:
    codecs.lookup(options.encoding)
except LookupError:
    print("Encoding " + options.encoding + " is not supported!")
    exit(1)
_encoding = options.encoding
if options.directory:
    if not os.path.isdir(options.directory):
        print("Directory '" + options.directory + "' doesn't exists")
        exit(1)
if options.xslt:
    xsl = et.parse(options.xslt)
    transform = et.XSLT(xsl)  # XSL transformation function

print("Using encoding: " + options.encoding)
print("Using output directory: " +
      (options.directory if options.directory else 'DEFAULT ([file-dir]/cstruct2xml-output/)'))
if options.file_only:
    print("Generating one output xml per file")
else:
    print("Generating xml file for each structure + overall for file")

for arg in args:
    if os.path.isdir(arg):
        process_dir(arg)
    elif os.path.isfile(arg):
        process_file(arg)
    else:
        print("Wrong argument: '" + arg + "'! Skipping...")
