#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os


class Extractor:

    # Header of structure definition
    _header_pattern = re.compile(r'(?:(?:(?://[^\n]*\n)|(?:/\*(?:[^*]|(?:\*+[^/]))*\*+/))\s*)*'
                               r'(?:typedef)?\s+struct\s+(?:\w+)?\s*\{')
    # Regex for #define
    _define_pattern = re.compile(r'#define\s+(?P<token>\w+)\s+(?P<value>\w+)')

    def __init__(self, path, encoding='utf-8'):
        self.path = path
        self.encoding = encoding
        self.pos = 0
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                self.content = f.read().decode(self.encoding)
        else:
            raise ExtractorError("No such file")

    def __iter__(self):
        definition = self._next_def()
        while definition:
            yield definition
            definition = self._next_def()

    def _next_def(self):
        match = self._header_pattern.search(self.content, self.pos)
        if match:
            pos = match.end()
            counter = 1
            while counter:
                if self.content[pos] == '}':
                    counter -= 1
                elif self.content[pos] == '{':
                    counter += 1
                pos += 1
            while self.content[pos] != ';':
                pos += 1
            self.pos = pos + 1
            return self.content[match.start():pos + 1]
        else:
            return None

    def defines(self):
        pos = 0
        define_dict = {}
        match = self._define_pattern.search(self.content, pos)
        while match:
            define_dict[match.group('token')] = match.group('value')
            pos = match.end()
            match = self._define_pattern.search(self.content, pos)
        return define_dict


class ExtractorError(Exception):

    def __init__(self, msg):
        super(ExtractorError, self).__init__(msg)
