#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
from cstruct2xml.extractor import Extractor, ExtractorError


class TestExtractor(unittest.TestCase):
    
    def test_with_inner_struct(self):
        testcase = os.path.join(os.path.dirname(__file__), 
                                'testcases',
                                'extractor',
                                'test_extractor_inner_struct.h')
        defs = [definition for definition in Extractor(testcase)]
        with open(testcase, 'rb') as f:
            content = [s.strip() for s in 
                            f.read().decode('utf-8').split('=' * 20)]
        self.assertEqual(defs, content)

    def test_simple(self):
        testcase = os.path.join(os.path.dirname(__file__),
                                'testcases',
                                'extractor',
                                'test_extractor_simple.h')
        defs = list(iter(Extractor(testcase)))
        with open(testcase) as f:
            content = f.read().strip()
        self.assertEqual(len(defs), 1)
        self.assertEqual(defs[0], content)

    def test_no_such_file(self):
        testcase = os.path.join(os.path.dirname(__file__),
                                'testcases',
                                'extractor',
                                'no_such_file.h')
        with self.assertRaises(ExtractorError):
            Extractor(testcase)

    def test_multiple_definitions(self):
        testcase = os.path.join(os.path.dirname(__file__),
                                'testcases',
                                'extractor',
                                'test_extractor_multiple_definitions.h')
        defs = list(Extractor(testcase))
        print(defs)
        with open(testcase, 'rb') as f:
            content = [s.strip() for s in f.read().decode('utf-8').split('=' * 20)]
        self.assertEqual(defs, content)