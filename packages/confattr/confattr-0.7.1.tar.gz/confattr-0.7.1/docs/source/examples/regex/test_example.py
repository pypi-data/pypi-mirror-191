#!../../../../venv/bin/pytest

import os
import sys
import subprocess

from .example import Parser

def test_parser() -> None:
	p = Parser()
	p.compile_regex()

	m = p.reo_mount_output.match('Mounted /dev/sdb1 at /media/usb1')
	assert m is not None
	assert m.group('mountpath') == '/media/usb1'

	m = p.reo_mount_output.match('Unlocked /dev/sdc at /dev/dm-5')
	assert m is not None
	assert m.group('mountpath') == '/dev/dm-5'

def test_export() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_config_export = os.path.join(path, 'expected-config')
	fn_exported_config = os.path.join(path, 'config')
	env = {'REGEX_EXP_CONFIG_DIRECTORY' : path}
	p = subprocess.run([sys.executable, fn_script], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_config_export, 'rt') as f:
		expected_config_export = f.read()

	with open(fn_exported_config, 'rt') as f:
		exported_config = f.read()

	assert exported_config == expected_config_export
