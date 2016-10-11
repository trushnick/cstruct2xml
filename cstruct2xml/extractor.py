#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os


class Extractor:

    def __init__(self, path, encoding='utf-8'):
        self._pattern = re.compile(r'(?:(?:(?://[^\n]*\n)|(?:/\*(?:[^*]|(?:\*[^/]))*\*/))\s*)*'
                                   r'typedef\s+struct\s+(?:[\w_][\w\d_]*)?\s*\{')
        self.path = path
        self.encoding = encoding
        self.pos = 0
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                self.content = f.read().decode(self.encoding)
        else:
            raise ExtractorError

    def __iter__(self):
        definition = self._next_def()
        while definition:
            yield definition
            definition = self._next_def()

    def _next_def(self):
        match = self._pattern.match(self.content, self.pos)
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


class ExtractorError(Exception):
    pass
