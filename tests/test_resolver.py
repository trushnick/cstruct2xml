#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from lib.resolver import resolve
import lxml.etree as et
from io import StringIO


def test_arraysize_resolving():
    xml = """
    <file>
        <structure>
            <name>FooStruct</name>
            <description/>
            <variables>
                <variable>
                    <name>Foo</name>
                    <type>FooType</type>
                    <description/>
                    <array_size>FOO_ARRAY_SIZE</array_size>
                </variable>
                <variable>
                    <name>Bar</name>
                    <type>BarType</type>
                    <description/>
                    <array_size>BAR_ARRAY_SIZE</array_size>
                </variable>
            </variables>
        </structure>
    </file>
    """
    defines = {
        'FOO_ARRAY_SIZE': 2,
        'BAR_ARRAY_SIZE': 3
    }
    xml_t = et.parse(StringIO(xml))
    resolved_xml = resolve(xml_t, defines)
    # resolved_tree = et.parse(StringIO(resolved_xml))
    foo, bar = list(resolved_xml.iterfind('structure/variables/'))
    assert foo.find('array_size').text == str(2)
    assert bar.find('array_size').text == str(3)


def test_type_resolving():
    xml = """
    <file>
        <structure>
            <name>FooStruct</name>
            <description/>
            <variables>
                <variable>
                    <name>Foo</name>
                    <type>FooType</type>
                    <description/>
                    <array_size>FOO_ARRAY_SIZE</array_size>
                </variable>
                <variable>
                    <name>Bar</name>
                    <type>BarType</type>
                    <description/>
                    <array_size>BAR_ARRAY_SIZE</array_size>
                </variable>
            </variables>
        </structure>
        <structure>
            <name>Test</name>
            <description/>
            <variables>
                <variable>
                    <name>Foo</name>
                    <type>FooType</type>
                    <description/>
                    <array_size>1</array_size>
                </variable>
                <variable>
                    <name>Bar</name>
                    <type>FooStruct</type>
                    <description>Bar var description</description>
                    <array_size>4</array_size>
                </variable>
            </variables>
        </structure>
    </file>
    """
    xml_t = et.parse(StringIO(xml))
    resolved_xml = resolve(xml_t, {})
    # resolved_tree = et.parse(StringIO(resolved_xml))
    test = resolved_xml.xpath("structure[./name/text()='Test']")[0]
    resolved_structure = test.find('variables/structure')
    assert resolved_structure.find('name').text == 'Bar'
    assert resolved_structure.find('description').text == 'Bar var description'
    assert resolved_structure.find('array_size').text == '4'
    assert len(list(resolved_structure.iterfind('variables/'))) == 2
