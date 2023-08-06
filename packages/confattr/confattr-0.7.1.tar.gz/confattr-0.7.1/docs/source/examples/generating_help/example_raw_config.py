#!../../../../venv/bin/python3

__package__ = 'exampleapp'


import typing

from confattr import ConfigFile, ConfigFileWriter
from argparse import RawTextHelpFormatter

if typing.TYPE_CHECKING:
	from . import example
else:
	import example

config_file = ConfigFile(appname=__package__, formatter_class=RawTextHelpFormatter)
config_file.save_to_writer(ConfigFileWriter(f=None, prefix='# '))
