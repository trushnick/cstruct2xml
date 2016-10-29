#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from cstruct2xml.resolver import resolve
import lxml.etree as et
from io import StringIO


class TestResolver(unittest.TestCase):

    def test_arraysize_resolving(self):
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
        resolved_xml = resolve(xml, defines)
        resolved_tree = et.parse(StringIO(resolved_xml))
        foo, bar = list(resolved_tree.iterfind('structure/variables/'))
        self.assertEqual(foo.find('array_size').text, str(2))
        self.assertEqual(bar.find('array_size').text, str(3))


    def test_type_resolving(self):
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
        resolved_xml = resolve(xml, {})
        resolved_tree = et.parse(StringIO(resolved_xml))
        test = resolved_tree.xpath("structure[./name/text()='Test']")[0]
        resolved_structure = test.find('variables/structure')
        self.assertEqual(resolved_structure.find('name').text, 'Bar')
        self.assertEqual(resolved_structure.find('description').text, 'Bar var description')
        self.assertEqual(resolved_structure.find('array_size').text, '4')
        self.assertEqual(len(list(resolved_structure.iterfind('variables/'))), 2)
