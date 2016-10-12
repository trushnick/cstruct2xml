#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from cstruct2xml.lexer import Lexer, LexerError


class TestLexer(unittest.TestCase):
    
    def test_all_tokens(self):
        testcase = \
"""//comment
typedef struct {
    int a;
    float b;
    /* some "multiline" comment */
    struct {
        long double c;
    }
    signed short d;
    unsigned char e;
} StructName;"""
        lexer = Lexer(testcase)
        lexemes = list(lexer)
        self.assertEqual(len(lexemes), 28)

    def test_with_error(self):
        pass
