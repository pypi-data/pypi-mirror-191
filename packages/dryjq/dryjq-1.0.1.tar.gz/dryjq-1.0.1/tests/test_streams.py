# -*- coding: utf-8 -*-

"""

test_streams

Unit test the streams module

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
import sys
import tempfile
import time

from unittest import TestCase
from unittest.mock import patch

from dryjq import access
from dryjq import streams

from . import data


class StreamReader(TestCase):

    """StreamReader tests"""

    def test_yaml_properties(self):
        """Test properties (YAML input)"""
        stream_io = io.StringIO(data.INPUT_YAML_ANIMALS)
        stream_reader = streams.StreamReader(stream_io)
        stream_reader.execute_single_query(
            access.ExtractingPath(
                access.PathComponent("felines"),
                access.PathComponent("cats"),
                access.PathComponent("big"),
                access.PathComponent(1, in_subscript=True),
            )
        )
        for tested_property, expected_value in (
            ("input_contents", data.INPUT_YAML_ANIMALS),
            ("input_format", "YAML"),
            ("output_contents", data.EXPECT_CATS_BIG_1),
            ("output_format", "YAML"),
            ("stream_io", stream_io),
        ):
            with self.subTest(
                tested_property=tested_property, expected_value=expected_value
            ):
                self.assertEqual(
                    getattr(stream_reader, tested_property),
                    expected_value,
                )
            #
        #

    def test_json_properties(self):
        """Test properties (JSON input)"""
        stream_io = io.StringIO(data.INPUT_JSON_ANIMALS)
        stream_reader = streams.StreamReader(stream_io)
        stream_reader.execute_single_query(
            access.ExtractingPath(access.PathComponent("canines"))
        )
        for tested_property, expected_value in (
            ("input_contents", data.INPUT_JSON_ANIMALS),
            ("input_format", "JSON"),
            ("output_contents", data.EXPECT_JSON_CANINES),
            ("output_format", "JSON"),
            ("stream_io", stream_io),
        ):
            with self.subTest(
                tested_property=tested_property, expected_value=expected_value
            ):
                self.assertEqual(
                    getattr(stream_reader, tested_property),
                    expected_value,
                )
            #
        #

    def test_json2yaml_properties(self):
        """Test properties (JSON input -> YAML output)"""
        stream_io = io.StringIO(data.INPUT_JSON_ANIMALS)
        stream_reader = streams.StreamReader(stream_io)
        stream_reader.execute_single_query(
            access.ExtractingPath(access.PathComponent("canines"))
        )
        stream_reader.set_serialization_format(output_format="YAML")
        for tested_property, expected_value in (
            ("input_contents", data.INPUT_JSON_ANIMALS),
            ("input_format", "JSON"),
            ("output_contents", data.EXPECT_YAML_CANINES),
            ("output_format", "YAML"),
            ("stream_io", stream_io),
        ):
            with self.subTest(
                tested_property=tested_property, expected_value=expected_value
            ):
                self.assertEqual(
                    getattr(stream_reader, tested_property),
                    expected_value,
                )
            #
        #

    def test_yaml2json_properties(self):
        """Test properties (YAML input -> JSON output)"""
        stream_io = io.StringIO(data.INPUT_YAML_ANIMALS)
        stream_reader = streams.StreamReader(stream_io)
        stream_reader.execute_single_query(
            access.ExtractingPath(access.PathComponent("canines"))
        )
        stream_reader.set_serialization_format(output_format="JSON")
        for tested_property, expected_value in (
            ("input_contents", data.INPUT_YAML_ANIMALS),
            ("input_format", "YAML"),
            ("output_contents", data.EXPECT_JSON_CANINES),
            ("output_format", "JSON"),
            ("stream_io", stream_io),
        ):
            with self.subTest(
                tested_property=tested_property, expected_value=expected_value
            ):
                self.assertEqual(
                    getattr(stream_reader, tested_property),
                    expected_value,
                )
            #
        #

    def test_valid_formats(self):
        """Test valid formats (YAML input)"""
        stream_io = io.StringIO(data.INPUT_YAML_ANIMALS)
        stream_reader = streams.StreamReader(stream_io)
        for output_format, expected_value in (
            ("input", data.INPUT_YAML_ANIMALS),
            ("toggle", data.EXPECT_CONVERTED_JSON_ANIMALS.rstrip()),
            ("YAML", data.INPUT_YAML_ANIMALS),
            ("JSON", data.EXPECT_CONVERTED_JSON_ANIMALS.rstrip()),
        ):
            with self.subTest(output_format=output_format):
                stream_reader.set_serialization_format(
                    output_format=output_format
                )
                self.assertEqual(
                    stream_reader.output_contents,
                    expected_value,
                )
            #
        #

    def test_unsupported_output_format(self):
        """Test unsupported output format"""
        stream_io = io.StringIO(data.INPUT_YAML_ANIMALS)
        stream_reader = streams.StreamReader(stream_io)
        self.assertRaisesRegex(
            ValueError,
            "Output format 'XML' not supported!",
            stream_reader.set_serialization_format,
            output_format="XML",
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_writing_output(self, mock_stdout):
        """Test writing output to standard output"""
        assert mock_stdout is sys.stdout
        stream_io = io.StringIO(data.INPUT_JSON_ANIMALS)
        stream_reader = streams.StreamReader(stream_io)
        stream_reader.execute_single_query(
            access.ExtractingPath(access.PathComponent("canines"))
        )
        stream_reader.set_serialization_format(output_format="YAML")
        stream_reader.write_output()
        self.assertEqual(mock_stdout.getvalue(), data.EXPECT_YAML_CANINES)


class FileWriter(TestCase):

    """FileWriter tests"""

    def test_file_output(self):
        """Test modification of an existing file"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            yaml_file_name = os.path.join(
                temporary_directory, f"{secrets.token_urlsafe(6)}.yaml"
            )
            with open(
                yaml_file_name, mode="w", encoding="utf-8"
            ) as source_file:
                source_file.write(data.INPUT_YAML_ANIMALS)
            #
            time.sleep(0.1)
            creation_time = os.stat(yaml_file_name).st_mtime
            with open(yaml_file_name, mode="r+", encoding="utf-8") as io_file:
                file_writer = streams.FileWriter(io_file)
                file_writer.execute_single_query(
                    access.ReplacingPath(
                        access.PathComponent("felines"),
                        access.PathComponent("cats"),
                        access.PathComponent("big"),
                        access.PathComponent(2, in_subscript=True),
                        replacement="panther",
                    )
                )
                file_writer.write_output()
            #
            # File changed after creation
            self.assertGreater(os.stat(yaml_file_name).st_mtime, creation_time)
            with open(
                yaml_file_name, mode="r", encoding="utf-8"
            ) as changed_file:
                self.assertEqual(
                    changed_file.read(), data.EXPECT_YAML_JAGUAR2PANTHER
                )
            #
        #

    def test_unchanged_output(self):
        """Test modification of an existing file without changing output"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            yaml_file_name = os.path.join(
                temporary_directory, f"{secrets.token_urlsafe(6)}.yaml"
            )
            with open(
                yaml_file_name, mode="w", encoding="utf-8"
            ) as source_file:
                source_file.write(data.INPUT_YAML_ANIMALS)
            #
            time.sleep(0.1)
            creation_time = os.stat(yaml_file_name).st_mtime
            with open(yaml_file_name, mode="r+", encoding="utf-8") as io_file:
                file_writer = streams.FileWriter(io_file)
                with self.assertLogs(level="ERROR") as log_cm:
                    file_writer.write_output()
                #
                self.assertIn(
                    "Not writing file: contents did not change.",
                    log_cm.records[0].message,
                )
            #
            # File NOT changed after creation
            self.assertEqual(os.stat(yaml_file_name).st_mtime, creation_time)
            with open(
                yaml_file_name, mode="r", encoding="utf-8"
            ) as changed_file:
                self.assertEqual(changed_file.read(), data.INPUT_YAML_ANIMALS)
            #
        #

    def test_changed_format(self):
        """Test modification of an existing file with changed format"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            yaml_file_name = os.path.join(
                temporary_directory, f"{secrets.token_urlsafe(6)}.yaml"
            )
            with open(
                yaml_file_name, mode="w", encoding="utf-8"
            ) as source_file:
                source_file.write(data.INPUT_YAML_ANIMALS)
            #
            time.sleep(0.1)
            creation_time = os.stat(yaml_file_name).st_mtime
            with open(yaml_file_name, mode="r+", encoding="utf-8") as io_file:
                file_writer = streams.FileWriter(io_file)
                file_writer.execute_single_query(
                    access.ReplacingPath(
                        access.PathComponent("felines"),
                        access.PathComponent("cats"),
                        access.PathComponent("big"),
                        access.PathComponent(2, in_subscript=True),
                        replacement="panther",
                    )
                )
                file_writer.set_serialization_format(output_format="JSON")
                with self.assertLogs(level="ERROR") as log_cm:
                    file_writer.write_output()
                #
                self.assertIn(
                    "Not writing file: data format changed.",
                    log_cm.records[0].message,
                )
            #
            # File NOT changed after creation
            self.assertEqual(os.stat(yaml_file_name).st_mtime, creation_time)
            with open(
                yaml_file_name, mode="r", encoding="utf-8"
            ) as changed_file:
                self.assertEqual(changed_file.read(), data.INPUT_YAML_ANIMALS)
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
