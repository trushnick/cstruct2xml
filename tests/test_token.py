#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import re
from lib.tokens import TokenType


def test_whitespaces():
    pattern = re.compile(TokenType.WHITESPACE.pattern())
    testcases_match = ['  ', '\t', ' \t', ' \t\n', '\r\n']
    testcases_no_match = ['0123', '0x123', 'afd']
    for testcase in testcases_match:
        assert pattern.match(testcase) is not None
    for testcase in testcases_no_match:
        assert pattern.match(testcase) is None

def test_endofline_comment():
    pattern = re.compile(TokenType.END_OF_LINE_COMMENT.pattern())
    testcases_match = ['// 123 \n', '//12//3\n']
    testcases_no_match = ['// 123', '/*da/', 'dsalk']
    for testcase in testcases_match:
        assert pattern.match(testcase) is not None
    for testcase in testcases_no_match:
        assert pattern.match(testcase) is None

def test_traditional_comment():
    pattern = re.compile(TokenType.TRADITIONAL_COMMENT.pattern())
    testcases_match = ['/* 123 */', '/****/', '/**123*321**/', '/**a///*/']
    testcases_no_match = ['/*/', '/*we1', '/*eda/', '//dfa*/']
    for testcase in testcases_match:
        assert pattern.match(testcase) is not None
    for testcase in testcases_no_match:
        assert pattern.match(testcase) is None

def test_variable_name():
    pattern = re.compile(TokenType.VARIABLE_NAME.pattern())
    testcases_match = ['___', 'afgad', '_as123']
    testcases_no_match = ['^FGD', '$dfa', '/fsd']
    for testcase in testcases_match:
        assert pattern.match(testcase) is not None
    for testcase in testcases_no_match:
        assert pattern.match(testcase) is None

def test_number():
    pattern = re.compile(TokenType.NUMBER.pattern())
    testcases_match = ['123', '345632']
    testcases_no_match = ['0123', '0x123', 'afd', '0']
    for testcase in testcases_match:
        assert pattern.match(testcase) is not None
    for testcase in testcases_no_match:
        assert pattern.match(testcase) is None
