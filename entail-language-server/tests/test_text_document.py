import sys

sys.path.append('./src')

import textwrap
import unittest

from entail_core.text.text import Position, Range
from text.change import Change
from text.text_document import TextDocument


class TestTextDocumentChange(unittest.TestCase):
    def test_line_into_empty(self):
        txt_doc = TextDocument('')
        change_range = Range(Position(0, 0), Position(0, 0))
        text = 'abc'
        change = Change(text, change_range)
        txt_doc.apply_change(change)
        expected_txt_doc = TextDocument('abc')
        self.assertEqual(txt_doc, expected_txt_doc)

    def test_insert_multiple_lines_into_empty(self):
        txt_doc = TextDocument('')
        change_range = Range(Position(0, 0), Position(0, 0))
        text = textwrap.dedent(
            """\
            abc
            def
            ghi""")
        change = Change(text, change_range)
        txt_doc.apply_change(change)
        expected_txt_doc = TextDocument(textwrap.dedent(
            """\
            abc
            def
            ghi"""
        ))
        self.assertEqual(txt_doc, expected_txt_doc)

    def test_delete_in_one_line(self):
        txt_doc = TextDocument('abcdef')
        change_range = Range(Position(0, 2), Position(0, 4))
        text = ''
        change = Change(text, change_range)
        txt_doc.apply_change(change)
        expected_txt_doc = TextDocument('abef')
        self.assertEqual(txt_doc, expected_txt_doc)

    def test_replace_in_one_line(self):
        txt_doc = TextDocument('abcdef')
        change_range = Range(
            Position(0, 2),
            Position(0, 4)
        )
        text = '123'
        change = Change(text, change_range)
        txt_doc.apply_change(change)
        expected_txt_doc = TextDocument('ab123ef')
        self.assertEqual(txt_doc, expected_txt_doc)

    def test_delete_multiple_lines(self):
        txt_doc = TextDocument(textwrap.dedent(
            """\
            abc  
            def
            ghi"""
        ))
        change_range = Range(Position(0, 2), Position(2, 2))
        text = ''
        change = Change(text, change_range)
        txt_doc.apply_change(change)
        expected_txt_doc = TextDocument('abi')
        self.assertEqual(txt_doc, expected_txt_doc)

    def test_delete_multiple_lines_and_insert_one(self):
        txt_doc = TextDocument(textwrap.dedent(
            """\
            abc  
            def
            ghi"""
        ))
        change_range = Range(
            Position(0, 2),
            Position(2, 2))
        text = '123'
        change = Change(text, change_range)
        txt_doc.apply_change(change)
        expected_txt_doc = TextDocument('ab123i')
        self.assertEqual(txt_doc, expected_txt_doc)

    def test_delete_multiple_lines_and_insert_multiple_lines(self):
        txt_doc = TextDocument(textwrap.dedent(
            """\
            abc  
            def
            ghi"""
        ))
        text = textwrap.dedent("""\
                12
                34
                56""")
        change_range = Range(Position(0, 2), Position(2, 2))
        change = Change(text, change_range)
        txt_doc.apply_change(change)
        expected_txt_doc = TextDocument(textwrap.dedent(
            """\
            ab12
            34
            56i"""
        ))
        self.assertEqual(txt_doc, expected_txt_doc)
