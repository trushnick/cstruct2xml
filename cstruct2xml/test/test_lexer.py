#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
from cstruct2xml.lexer import Lexer, LexerError
#from lexer import Lexer, LexerError


class TestLexer(unittest.TestCase):
    
    def test_all_tokens(self):
        testcase = """
        //comment
        typedef struct {
            int a;
            float b;
            /* some "multiline" comment */
            struct {
                long double c;
            }
            signed short d;
            unsigned char e;   
        } StructName;
        """
        lexer = Lexer(testcase)
        lexemes = list(lexer)
        print( len(lexemes))
        self.assertEqual(len(lexemes), 29)


    def test_with_error(self):
        pass
