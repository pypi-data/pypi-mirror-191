# -*- coding: utf-8 -*-

"""

test_commons

Unit test the commons module

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

from dryjq import commons


class CharactersPair(TestCase):

    """CharactersPair tests"""

    def test_properties(self):
        """Test properties"""
        pair = commons.CharactersPair("()")
        for tested_property, expected_value in (
            ("first", ord("(")),
            ("last", ord(")")),
            ("open", ord("(")),
            ("close", ord(")")),
            ("source", "()"),
            ("both", (ord("("), ord(")"))),
        ):
            with self.subTest(
                tested_property=tested_property, expected_value=expected_value
            ):
                self.assertEqual(
                    getattr(pair, tested_property),
                    expected_value,
                )
            #
        #

    def test_single_character(self):
        """Test initialization with a single character"""
        pair = commons.CharactersPair("/")
        codepoint = ord("/")
        for tested_property in ("first", "last", "open", "close"):
            with self.subTest(
                tested_property=tested_property, codepoint=codepoint
            ):
                self.assertEqual(
                    getattr(pair, tested_property),
                    codepoint,
                )
            #
        #

    def test_exceptions(self):
        """Test initialization errors"""
        for parameter, expected_exception in (
            ("too long", ValueError),
            ("", IndexError),
        ):
            with self.subTest(parameter=parameter):
                self.assertRaises(
                    expected_exception,
                    commons.CharactersPair,
                    parameter,
                )
            #
        #

    def test_comparisons(self):
        """Test comparisons and hash equality"""
        for source1, source2, equal, hash_equal in (
            ("[]", "()", False, False),
            ("//", "/", True, False),
            ("!", "!", True, True),
        ):
            with self.subTest(source1=source1, source2=source2):
                cp1 = commons.CharactersPair(source1)
                cp2 = commons.CharactersPair(source2)
                if equal:
                    self.assertEqual(cp1, cp2)
                else:
                    self.assertNotEqual(cp1, cp2)
                #
                if hash_equal:
                    self.assertEqual(hash(cp1), hash(cp2))
                else:
                    self.assertNotEqual(hash(cp1), hash(cp2))
                #
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
