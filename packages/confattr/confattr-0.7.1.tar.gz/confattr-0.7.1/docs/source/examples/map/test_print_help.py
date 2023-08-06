#!../../../../venv/bin/pytest

import os
import sys
import subprocess

def test__output() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_print_help.py')
	fn_expected_output = os.path.join(path, 'output_help.txt')
	env = {'MAP_EXP_CONFIG_DIRECTORY' : path}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert p.stdout.decode() == expected_output
