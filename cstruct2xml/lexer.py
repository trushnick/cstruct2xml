#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .tokens import Token, TokenType
import re


class Lexer:

    def __init__(self, input_text):
        self.input_text = input_text
        self.line = 0
        self.symbol = 0
        self.pos = 0

    def  _consume(self, token):
        self.line += token.value.count('\n')

    def __iter__(self):
        token = self._next_token()
        while token.type == TokenType.WHITESPACE:
            token = self._next_token()
        yield token

    def _next_token(self):
        matches = []
        for t_type in TokenType:
            match = re.match(t_type.pattern(), self.input_text, self.pos)
            if match:
                matches.append( (t_type,match))
        if not matches:
            raise LexerError
        t_type, t_value = max(matches, key=len(lambda x : x[1].group(0)))
        return Token(t_type, t_value)


class LexerError(Exception):
    pass