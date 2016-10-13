#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from cstruct2xml.lexer import Lexer
from cstruct2xml.parser import Parser, ParserError


class TestParser(unittest.TestCase):

    def test_correct_syntax(self):
        testcase = """
            //comment
            typedef struct {
                int a;
                float b;
                /* some "multiline" comment */
                struct {
                    long double c;
                } inner_struct_name;
                signed short d[123];
                unsigned char e;
            } StructName;
        """
        lexer = Lexer(testcase)
        parser = Parser(lexer)
        structure = parser.parse()
        self.assertEqual(structure.name, "StructName")
        self.assertEqual(structure.description, "comment")
        self.assertEqual(len(structure.variables), 5)

    def test_wrong_lexeme_error(self):
        testcase = """
            //comment
            typedef struct {
                int a;
                float b;
                /* some "multiline" comment */
                struct {
                    long struct c;
                } inner_struct_name;
                signed short d[123];
                unsigned char e;
            } StructName;
        """
        lexer = Lexer(testcase)
        parser = Parser(lexer)
        with self.assertRaises(ParserError) as context:
            parser.parse()
        exception = context.exception
        self.assertTrue(exception.message.startswith('Wrong'))

    def test_unexpected_end_of_lexemes(self):
        testcase = """
        //comment
            typedef struct {
                int a;
                float b;
                /* some "multiline" comment */
                struct {
                    long double c;
                } inner_struct_name;
                signed short d[123];
                unsigned char e;
            }
        """
        lexer = Lexer(testcase)
        parser = Parser(lexer)
        with self.assertRaises(ParserError) as context:
            parser.parse();
        exception = context.exception
        self.assertFalse(exception.message.startswith('End of lexemes') or
                            exception.message.startswith('Wrong lexeme'))

    def test_end_expected_but_lexeme_found(self):
        testcase = """
        //comment
            typedef struct {
                int a;
                float b;
                /* some "multiline" comment */
                struct {
                    long double c;
                } inner_struct_name;
                signed short d[123];
                unsigned char e;
            } StructName; int a = 5;

        """
        lexer = Lexer(testcase)
        parser = Parser(lexer)
        with self.assertRaises(ParserError) as context:
            parser.parse()
        exception = context.exception
        self.assertTrue(exception.message.startswith('End of lexemes'))
