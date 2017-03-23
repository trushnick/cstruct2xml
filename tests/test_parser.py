#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.lexer import Lexer
from lib.parser import Parser, ParserError


def test_correct_syntax():
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
    assert structure.name == "StructName"
    assert structure.description == "comment"
    assert len(structure.variables) == 5


def test_wrong_lexeme_error():
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
    try:
        parser.parse()
    except ParserError as err:
        assert err.message.startswith('Wrong')
    else:
        assert False


def test_unexpected_end_of_lexemes():
    testcase = """
    //comment
        typedef struct {
            int a;
            float b;
            /* some "multiline" comment */
            struct {
                long double c;
            } inner_struct_name[5];
            signed short d[123];
            unsigned char e;
        }
    """
    lexer = Lexer(testcase)
    parser = Parser(lexer)
    try:
        parser.parse()
    except ParserError as err:
        assert err.message.endswith('end of lexemes found')
    else:
        assert False


def test_end_expected_but_lexeme_found():
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
    try:
        parser.parse()
    except ParserError as err:
        assert err.message.startswith('End of lexemes')
    else:
        assert False


def test_comment_before_bracket():
    testcase = """
    //comment
    typedef struct // comment before opening bracket
    {
        int a;
        unsigned long long int b;
    /* comment
        before
        closing bracket */
    } StructName;
    """
    lexer = Lexer(testcase)
    parser = Parser(lexer)
    structure = parser.parse()
    assert structure is not None


def test_multiple_names():
    testcase = """
    //comment
    typedef struct StructName {
        int foo;
        float bar[MAX_SIZE];
    } StructNameAlias;
    """
    lexer = Lexer(testcase)
    parser = Parser(lexer)
    structure = parser.parse()
    assert structure.name == 'StructNameAlias'


def test_without_typedef():
    testcase = """
    //comment
    struct FirstName {
        int foo;
        float bar[1];
    } NameAlias;
    """
    lexer = Lexer(testcase)
    parser = Parser(lexer)
    structure = parser.parse()
    assert structure is not None
