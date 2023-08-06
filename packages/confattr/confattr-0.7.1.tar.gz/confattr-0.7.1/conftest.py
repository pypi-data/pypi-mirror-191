#!venv/bin/pytest

from confattr import ConfigFile

import pytest

@pytest.fixture(autouse=True)
def reset_config_path() -> None:
	assert ConfigFile.config_path is None
	assert ConfigFile.config_directory is None
