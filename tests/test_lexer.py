#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import raises
from lib.lexer import Lexer, LexerError


def test_all_tokens():
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
            unsigned char e[123 * (2 - 4) + 3 / 4 - a];
        } StructName ;"""
    lexer = Lexer(testcase)
    lexemes = list(lexer)
    for lexeme in lexemes:
        print(lexeme)
    assert len(lexemes) == 47


@raises(LexerError)
def test_with_error():
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
    lexer = Lexer(testcase)
    list(lexer)


def test_position():
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
    line = lexer.line_number
    pos = lexer.line_pos
    assert (line, pos) == (3, 22)
    next(iterator)
    next(iterator)
    next(iterator)
    line = lexer.line_number
    pos = lexer.line_pos
    assert (line, pos) == (4, 17)
    next(iterator)
    next(iterator)
    line = lexer.line_number
    pos = lexer.line_pos
    assert (line, pos) == (5, 17)
