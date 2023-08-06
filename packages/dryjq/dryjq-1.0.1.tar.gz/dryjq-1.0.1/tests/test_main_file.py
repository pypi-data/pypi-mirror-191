# -*- coding: utf-8 -*-

"""

test_main_file

Unit test the command line interface
with input from a file

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
import os
import secrets
import tempfile
import time

from unittest import TestCase
from unittest.mock import patch

from dryjq import __main__

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

    # tempdir = None

    def setUp(self):
        """Create a temporary directory"""
        # pylint: disable=consider-using-with
        self.tempdir = tempfile.TemporaryDirectory()
        # pylint: enable=consider-using-with
        self.testfile_name = os.path.join(
            self.tempdir.name, f"{secrets.token_urlsafe(6)}.yaml"
        )

    def tearDown(self):
        """Cleanup the temporary directory"""
        self.tempdir.cleanup()

    def __create_file(self, content=None):
        """Create a file in the temporary directory"""
        if content:
            with open(
                self.testfile_name,
                mode="w",
                encoding="utf-8",
            ) as testdata_file:
                testdata_file.write(content)
            #
        #

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_get_single_value(self, mock_stdout):
        """Get a single value"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        result = CommandLineResult.from_call(
            ".felines.cats.big[1]",
            self.testfile_name,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_CATS_BIG_1)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_get_subtree(self, mock_stdout):
        """Get a subtree"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        result = CommandLineResult.from_call(
            ".canines",
            self.testfile_name,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_YAML_CANINES)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_missing_list_value(self, mock_stdout):
        """Try to get a missing list value"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        missing_index = 5
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f".felines.cats.big[{missing_index}]",
                self.testfile_name,
                stdout=mock_stdout,
            )
        #
        self.assertIn(f"Index {missing_index!r} not found", log_cm.output[0])
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_missing_mapping_value(self, mock_stdout):
        """Try to get a missing mapping value"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        missing_key = "rodents"
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f".{missing_key}",
                self.testfile_name,
                stdout=mock_stdout,
            )
        #
        self.assertIn(f"Index {missing_key!r} not found", log_cm.output[0])
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_indexing_scalar_value(self, mock_stdout):
        """Try to get an indexed value from a scalar"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        wrong_index = 1
        path_to_value = ".felines.cats.big[0]"
        scalar_value = CommandLineResult.from_call(
            path_to_value,
            self.testfile_name,
            stdout=mock_stdout,
        ).stdout.rstrip()
        mock_stdout.seek(0)
        mock_stdout.truncate()
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f"{path_to_value}[{wrong_index}]",
                self.testfile_name,
                stdout=mock_stdout,
            )
        #
        self.assertIn(
            f"Scalar value {scalar_value!r} cannot have an index!",
            log_cm.output[0],
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_key_indexing_list(self, mock_stdout):
        """Try to get a value indexed by a key from a list"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        wrong_index = "lion"
        with self.assertLogs(None, level="ERROR") as log_cm:
            result = CommandLineResult.from_call(
                f".felines.cats.big[{wrong_index}]",
                self.testfile_name,
                stdout=mock_stdout,
            )
        #
        self.assertIn(
            f"PathComponent(index={wrong_index!r}, in_subscript=True)"
            " does not allow lists!",
            log_cm.output[0],
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_ERROR)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_replace_single_value(self, mock_stdout):
        """Replace a single value"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        result = CommandLineResult.from_call(
            ".felines.cats.big[2] = panther",
            self.testfile_name,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_YAML_JAGUAR2PANTHER)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_replace_subtree(self, mock_stdout):
        """Replace a subtree"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        result = CommandLineResult.from_call(
            f".felines.cats = {data.REPLACEMENT_YAML_CATS_TAXONOMY}",
            self.testfile_name,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_YAML_CATS_TAXONOMY)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_replace_subtree_inplace(self, mock_stdout):
        """Replace a subtree and modify the file in place"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        time.sleep(0.1)
        creation_time = os.stat(self.testfile_name).st_mtime
        result = CommandLineResult.from_call(
            "--inplace",
            f".felines.cats = {data.REPLACEMENT_YAML_CATS_TAXONOMY}",
            self.testfile_name,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_OK)
        self.assertGreater(os.stat(self.testfile_name).st_mtime, creation_time)
        with open(
            self.testfile_name, mode="r", encoding="utf-8"
        ) as changed_file:
            changed_data = changed_file.read()
        #
        self.assertEqual(changed_data, data.EXPECT_YAML_CATS_TAXONOMY)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_unchanged_file(self, mock_stdout):
        """Do a modification not changing original data"""
        self.__create_file(content=data.INPUT_YAML_ANIMALS)
        time.sleep(0.1)
        creation_time = os.stat(self.testfile_name).st_mtime
        with self.assertLogs(None, level="WARNING") as log_cm:
            result = CommandLineResult.from_call(
                "--inplace",
                ".felines.cats.big[2] = jaguar",
                self.testfile_name,
                stdout=mock_stdout,
            )
        #
        self.assertIn(
            "contents did not change",
            log_cm.output[0],
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.returncode, data.RETURNCODE_OK)
        self.assertEqual(os.stat(self.testfile_name).st_mtime, creation_time)
        with open(
            self.testfile_name, mode="r", encoding="utf-8"
        ) as unchanged_file:
            unchanged_data = unchanged_file.read()
        #
        self.assertEqual(unchanged_data, data.INPUT_YAML_ANIMALS)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
