# -*- coding: utf-8 -*-

"""

test_queries

Unit test the queries module

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


from unittest import TestCase

from unittest.mock import patch

from dryjq import commons
from dryjq import queries

from dryjq.access import PathComponent, ExtractingPath, ReplacingPath


class Itemizer(TestCase):

    """Itemizer class test"""

    def setUp(self):
        """Initialize the itemizer"""
        self.itemizer = queries.Itemizer()

    def test_queries(self):
        """Test queries"""
        for query, expected_items in (
            (
                "",
                [
                    queries.DelimiterItem(end=False),
                    queries.DelimiterItem(end=True),
                ],
            ),
            (
                ".",
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("."),
                    queries.DelimiterItem(end=True),
                ],
            ),
            (
                " .",
                [
                    queries.DelimiterItem(end=False),
                    queries.WhitespaceItem(" "),
                    queries.SeparatorItem("."),
                    queries.DelimiterItem(end=True),
                ],
            ),
            (
                ".abc",
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("."),
                    queries.LiteralItem("abc"),
                    queries.DelimiterItem(end=True),
                ],
            ),
            (
                ".abc['yes'].xyz = [1, 2, 4]",
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("."),
                    queries.LiteralItem("abc"),
                    queries.SubscriptOpenerItem("["),
                    queries.LiteralItem("'yes'"),
                    queries.SubscriptCloserItem("]"),
                    queries.SeparatorItem("."),
                    queries.LiteralItem("xyz"),
                    queries.WhitespaceItem(" "),
                    queries.AssignmentItem("="),
                    queries.WhitespaceItem(" "),
                    queries.SubscriptOpenerItem("["),
                    queries.LiteralItem("1,"),
                    queries.WhitespaceItem(" "),
                    queries.LiteralItem("2,"),
                    queries.WhitespaceItem(" "),
                    queries.LiteralItem("4"),
                    queries.SubscriptCloserItem("]"),
                    queries.DelimiterItem(end=True),
                ],
            ),
        ):
            with self.subTest(query=query):
                self.assertEqual(
                    list(self.itemizer.itemize(query)),
                    expected_items,
                )
            #
        #

    def test_specialchars_variations(self):
        """Test variations of separator and subscript (...)
        ... indicator characters in queries
        """
        for query, separator, subscript_pair, expected_items in (
            (
                "/",
                "/",
                "[]",
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("/"),
                    queries.DelimiterItem(end=True),
                ],
            ),
            (
                "?abc",
                "?",
                "<>",
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("?"),
                    queries.LiteralItem("abc"),
                    queries.DelimiterItem(end=True),
                ],
            ),
            (
                "!abc('yes')!xyz = [1, 2, 4]",
                "!",
                "()",
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("!"),
                    queries.LiteralItem("abc"),
                    queries.SubscriptOpenerItem("("),
                    queries.LiteralItem("'yes'"),
                    queries.SubscriptCloserItem(")"),
                    queries.SeparatorItem("!"),
                    queries.LiteralItem("xyz"),
                    queries.WhitespaceItem(" "),
                    queries.AssignmentItem("="),
                    queries.WhitespaceItem(" "),
                    queries.LiteralItem("[1,"),
                    queries.WhitespaceItem(" "),
                    queries.LiteralItem("2,"),
                    queries.WhitespaceItem(" "),
                    queries.LiteralItem("4]"),
                    queries.DelimiterItem(end=True),
                ],
            ),
        ):
            with self.subTest(query=query):
                itemizer = queries.Itemizer(
                    separator_codepoint=ord(separator),
                    subscript_indicators_pair=commons.CharactersPair(
                        subscript_pair
                    ),
                )
                self.assertEqual(
                    list(itemizer.itemize(query)),
                    expected_items,
                )
            #
        #

    def test_errors(self):
        """Test itemizer errors"""
        for query, expected_exception, position in (
            (".abc[null", queries.UnclosedSubscriptError, 5),
            (".abc['def", queries.UnclosedQuoteError, 6),
        ):
            with self.subTest(query=query):
                self.assertRaisesRegex(
                    expected_exception,
                    f".* character position #{position}",
                    list,
                    self.itemizer.itemize(query),
                )
            #

    def test_warning(self):
        """Test the warning about subscript opener in subscript"""

        with self.assertLogs(None, level="WARNING") as log_cm:
            result = list(self.itemizer.itemize(".abc[def[ghi]jkl]"))
        #
        self.assertIn(
            "Possible error: Found subscript opener",
            log_cm.output[0],
        )
        self.assertEqual(
            result,
            [
                queries.DelimiterItem(end=False),
                queries.SeparatorItem("."),
                queries.LiteralItem("abc"),
                queries.SubscriptOpenerItem("["),
                queries.LiteralItem("def[ghi"),
                queries.SubscriptCloserItem("]"),
                queries.LiteralItem("jkl]"),
                queries.DelimiterItem(end=True),
            ],
        )

    def test_init_errors(self):
        """Test initialization errors"""
        for separator, subscript_pair, expected_exception_regex in (
            ("=", "[]", r"\ASeparator codepoint \d+ \('='\) not allowed"),
            (
                ".",
                "'",
                r"""\ASubscript indicator codepoint \d+ \("'"\) not allowed""",
            ),
            ("/", r"\/", r"\ASeparator codepoint \d+ \('/'\) not allowed"),
        ):
            with self.subTest(
                separator=separator,
                subscript_pair=subscript_pair,
            ):
                self.assertRaisesRegex(
                    ValueError,
                    expected_exception_regex,
                    queries.Itemizer,
                    separator_codepoint=ord(separator),
                    subscript_indicators_pair=commons.CharactersPair(
                        subscript_pair
                    ),
                )
            #
        #


class Parser(TestCase):

    """Test the Parser class"""

    def test_error_empty_query(self):
        """Test IllegalState error being raised"""
        parser = queries.Parser()
        self.assertRaisesRegex(
            queries.IllegalStateError,
            "The query must always start with a separator item!",
            parser.parse_query,
            "",
        )

    def test_working_queries(self):
        """Test working queries"""
        parser = queries.Parser()
        for query, expected_path, warning in (
            (
                ".",
                ExtractingPath(),
                None,
            ),
            (
                " .",
                ExtractingPath(),
                None,
            ),
            (
                ".abc",
                ExtractingPath(PathComponent(index="abc", in_subscript=False)),
                None,
            ),
            (
                ".abc[ d e f g h ]",
                ExtractingPath(
                    PathComponent(index="abc", in_subscript=False),
                    PathComponent(index="defgh", in_subscript=True),
                ),
                None,
            ),
            (
                ".abc[def[ghi]jkl]",
                ExtractingPath(
                    PathComponent(index="abc", in_subscript=False),
                    PathComponent(index="def[ghi", in_subscript=True),
                    PathComponent(index="jkl]", in_subscript=False),
                ),
                "Possible error: Found subscript",
            ),
            (
                ".abc['yes'].xyz = [1, 2, 4]",
                ReplacingPath(
                    PathComponent(index="abc", in_subscript=False),
                    PathComponent(index="yes", in_subscript=True),
                    PathComponent(index="xyz", in_subscript=False),
                    replacement=[1, 2, 4],
                ),
                None,
            ),
            (
                ".abc['yes'].xyz = ",
                ReplacingPath(
                    PathComponent(index="abc", in_subscript=False),
                    PathComponent(index="yes", in_subscript=True),
                    PathComponent(index="xyz", in_subscript=False),
                    replacement=None,
                ),
                "Assuming empty assignment value",
            ),
        ):
            with self.subTest(query=query):
                if warning:
                    with self.assertLogs(None, level="WARNING") as log_cm:
                        self.assertEqual(
                            parser.parse_query(query),
                            expected_path,
                        )
                    self.assertIn(warning, log_cm.output[0])
                else:
                    self.assertEqual(
                        parser.parse_query(query),
                        expected_path,
                    )
                #
            #
        #

    def test_separator_variations(self):
        """Test working queries"""
        parser = queries.Parser()
        for query, expected_path, separator in (
            (
                "/",
                ExtractingPath(),
                "/",
            ),
            (
                " ~",
                ExtractingPath(),
                "~",
            ),
            (
                "§abc",
                ExtractingPath(PathComponent(index="abc", in_subscript=False)),
                "§",
            ),
            (
                "|abc | d e f g h ",
                ExtractingPath(
                    PathComponent(index="abc", in_subscript=False),
                    PathComponent(index="defgh", in_subscript=False),
                ),
                "|",
            ),
            (
                ":abc['yes']:xyz = [1, 2, 4]",
                ReplacingPath(
                    PathComponent(index="abc", in_subscript=False),
                    PathComponent(index="yes", in_subscript=True),
                    PathComponent(index="xyz", in_subscript=False),
                    replacement=[1, 2, 4],
                ),
                ":",
            ),
        ):
            with self.subTest(query=query, separator=separator):
                self.assertEqual(
                    parser.parse_query(
                        query, separator_codepoint=ord(separator)
                    ),
                    expected_path,
                )
            #
        #

    def test_illegal_states(self):
        """Test illegal states"""
        for mock_items, expected_error_regex in (
            (
                # before start
                [queries.LiteralItem("x")],
                "(?s)Parser phase: 'before start'.+"
                r"Expected DelimiterItem\(end=False\)",
            ),
            (
                # started
                [
                    queries.DelimiterItem(end=False),
                    queries.LiteralItem("x"),
                ],
                "(?s)Parser phase: 'started'.+"
                "The query must always start with a separator item",
            ),
            (
                # address
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("."),
                    queries.LiteralItem("x"),
                    queries.DelimiterItem(end=False),
                ],
                "(?s)Parser phase: 'address'.+"
                r"DelimiterItem\(end=False\) not allowed here",
            ),
            (
                # replacement
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("."),
                    queries.LiteralItem("x"),
                    queries.AssignmentItem("="),
                    queries.DelimiterItem(end=False),
                ],
                "(?s)Parser phase: 'replacement'.+"
                r"DelimiterItem\(end=False\) not allowed here",
            ),
            (
                # ended
                [
                    queries.DelimiterItem(end=False),
                    queries.SeparatorItem("."),
                    queries.LiteralItem("x"),
                    queries.AssignmentItem("="),
                    queries.DelimiterItem(end=True),
                    queries.WhitespaceItem(" "),
                ],
                "(?s)Parser phase: 'ended'.+No items allowed anymore",
            ),
        ):
            with self.subTest(expected_error_regex=expected_error_regex):
                with patch.object(
                    queries.Itemizer, "itemize", return_value=mock_items
                ):
                    parser = queries.Parser()
                    self.assertRaisesRegex(
                        queries.IllegalStateError,
                        expected_error_regex,
                        parser.parse_query,
                        "…",
                    )
                #
            #
        #

    @patch.object(queries.Parser, "phase", new="not implemented")
    def test_phase_not_implemented(self):
        """Test illegal states"""
        parser = queries.Parser()
        self.assertRaisesRegex(
            queries.IllegalStateError,
            "(?s)Parser phase: 'not implemented'.+"
            "Item handler for this phase not implemented",
            parser.parse_query,
            "…",
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
