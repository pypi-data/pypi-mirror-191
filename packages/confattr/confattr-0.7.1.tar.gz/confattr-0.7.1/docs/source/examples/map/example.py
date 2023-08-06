#!../../../../venv/bin/python3

__package__ = 'map-exp'

import os
from confattr import ConfigFile
ConfigFile.config_directory = os.path.dirname(__file__)

# ------- start -------
import argparse
from collections.abc import Sequence
import urwid
from confattr import ConfigFileArgparseCommand, ConfigFile, Config, NotificationLevel


class Map(ConfigFileArgparseCommand):

	'''
	bind a command to a key
	'''

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('key', help='http://urwid.org/manual/userinput.html#keyboard-input')
		parser.add_argument('cmd', help='any urwid command')

	def run_parsed(self, args: argparse.Namespace) -> None:
		urwid.command_map[args.key] = args.cmd


if __name__ == '__main__':
	# config
	choices = Config('choices', ['vanilla', 'strawberry'])
	urwid.command_map['enter'] = 'confirm'
	config_file = ConfigFile(appname=__package__)
	config_file.load()

	# show errors in config
	palette = [(NotificationLevel.ERROR.value, 'dark red', 'default')]
	status_bar = urwid.Pile([])
	def on_config_message(lvl: NotificationLevel, msg: 'str|BaseException') -> None:
		markup = (lvl.value, str(msg))
		widget_options_tuple = (urwid.Text(markup), status_bar.options('pack'))
		status_bar.contents.append(widget_options_tuple)
	config_file.set_ui_callback(on_config_message)

	# a simple example app showing check boxes and printing the user's choice to stdout
	def key_handler(key: str) -> None:
		cmd = urwid.command_map[key]
		if cmd == 'confirm':
			raise urwid.ExitMainLoop()
	checkboxes = [urwid.CheckBox(choice) for choice in choices.value]
	frame = urwid.Frame(urwid.Filler(urwid.Pile(checkboxes)), footer=status_bar)
	urwid.MainLoop(frame, palette=palette, unhandled_input=key_handler).run()

	for ckb in checkboxes:
		print(f'{ckb.label}: {ckb.state}')
