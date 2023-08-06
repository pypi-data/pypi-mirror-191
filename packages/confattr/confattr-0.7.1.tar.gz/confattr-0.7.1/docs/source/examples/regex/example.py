__package__ = 'regex exp'

# ------- start -------
import re
from confattr import Config, ConfigFile

class Regex(str):

	type_name = 'regular expression'
	help = 'https://docs.python.org/3/library/re.html#regular-expression-syntax'

class Parser:

	re_mount_output = Config('udisksctl.mount-output-pattern', Regex(r'^.*?(?P<mountpath>/(\S+/)*[^/]+?)\.?$'),
		help='a regular expression to parse the output of `udisksctl mount`. Must contain a named group called "mountpath".')
	re_unlock_output = Config('udisksctl.unlock-output-pattern', Regex(r'^.*?(?P<unlockpath>/(\S+/)*[^/]+?)\.?$'),
		help='a regular expression to parse the output of `udisksctl unlock`. Must contain a named group called "unlockpath".')

	def compile_regex(self) -> None:
		'''
		This must be called every time after the config file has been loaded.
		'''
		self.reo_mount_output = re.compile(self.re_mount_output)
		self.reo_unlock_output = re.compile(self.re_unlock_output)

if __name__ == '__main__':
	ConfigFile(appname=__package__).save()
