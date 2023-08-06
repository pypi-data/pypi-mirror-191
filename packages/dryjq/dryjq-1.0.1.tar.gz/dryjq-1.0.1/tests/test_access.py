# -*- coding: utf-8 -*-

"""

test_access

Unit test the access module

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

from dryjq import access


class PathComponent(TestCase):

    """Path component tests"""

    def test_failed_init(self):
        """Test initialization with wrong index types"""
        for unsuitable_index in ([], tuple(), set(), {}):
            self.assertRaisesRegex(
                TypeError,
                r"\AThe index must be None or a scalar of type int,"
                " float, str or bool.",
                access.PathComponent,
                unsuitable_index,
            )
        #

    def test_string_representation(self):
        """Test all possible string representations"""
        numeric_index = 3
        mapping_key = "any key"
        purpose_maps_only = "for maps only"
        purpose_all = "for maps and lists"
        for index, in_subscript, purpose in (
            (numeric_index, True, purpose_all),
            (mapping_key, True, purpose_maps_only),
            (numeric_index, False, purpose_maps_only),
            (mapping_key, False, purpose_maps_only),
        ):
            component = access.PathComponent(index, in_subscript=in_subscript)
            with self.subTest(
                msg=f"Subtest with {component!r}",
                index=index,
                in_subscript=in_subscript,
            ):
                self.assertEqual(
                    str(component), f"<Index {index!r} ({purpose})>"
                )
            #
        #

    def test_list_support(self):
        """Test if the component supports lists"""
        numeric_index = 3
        mapping_key = "any key"
        for index, in_subscript, expected_list_support in (
            (numeric_index, True, True),
            (mapping_key, True, False),
            (numeric_index, False, False),
            (mapping_key, False, False),
        ):
            component = access.PathComponent(index, in_subscript=in_subscript)
            with self.subTest(
                msg=f"Subtest with {component!r}",
                index=index,
                in_subscript=in_subscript,
            ):
                self.assertEqual(component.allows_lists, expected_list_support)
            #
        #

    def test_failed_access(self):
        """Test all possible access failures"""
        numeric_index = 3
        mapping_key = "any key"
        test_dict = dict(different_key=1)
        test_list = ["dummy1", "dummy2", "dummy3"]
        test_scalar = 123
        for index, in_subscript, structure, exception, message, args in (
            (
                numeric_index,
                True,
                [],
                ValueError,
                "Index %r is not suitable for an empty list",
                (numeric_index,),
            ),
            (
                numeric_index,
                True,
                test_list,
                ValueError,
                "Index %r is not in allowed range (%r..%r)",
                (numeric_index, -numeric_index, numeric_index - 1),
            ),
            (
                numeric_index,
                False,
                test_list,
                TypeError,
                "Index %r is not suitable for lists (%r)",
                (numeric_index, "not in subscript"),
            ),
            (
                mapping_key,
                True,
                test_list,
                TypeError,
                "Index %r is not suitable for lists (%r)",
                (mapping_key, "not a valid list index"),
            ),
            (
                numeric_index,
                True,
                test_scalar,
                TypeError,
                "Index %r is not suitable for %r",
                (numeric_index, test_scalar),
            ),
            (
                mapping_key,
                True,
                test_scalar,
                TypeError,
                "Index %r is not suitable for %r",
                (mapping_key, test_scalar),
            ),
            (
                mapping_key,
                True,
                test_dict,
                ValueError,
                "Index (key) %r not found in %r",
                (mapping_key, list(test_dict)),
            ),
        ):
            component = access.PathComponent(index, in_subscript=in_subscript)
            with self.subTest(
                msg=f"Subtest with {component!r}",
                index=index,
                in_subscript=in_subscript,
                data_structure=structure,
                expected_exception=exception,
                message=message,
                args=args,
            ):
                with self.assertLogs(level="INFO") as cm_log:
                    self.assertRaises(
                        exception,
                        component.get_value,
                        structure,
                    )
                    self.assertEqual(cm_log.records[0].msg, message)
                    self.assertEqual(cm_log.records[0].args, args)
                #
            #
        #

    def test_get_value(self):
        """Test all possible value retrievals"""
        numeric_index_1 = -3
        numeric_index_2 = 1
        mapping_key_1 = "second_key"
        mapping_key_2 = "different_key"
        test_dict = dict(first_key=3, second_key=7, different_key=1)
        test_list = ["dummy1", "dummy2", "dummy3"]
        for index, in_subscript, data_structure, expected_result in (
            (numeric_index_1, True, test_list, "dummy1"),
            (numeric_index_2, True, test_list, "dummy2"),
            (mapping_key_1, True, test_dict, 7),
            (mapping_key_2, False, test_dict, 1),
        ):
            component = access.PathComponent(index, in_subscript=in_subscript)
            with self.subTest(
                msg=f"Subtest with {component!r}",
                index=index,
                in_subscript=in_subscript,
                data_structure=data_structure,
                expected_result=expected_result,
            ):
                self.assertEqual(
                    component.get_value(data_structure), expected_result
                )
            #
        #


class Path(TestCase):

    """Path tests"""

    def test_inequality(self):
        """Test inequality of two paths"""
        path1 = access.Path(
            access.PathComponent(3), access.PathComponent("key")
        )
        path2 = access.Path(
            access.PathComponent("3"), access.PathComponent("key")
        )
        self.assertNotEqual(path1, path2)

    def test_failed_comparison(self):
        """Test for failed comparison of different types"""
        path1 = access.Path(
            access.PathComponent(3), access.PathComponent("key")
        )
        path2 = access.ExtractingPath(
            access.PathComponent("3"), access.PathComponent("key")
        )
        path3 = access.ReplacingPath(
            access.PathComponent("3"), access.PathComponent("key")
        )
        for first, second in (
            (path1, path2),
            (path1, path3),
            (path2, path1),
            (path2, path3),
            (path3, path1),
            (path3, path2),
        ):
            with self.subTest(first=first, second=second):
                self.assertRaises(TypeError, first.__eq__, second)
            #
        #

    def test_apply_to(self):
        """Test not implemented apply_to"""
        path = access.Path(
            access.PathComponent(3), access.PathComponent("key")
        )
        self.assertRaises(NotImplementedError, path.apply_to, None)

    def test_hash(self):
        """Test if hash() returns an integer"""
        path = access.Path(
            access.PathComponent(3), access.PathComponent("key")
        )
        self.assertTrue(isinstance(hash(path), int))

    def test_representation(self):
        """Test all possible representations"""
        for components, representation in (
            (
                (access.PathComponent("key"), access.PathComponent(-3)),
                "Path(PathComponent(index='key', in_subscript=False),"
                " PathComponent(index=-3, in_subscript=False))",
            ),
            (
                (
                    access.PathComponent(0, in_subscript=True),
                    access.PathComponent("key", in_subscript=True),
                ),
                "Path(PathComponent(index=0, in_subscript=True),"
                " PathComponent(index='key', in_subscript=True))",
            ),
        ):
            with self.subTest(
                components=components,
                representation=representation,
            ):
                self.assertEqual(
                    repr(access.Path(*components)), representation
                )
            #
        #

    def test_lengths(self):
        """Test all possible lengths"""
        for components, expected_length in (
            (
                (access.PathComponent("key"), access.PathComponent(-3)),
                2,
            ),
            ((access.PathComponent(0, in_subscript=True),), 1),
            ((), 0),
            (
                (
                    access.PathComponent("key"),
                    access.PathComponent(-3),
                    access.PathComponent(5, in_subscript=True),
                ),
                3,
            ),
        ):
            with self.subTest(
                components=components,
                expected_length=expected_length,
            ):
                self.assertEqual(
                    len(access.Path(*components)), expected_length
                )
            #
        #


class ExtractingPath(TestCase):

    """Extracting Path tests"""

    def test_get_value(self):
        """Test various value retrievals"""
        for components, data_structure, expected_value in (
            (
                (access.PathComponent("key"), access.PathComponent(-3)),
                {"key": {-3: "surprise", "no_surprise": 957}},
                "surprise",
            ),
            (
                (access.PathComponent(0, in_subscript=True),),
                ["abc", "def", "ghi"],
                "abc",
            ),
            ((), "scalar value", "scalar value"),
            ((), 7, 7),
            ((), False, False),
            ((), None, None),
            (
                (
                    access.PathComponent("key"),
                    access.PathComponent(-3),
                    access.PathComponent(5, in_subscript=True),
                ),
                {"key": {-3: [9, 8, 7, 6, 5, 4, 3, 2], "no_surprise": 957}},
                4,
            ),
            (
                (
                    access.PathComponent("key"),
                    access.PathComponent(-3),
                    access.PathComponent(5, in_subscript=True),
                ),
                {
                    "key": {
                        -3: {"surprise": 8, 5: "whatever"},
                        "no_surprise": 957,
                    }
                },
                "whatever",
            ),
        ):
            with self.subTest(
                components=components,
                data_structure=data_structure,
                expected_value=expected_value,
            ):
                current_path = access.ExtractingPath(*components)
                self.assertEqual(
                    current_path.apply_to(data_structure), expected_value
                )
            #
        #


class ReplacingPath(TestCase):

    """Replacing Path tests"""

    def test_hash(self):
        """Test if hash() returns an integer"""
        path = access.ReplacingPath(
            access.PathComponent(3), access.PathComponent("key")
        )
        self.assertTrue(isinstance(hash(path), int))

    def test_representation(self):
        """Test if hash() returns an integer"""
        path = access.ReplacingPath(
            access.PathComponent(3), access.PathComponent("key")
        )
        self.assertEqual(
            repr(path),
            "ReplacingPath(PathComponent(index=3, in_subscript=False),"
            " PathComponent(index='key', in_subscript=False),"
            " replacement=None)",
        )

    def test_replace_value(self):
        """Test various value replacements"""
        replacement_none = None
        replacement_ds = {"new_1": 7, "new_2": 576}
        for components, data_structure, replacement, expected_result in (
            (
                (access.PathComponent("key"), access.PathComponent(-3)),
                {"key": {-3: "surprise", "no_surprise": 957}},
                replacement_ds,
                {"key": {-3: {"new_1": 7, "new_2": 576}, "no_surprise": 957}},
            ),
            (
                (access.PathComponent(0, in_subscript=True),),
                ["abc", "def", "ghi"],
                None,
                [None, "def", "ghi"],
            ),
            ((), "scalar value", replacement_ds, replacement_ds),
            ((), 7, replacement_none, replacement_none),
            (
                (
                    access.PathComponent("key"),
                    access.PathComponent(-3),
                    access.PathComponent(5, in_subscript=True),
                ),
                {"key": {-3: [9, 8, 7, 6, 5, 4, 3, 2], "no_surprise": 957}},
                replacement_none,
                {"key": {-3: [9, 8, 7, 6, 5, None, 3, 2], "no_surprise": 957}},
            ),
            (
                (
                    access.PathComponent("key"),
                    access.PathComponent(-3),
                    access.PathComponent(5, in_subscript=True),
                ),
                {
                    "key": {
                        -3: {"surprise": 8, 5: "whatever"},
                        "no_surprise": 957,
                    }
                },
                replacement_ds,
                {
                    "key": {
                        -3: {"surprise": 8, 5: {"new_1": 7, "new_2": 576}},
                        "no_surprise": 957,
                    }
                },
            ),
        ):
            with self.subTest(
                components=components,
                data_structure=data_structure,
                replacement=replacement,
                expected_result=expected_result,
            ):
                current_path = access.ReplacingPath(
                    *components, replacement=replacement
                )
                self.assertEqual(
                    current_path.apply_to(data_structure),
                    expected_result,
                )
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
