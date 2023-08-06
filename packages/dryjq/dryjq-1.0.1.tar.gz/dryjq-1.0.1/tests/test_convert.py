# -*- coding: utf-8 -*-

"""

test.test_convert

Unit test the 'dryjq.convert' command line interface

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

from unittest import TestCase
from unittest.mock import patch

import dryjq

from dryjq import convert

from . import data
from .commons import GenericCallResult


class ConvertResult(GenericCallResult):

    """Conversion result"""

    @classmethod
    def do_call(cls, *args, **kwargs):
        """Do the real function call"""
        del kwargs
        return convert.main(list(args))


class TestSimple(TestCase):

    """Simple test module using patched stdin and stdout"""

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_convert_json2yaml(self, mock_stdout):
        """Convert JSON to YAML"""
        result = ConvertResult.from_call(
            stdin_data=data.INPUT_JSON_AURORA,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_CONVERTED_YAML_AURORA)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_convert_yaml2json(self, mock_stdout):
        """Convert YAML to json"""
        result = ConvertResult.from_call(
            stdin_data=data.INPUT_YAML_ANIMALS,
            stdout=mock_stdout,
        )
        self.assertEqual(result.stdout, data.EXPECT_CONVERTED_JSON_ANIMALS)
        self.assertEqual(result.returncode, data.RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_version(self, mock_stdout):
        """Print version"""
        with self.assertRaises(SystemExit) as sys_exit:
            result = ConvertResult.from_call(
                "--version",
                stdout=mock_stdout,
            )
            self.assertEqual(
                result.stdout, f"dryjq.convert {dryjq.__version__}\n"
            )
            self.assertEqual(result.returncode, data.RETURNCODE_OK)
        #
        self.assertEqual(sys_exit.exception.code, data.RETURNCODE_OK)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
