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


class Variable:

    def __init__(self, structure=None):
        if structure:
            self.description = structure.description
            self.type = 'struct'
            self.value = structure
            self.array_size = 1
        else:
            self.description = None
            self.type = None
            self.value = None
            self.array_size = None


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current = next(lexer)
        self.structure = Structure()
        self.current_var = None

    def parse(self):
        return self._structure_definition()

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
        # structure_body -> structure_body inner_structure_definition |
        #                   structure_body variable_declaration |
        #                   inner_structure_definition |
        #                   variable_declaration
        # TODO: How to handle this left recursion? Make method 'inner_struct_or_var_decl'?
        pass

    def _inner_structure_definition(self):
        # inner_structure_definition -> comment_block STRUCT RCB structure_body RCB structure_name SC
        self.current_var = Variable()
        self.current_var.type = 'struct'
        self.current_var.array_size = 1
        inner_structure = Structure()
        self.current_var.description = inner_structure.description = self._comment_block()
        self._match(TokenType.STRUCT)
        self._match(TokenType.STRUCT)
        self._match(TokenType.LCB)
        self._structure_body(inner_structure)
        self._match(TokenType.RCB)
        self.current_var.name = inner_structure.name = self._structure_name()
        self._match(TokenType.SC)
        return inner_structure

    def _variable_declaration(self):
        # variable_declaration -> comment_block variable_specification
        self.current_var = Variable()
        self.current_var.description = self._comment_block()
        pass

    def _variable_specification(self):
        # variable_specification -> variable_type VARIABLE_NAME SC |
        #                           variable_type VARIABLE_NAME array_specifier SC
        pass

    def _variable_type(self):
        pass

    def _primitive_type(self):
        pass

    def _users_type(self):
        # users_type -> VARIABLE_NAME
        t = self._match(TokenType.VARIABLE_NAME)
        return t.value

    def _array_specifier(self):
        pass

    def _array_size(self):
        # array_size -> NUMBER |
        #               VARIABLE_NAME |
        #               array_size_expression
        if self.current.type == TokenType.NUMBER:
            t = self._match(TokenType.NUMBER)
            return int(t.value)
        elif self.current.type == TokenType.VARIABLE_NAME:
            t = self._match(TokenType.VARIABLE_NAME)
            return t.value
        else:
            return self._array_size_expression()

    def _array_size_expression(self):
        pass

    def _array_size_expression2(self):
        pass

    def _array_size_expression3(self):
        pass

    def _structure_name(self):
        # structure_name -> VARIABLE_NAME
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