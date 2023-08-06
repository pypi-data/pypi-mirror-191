#!../../../../venv/bin/pytest

from .example import Car

import os
import sys
import subprocess
import pytest

def test__accelerate() -> None:
	c1 = Car()
	assert c1.speed == 0
	assert c1.speed_limit == 50

	c1.accelerate(49)
	assert c1.speed == 49
	c1.accelerate(1)
	assert c1.speed == 50
	with pytest.raises(ValueError):
		c1.accelerate(1)
	assert c1.speed == 50


def test__print_config(capsys: 'pytest.CaptureFixture[str]') -> None:
	c1 = Car()
	c1.print_config()
	captured = capsys.readouterr()
	assert captured.out == "traffic-law.speed-limit: 50\n"


def test__output() -> None:
	# output.txt does not contain "configuration was written to ..." because print is redefined to do nothing
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_output = os.path.join(path, 'output.txt')
	env = {'EXP_CONFIG_DIRECTORY' : path}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert p.stdout.decode() == expected_output

	with open(os.path.join(path, 'expected-config'), 'rt') as f:
		expected_config = f.read()
	with open(os.path.join(path, 'exported-config'), 'rt') as f:
		exported_config = f.read()
	assert exported_config == expected_config
