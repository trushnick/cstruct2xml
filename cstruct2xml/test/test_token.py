#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import re
from tokens import TokenType


class TestToken(unittest.TestCase):
    
    def test_whitespaces(self):
        pattern = re.compile(TokenType.WHITESPACE.pattern())
        testcases_match = ['  ', '\t', ' \t', ' \t\n', '\r\n']
        testcases_no_match = ['0123', '0x123', 'afd']
        for testcase in testcases_match:
            self.assertNotEqual(pattern.match(testcase), None)
        for testcase in testcases_no_match:
            self.assertEqual(pattern.match(testcase), None)

    def test_endofline_comment(self):
        pattern = re.compile(TokenType.END_OF_LINE_COMMENT.pattern())
        testcases_match = ['// 123 \n', '//12//3\n']
        testcases_no_match = ['// 123', '/*da/', 'dsalk']
        for testcase in testcases_match:
            print(testcase)
            self.assertNotEqual(pattern.match(testcase), None)
        for testcase in testcases_no_match:
            print(testcase)
            self.assertEqual(pattern.match(testcase), None)

    def test_traditional_comment(self):
        pattern = re.compile(TokenType.TRADITIONAL_COMMENT.pattern())
        testcases_match = ['/* 123 */', '/****/', '/**123*321**/']
        testcases_no_match = ['/*/', '/*we1', '/*eda/', '//dfa*/']
        for testcase in testcases_match:
            print(testcase)
            self.assertNotEqual(pattern.match(testcase), None)
        for testcase in testcases_no_match:
            print(testcase)
            self.assertEqual(pattern.match(testcase), None)

    def test_variable_name(self):
        pattern = re.compile(TokenType.VARIABLE_NAME.pattern())
        testcases_match = ['___', 'afgad', '_as123']
        testcases_no_match = ['^FGD', '$dfa', '/fsd']
        for testcase in testcases_match:
            print(testcase)
            self.assertNotEqual(pattern.match(testcase), None)
        for testcase in testcases_no_match:
            print(testcase)
            self.assertEqual(pattern.match(testcase), None)

    def test_number(self):
        pattern = re.compile(TokenType.NUMBER.pattern())
        testcases_match = ['123', '0']
        testcases_no_match = ['0123', '0x123', 'afd']
        for testcase in testcases_match:
            print("Must match: " + testcase)
            self.assertNotEqual(pattern.match(testcase), None)
        for testcase in testcases_no_match:
            print("Must not match: " + testcase)
            self.assertEqual(pattern.match(testcase), None)
