#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from nose.tools import raises
from lib.extractor import Extractor, ExtractorError


def test_with_inner_struct():
    testcase = os.path.join(os.path.dirname(__file__),
                            'testcases',
                            'extractor',
                            'test_extractor_inner_struct.h')
    defs = [definition for definition in Extractor(testcase)]
    with open(testcase, 'rb') as f:
        content = [s.strip() for s in
                   f.read().decode('utf-8').split('=' * 20)]
    assert defs == content


def test_simple():
    testcase = os.path.join(os.path.dirname(__file__),
                            'testcases',
                            'extractor',
                            'test_extractor_simple.h')
    defs = list(iter(Extractor(testcase)))
    with open(testcase) as f:
        content = f.read().strip()
    assert len(defs) == 1
    assert defs[0] == content


@raises(ExtractorError)
def test_no_such_file():
    testcase = os.path.join(os.path.dirname(__file__),
                            'testcases',
                            'extractor',
                            'no_such_file.h')
    Extractor(testcase)


def test_multiple_definitions():
    testcase = os.path.join(os.path.dirname(__file__),
                            'testcases',
                            'extractor',
                            'test_extractor_multiple_definitions.h')
    defs = list(Extractor(testcase))
    print(defs)
    with open(testcase, 'rb') as f:
        content = [s.strip() for s in f.read().decode('utf-8').split('=' * 20)]
    assert defs == content
