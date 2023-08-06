# -*- coding: utf-8 -*-

"""

test.test_main_stdin

Unit test the command line interface
with input from stdin

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import io
import sys

from unittest import TestCase
from unittest.mock import patch

import yaml

import dryjq

from dryjq import __main__
from dryjq import queries

from . import data
from .commons import GenericCallResult


class CommandLineResult(GenericCallResult):

    """Command line call result"""

    @classmethod
    def do_call(cls, *args, **kwargs):
        """Do the real function call"""
        del kwargs
        return __main__.main(list(args))


class TestSimple(TestCase):

    """Simple test module using patched stdin and stdout"""

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_get_single_value(self, mock_stdout):
        """Get a single value"""
        result = CommandLineResult.from_call(
            ".felines.cats.big[1]",
            stdin_data=data.INPUT_YAML_ANIMALS,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_CATS_BIG_1)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_get_subtree(self, mock_stdout):
        """Get a subtree"""
        result = CommandLineResult.from_call(
            ".canines",
            stdin_data=data.INPUT_YAML_ANIMALS,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_YAML_CANINES)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_missing_list_value(self, mock_stdout):
        """Try to get a missing list value"""
        missing_index = 5
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f".felines.cats.big[{missing_index}]",
                stdin_data=data.INPUT_YAML_ANIMALS,
                stdout=mock_stdout,
            )
        #
        self.assertIn(f"Index {missing_index!r} not found", log_cm.output[0])
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_invalid_query(self, mock_stdout):
        """Try to parse a malformed query"""
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                "invalid query",
                stdin_data=data.INPUT_YAML_ANIMALS,
                stdout=mock_stdout,
            )
        #
        self.assertIn(
            "The query must always start with a separator item",
            log_cm.output[0],
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_missing_mapping_value(self, mock_stdout):
        """Try to get a missing mapping value"""
        missing_key = "rodents"
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f".{missing_key}",
                stdin_data=data.INPUT_YAML_ANIMALS,
                stdout=mock_stdout,
            )
        #
        self.assertIn(f"Index {missing_key!r} not found", log_cm.output[0])
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_indexing_scalar_value(self, mock_stdout):
        """Try to get an indexed value from a scalar"""
        wrong_index = 1
        query = ".felines.cats.big[0]"
        query_parser = queries.Parser()
        scalar_value = query_parser.parse_query(query).apply_to(
            yaml.safe_load(data.INPUT_YAML_ANIMALS)
        )
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f"{query}[{wrong_index}]",
                stdin_data=data.INPUT_YAML_ANIMALS,
                stdout=mock_stdout,
            )
        #
        self.assertIn(
            f"Scalar value {scalar_value!r} cannot have an index",
            log_cm.output[0],
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_key_indexing_list(self, mock_stdout):
        """Try to get a value indexed by a key from a list"""
        wrong_index = "lion"
        query = f".felines.cats.big[{wrong_index}]"
        query_parser = queries.Parser()
        last_path_component = query_parser.parse_query(query).components[-1]
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f"{query}",
                stdin_data=data.INPUT_YAML_ANIMALS,
                stdout=mock_stdout,
            )
        #
        self.assertIn(
            f"{last_path_component!r} does not allow lists",
            log_cm.output[0],
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_invalid_yaml(self, mock_stdout):
        """Invalid input data"""
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                ".",
                stdin_data="a: b: c: d:",
                stdout=mock_stdout,
            )
        #
        self.assertIn(
            # FIXME: PyYAML specific error message, might change
            "mapping values are not allowed here",
            log_cm.output[0],
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_modify_stdin(self, mock_stdout):
        """Try to modify stdin in place"""
        assert mock_stdout is sys.stdout
        with self.assertLogs(None, level="WARNING") as log_cm:
            result = CommandLineResult.from_call(
                "--inplace",
                stdin_data=data.INPUT_YAML_ANIMALS,
                stdout=mock_stdout,
            )
        #
        self.assertIn("Cannot modify <stdin> in place", log_cm.output[0])
        self.assertEqual(result.returncode, data.RETURNCODE_OK)
        self.assertEqual(mock_stdout.getvalue(), data.INPUT_YAML_ANIMALS)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_replace_single_value(self, mock_stdout):
        """Replace a single value"""
        result = CommandLineResult.from_call(
            ". = 42",
            stdin_data="Answer to the Ultimate Question of Life,"
            " The Universe, and Everything",
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, "42\n")
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_replace_item(self, mock_stdout):
        """Replace an item"""
        result = CommandLineResult.from_call(
            ".felines.cats.big[2] = panther",
            stdin_data=data.INPUT_YAML_ANIMALS,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_YAML_JAGUAR2PANTHER)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_replace_subtree(self, mock_stdout):
        """Replace a subtree"""
        result = CommandLineResult.from_call(
            f".felines.cats = {data.REPLACEMENT_YAML_CATS_TAXONOMY}",
            stdin_data=data.INPUT_YAML_ANIMALS,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_YAML_CATS_TAXONOMY)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_get_json_value(self, mock_stdout):
        """Get a single value from JSON input"""
        result = CommandLineResult.from_call(
            ".aurora.australis",
            stdin_data=data.INPUT_JSON_AURORA,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_JSON_AURORA_AUSTRALIS)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_convert_json2yaml(self, mock_stdout):
        """Convert JSON to YAML"""
        result = CommandLineResult.from_call(
            "--output-format",
            "YAML",
            stdin_data=data.INPUT_JSON_AURORA,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_CONVERTED_YAML_AURORA)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_convert_yaml2json(self, mock_stdout):
        """Convert YAML to json"""
        result = CommandLineResult.from_call(
            "--output-format",
            "JSON",
            stdin_data=data.INPUT_YAML_ANIMALS,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_CONVERTED_JSON_ANIMALS)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_version(self, mock_stdout):
        """Print version"""
        with self.assertRaises(SystemExit) as sys_exit:
            result = CommandLineResult.from_call(
                "--version",
                stdout=mock_stdout,
            )
            self.assertEqual(result.stdout, f"dryjq {dryjq.__version__}\n")
            self.assertEqual(result.returncode, data.RETURNCODE_OK)
        #
        self.assertEqual(sys_exit.exception.code, data.RETURNCODE_OK)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
