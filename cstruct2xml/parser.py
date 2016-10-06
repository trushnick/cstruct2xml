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
        self.structure = Structure()

    def parse(self):
        pass

    def _structure_definition(self):
        # structure_definition -> comment_block TYPEDEF STRUCT LCB struct_body RCB structure_name SC
        self.structure.description = self._comment_block()
        self._match(TokenType.TYPEDEF)
        self._match(TokenType.STRUCT)
        self._match(TokenType.LCB)
        self._structure_body(self.structure)
        self._match(TokenType.RCB)
        self.structure.name = self._structure_name()
        self._match(TokenType.SC)
        return self.structure

    def _comment_block(self):
        # comment_block -> comment_block comment | comment
        comment_block = ''
        while self.current.type in [TokenType.END_OF_LINE_COMMENT, TokenType.TRADITIONAL_COMMENT]:
            comment = self.current.type[2:]
            if self.current.type == TokenType.TRADITIONAL_COMMENT:
                comment = comment[:-2]
                comment = '\n'.join(line.strip() for line in comment.split('\n'))
            else:
                comment = comment.strip()
            comment_block += '\n' + comment
            self.current = next(self.lexer)
        return comment_block.strip()

    def _structure_body(self, structure):
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
        t = self._match(TokenType.VARIABLE_NAME)
        return t.value

    def _match(self, types):
        if self.current.type in types:
            token = self.current
            self.current = next(self.lexer)
            return token
        else:
            raise ParserError


class ParserError(Exception):

    def __init__(self, token):
        message = 'Wrong lexeme: {} at line {}, pos {}'.format(token, self.lexer.line_number, self.lexer.line_pos)
        super(ParserError, self).__init__(message)