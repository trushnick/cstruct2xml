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

    def parse(self):
        pass