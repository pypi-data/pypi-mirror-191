#!../../../../venv/bin/pytest

import os
import sys
import subprocess

import pytest

def test__output() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_output = os.path.join(path, 'output.txt')
	env = {'HOME' : '/home/username'}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	if sys.version_info < (3, 10):
		expected_output = expected_output.replace('options:', 'optional arguments:')

	assert p.stdout.decode() == expected_output

def test_normal_config() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_config.py')
	fn_expected_output = os.path.join(path, 'expected-config')
	env = {'HOME' : '/home/username'}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert p.stdout.decode() == expected_output


def test_raw_help() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_raw_help.py')
	fn_expected_output = os.path.join(path, 'expected-raw-help.txt')
	env = {'HOME' : '/home/username'}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	if sys.version_info < (3, 10):
		expected_output = expected_output.replace('options:', 'optional arguments:')

	assert p.stdout.decode() == expected_output

def test_raw_config() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_raw_config.py')
	fn_expected_output = os.path.join(path, 'expected-raw-config')
	env = {'HOME' : '/home/username'}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert p.stdout.decode() == expected_output
