#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os

from extractor import Extractor, ExtractorError


class TestExtractor(unittest.TestCase):
    
    def test_with_inner_struct(self):
        testcase = os.path.join(os.path.dirname(__file__), 
					'testcases', 
					'extractor',
					'test_extractor_inner_struct.h')
        defs = [definition for definition in Extractor(testcase)]
        with open(testcase) as f:
            content = f.read().split('=' * 20)
        self.assertEqual(defs, content)

    def test_simple(self):
        self.assertTrue(True)

    def test_no_such_file(self):
        with self.assertRaises(ExtractorError):
            raise ExtractorError


if __name__ == '__main__':
    unittest.main()
