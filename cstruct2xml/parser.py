#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .tokens import Token, TokenType
from .lexer import Lexer


class Structure:

    def __init__(self):
        self.name = ''
        self.description = ''
        self.variables = []

    def add_variable(self, variable):
        self.variables.append(variable)


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current = next(lexer)

    def parse(self):
        pass

    def _structure_definition(self):
        pass

    def _comment_block(self):
        pass

    def _comment(self):
        pass

    def _structure_body(self):
        pass

    def _inner_structure_definition(self):
        pass

    def _variable_declaration(self):
        pass

    def _variable_specification(self):
        pass

    def _variable_type(self):
        pass

    def _primitive_type(self):
        pass

    def _users_type(self):
        pass

    def _array_specifier(self):
        pass

    def _array_size(self):
        pass

    def _array_size_expression(self):
        pass

    def _array_size_expression2(self):
        pass

    def _array_size_expression3(self):
        pass

    def _structure_name(self):
        pass

    def _check_token(self, token_type):
        if self.current.type == token_type:
            return True
        else:
            raise ParserError


class ParserError(Exception):

    def __init__(self, token):
        message = 'Wrong lexeme: {} at line {}, pos {}'.format(token, self.lexer.line_number, self.lexer.line_pos)
        super(ParserError, self).__init__(message)