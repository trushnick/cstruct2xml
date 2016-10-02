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
        self.line_pos = len(token.value.split('\n')[-1])
        self.pos += len(token.value)

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
                token = Token(t_type, match.group(0))
                matches.append(token)
        if not matches:
            raise LexerError(self.line_number, self.line_pos, self.input_text[self.pos:self.pos + 10])
        best_match = max(matches, key=len)
        self._consume(best_match)
        return best_match


class LexerError(Exception):

    def __init__(self, line_num, line_pos, text):
        message = 'Cannot recognize lexeme at line {0} at pos {1}: {2}'.format(line_num, line_pos, text)
        super(LexerError, self).__init__(message)
