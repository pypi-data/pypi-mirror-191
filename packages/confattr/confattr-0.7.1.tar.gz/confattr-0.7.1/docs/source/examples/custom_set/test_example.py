#!../../../../venv/bin/pytest

import os
import sys
import subprocess
import pathlib

def test__output() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_output = os.path.join(path, 'output.txt')
	env = {'EXP_CONFIG_DIRECTORY' : path}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert p.stdout.decode() == expected_output

def test__output_no_include() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_no_include.py')
	fn_expected_output = os.path.join(path, 'output_no_include.txt')
	env = {'EXP_CONFIG_DIRECTORY' : path}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert p.stdout.decode() == expected_output


def test__save(tmp_path: pathlib.Path) -> None:
	fn_script = os.path.join(os.path.dirname(__file__), 'example_save.py')
	env = {'EXP_CONFIG_DIRECTORY' : str(tmp_path)}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)
