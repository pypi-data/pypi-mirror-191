#!/usr/bin/env python3
__package__ = 'exp'

# ------- start -------
from confattr import Config, ConfigFile

class App:

	color = Config('color', 'red', allowed_values=['red', 'green', 'blue'])


if __name__ == '__main__':
	config_file = ConfigFile(appname=__package__)
	config_file.load()

	a = App()
	print(a.color)
