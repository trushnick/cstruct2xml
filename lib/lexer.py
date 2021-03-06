# -*- coding: utf-8 -*-
from .tokens import Token, TokenType
import re


class Lexer:

    def __init__(self, input_text):
        self.input_text = input_text
        self.line_number = 1
        self.line_pos = 0
        self.pos = 0

    def _consume(self, token):
        self.line_number += token.value.count('\n')
        if token.value.count('\n'):
            self.line_pos = len(token.value.split('\n')[-1])
        else:
            self.line_pos += len(token.value)
        self.pos += len(token.value)

    def __iter__(self):
        while not self._done():
            token = self._next_token()
            while token.type == TokenType.WHITESPACE and not self._done():
                token = self._next_token()
            if self._done() and token.type == TokenType.WHITESPACE:  # TODO: Refactor (crutch)
                break
            yield token

    def _next_token(self):
        matches = []
        for t_type in TokenType:
            match = re.match(t_type.pattern(), self.input_text[self.pos:])
            if match:
                token = Token(t_type, match.group(0))
                matches.append(token)
        if not matches:
            raise LexerError(self.line_number, self.line_pos, self.input_text[self.pos:self.pos + 10])
        best_match = max(matches, key=len)
        self._consume(best_match)
        return best_match

    def _done(self):
        return self.pos >= len(self.input_text)


class LexerError(Exception):

    def __init__(self, line_num, line_pos, text):
        message = f'Cannot recognize lexeme at line {line_num} at pos {line_pos}: {text}'
        super(LexerError, self).__init__(message)
