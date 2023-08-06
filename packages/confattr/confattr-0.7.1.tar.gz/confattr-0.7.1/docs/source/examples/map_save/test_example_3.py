#!../../../../venv/bin/pytest

import os
import sys
import subprocess


def test__example_1() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_1.py')
	p = subprocess.run([sys.executable, fn_script], stdout=subprocess.PIPE, check=True)

	# I am not checking the output to avoid a fail if urwid.command_map changes
	# but I at least want to make sure that it runs without raising an exception


def test__output__example_3() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_3.py')
	fn_expected_output = os.path.join(path, 'config_expected')
	fn_generated_output = os.path.join(path, 'config')
	p = subprocess.run([sys.executable, fn_script], stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	with open(fn_generated_output, 'rt') as f:
		generated_output = f.read()

	assert generated_output == expected_output
