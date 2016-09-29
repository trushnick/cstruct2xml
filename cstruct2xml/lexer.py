#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .tokens import Token, TokenType
import re


class Lexer:

    def __init__(self, input_text):
        self.input_text = input_text
        self.line_number = 0
        self.line_pos = 0
        self.pos = 0

    def _consume(self, token):
        self.line_number += token.value.count('\n')
        self.line_pos = len(token.value.split('\n')[-1])  # TODO: Is it okay?
        self.pos += len(token.value)

    def __iter__(self):
        token = self._next_token()
        while token.type == TokenType.WHITESPACE:
            token = self._next_token()
            self._consume(token)
        self._consume(token)
        yield token

    def _next_token(self):
        matches = []
        for t_type in TokenType:
            match = re.match(t_type.pattern(), self.input_text, self.pos)
            if match:
                token = Token(t_type, match.group(0))
                matches.append( (t_type,match))
        if not matches:
            raise LexerError
        best_match = max(matches, key=len)
        return best_match


class LexerError(Exception):
    pass