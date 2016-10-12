#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from enum import Enum


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __len__(self):
        return len(self.value)


class TokenType(Enum):

    WHITESPACE = r'\s+'

    END_OF_LINE_COMMENT = r'//[^\n]*\n'
    TRADITIONAL_COMMENT = r'/\*([^\*]|\*[^/])*\*/'

    TYPEDEF = r'typedef'
    STRUCT = r'struct'
    CHAR = r'char'
    INT = r'int'
    FLOAT = r'float'
    DOUBLE = r'double'
    SIGNED = r'signed'
    UNSIGNED = r'unsigned'
    LONG = r'long'
    SHORT = r'short'

    VARIABLE_NAME = r'\w+'
    NUMBER = r'[1-9][0-9]*'
    LCB = r'\{'
    RCB = r'\}'
    LSB = r'\['
    RSB = r'\]'
    SC = r';'

    def pattern(self):
        return self.value
