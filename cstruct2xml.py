#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os

_pattern = re.compile(r'(?:(?:(?://[^\n]*\n)|(?:/\*(?:[^*]|(?:\*[^/]))*\*/))\s*)*'
                      r'typedef\s+struct\s+(?:[\w_][\w\d_]*)?\s*\{')
_encoding = 'utf-8'
_directory = ''


class Structure:
    name = ''


def extract(string):
    match = _pattern.match(string)
    definitions = []
    while match:
        pos = match.end()
        counter = 1
        while counter:
            if string[pos] == '}':
                counter -= 1
            elif string[pos] == '{':
                counter += 1
            pos += 1
        while string[pos] != ';':
            pos += 1
        definitions.append(string[match.start():pos])
        string = string[pos:]
        match = _pattern.match(string)
    return definitions


def lex(definition):
    pass


def parse(lexed_definition):
    structure = Structure()
    return structure


def convert(parsed_definition):
    xml = ''
    return xml


def _process_dir(dir_path):
    # print("Processing directory: " + dir_path)
    for path in os.listdir(dir_path):
        full_path = os.path.join(dir_path, path)
        if os.path.isdir(full_path):
            _process_dir(full_path)
        elif os.path.isfile(full_path):
            _process_file(full_path)


def _process_file(file_path):
    # print("Processing: " + file_path)
    with open('file_name', 'rb') as f:
        context = f.read().decode(_encoding)
    definitions = extract(context)
    lexed = [lex(definition) for definition in definitions]
    parsed = [parse(definition) for definition in lexed]
    for struct in parsed:
        xml_filename = os.path.splitext(os.path.basename(file_path))[0] + struct.name + '.xml'
        output_dirname = os.path.join(os.path.dirname(file_path),
                                      'cstruct2xml-output') if _directory == '' else _directory
        if not os.path.exists(output_dirname):
            os.mkdir(output_dirname)
        output_path = os.path.join(output_dirname, xml_filename)
        with open(output_path, 'wb+') as f:
            f.write(convert(struct).encode("utf-8"))


def main():
    import optparse
    global _encoding
    global _directory
    opt_parser = optparse.OptionParser()
    opt_parser.add_option('-e', '--encoding', dest='encoding',
                          help='Use specific encoding for files. Default is utf-8.', metavar='ENCODING')
    opt_parser.add_option('-d', dest='directory',
                          help='Output XML-file to specific directory.', metavar='DIR')
    options, args = opt_parser.parse_args()
    print(type(options))
    if options.encoding is not None:
        # TODO: Check if given encoding is correct
        _encoding = options.encoding
    if options.directory is not None:
        # TODO: Check if correct path is given and directory exists
        _directory = options.directory
        if not os.path.isdir(_directory):
            exit("Provided directory is not existing directory.")
    print("Using encoding: " + _encoding)
    print("Using output directory: " + _directory)
    print("Converting files: " + str(args))
    for arg in args:
        if os.path.isdir(arg):
            _process_dir(arg)
        elif os.path.isfile(arg):
            _process_file(arg)


if __name__ == '__main__':
    main()
