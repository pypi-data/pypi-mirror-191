__package__ = 'exp'

# ------- start -------
from confattr import Set, ParseException, ConfigId, FormattedWriter, SectionLevel

import typing
if typing.TYPE_CHECKING:
	from confattr import ParseSplittedLineKwargs, SaveKwargs
	from typing_extensions import Unpack
	from collections.abc import Sequence


class SimpleSet(Set, replace=True):

	name = ''

	SEP = ':'

	def run(self, cmd: 'Sequence[str]', **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		ln = kw['line']
		if self.SEP not in ln:
			raise ParseException(f'missing {self.SEP} between key and value')
		key, value = ln.split(self.SEP)
		value = value.lstrip()
		self.parse_key_and_set_value(key, value)

	def save_config_instance(self, writer: FormattedWriter, instance: 'Config[object]', config_id: 'ConfigId|None', **kw: 'Unpack[SaveKwargs]') -> None:
		# this is called by Set.save
		if kw['comments']:
			self.write_config_help(writer, instance)
		value = self.format_value(instance, config_id)
		#value = self.config_file.quote(value)  # not needed because run uses line instead of cmd
		writer.write_command(f'{instance.key}{self.SEP} {value}')


if __name__ == '__main__':
	from confattr import Config, ConfigFile
	color = Config('favorite color', 'white')
	subject = Config('favorite subject', 'math')
	config_file = ConfigFile(appname=__package__)
	config_file.load()
	config_file.set_ui_callback(lambda lvl, msg: print(msg))
	print(color.value)
	print(subject.value)
