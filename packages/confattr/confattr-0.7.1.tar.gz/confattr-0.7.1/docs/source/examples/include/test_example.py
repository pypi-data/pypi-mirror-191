#!../../../../venv/bin/pytest -s

from .example import App

import os
import pytest
from confattr import ConfigFile

def test__output(monkeypatch: 'pytest.MonkeyPatch') -> None:
	path = os.path.dirname(__file__)
	monkeypatch.setattr(ConfigFile, 'config_directory', path)
	fn = os.path.join(path, 'output.txt')
	app = App()
	with open(fn, 'rb') as f:
		expected = f.read().splitlines()
		assert app.frame.render((51,5)).text == expected
