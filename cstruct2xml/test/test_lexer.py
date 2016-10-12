#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from cstruct2xml.lexer import Lexer, LexerError


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
                signed short d[123];
                unsigned char e;
            } StructName;
        """
        lexer = Lexer(testcase)
        lexemes = list(lexer)
        for lexeme in lexemes:
            print(lexeme)
        self.assertEqual(len(lexemes), 32)

    def test_with_error(self):
        testcase = """
            //comment
            typedef struct {
                int a;
                struct {
                    double b;
                } abc;
                ^#$Asd fssd;
            } StructName;
        """
        with self.assertRaises(LexerError):
            lexer = Lexer(testcase)
            lexemes = list(lexer)

    def test_position(self):
        testcase = """
            //comment
            typedef struct {
                int a;
                float b;
                /* some "multiline" comment */
                struct {
                    long double c;
                }
                signed short d[123];
                unsigned char e;
            } StructName;
        """
        lexer = Lexer(testcase)
        iterator = iter(lexer)
        next(iterator)
        next(iterator)
        next(iterator)
        self.assertEqual((lexer.line_number, lexer.line_pos), (3,26))
        next(iterator)
        next(iterator)
        next(iterator)
        self.assertEqual((lexer.line_number, lexer.line_pos), (4,21))
