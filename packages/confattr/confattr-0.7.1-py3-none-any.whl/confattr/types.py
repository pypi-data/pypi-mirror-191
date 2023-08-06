#!./runmodule.sh

import os
import shutil
import shlex
import typing
from collections.abc import Sequence, Callable, Mapping, MutableMapping

from .subprocess_pipe import run_and_pipe, CompletedProcess


TYPE_CONTEXT: 'typing.TypeAlias' = 'Callable[[SubprocessCommand], typing.ContextManager[SubprocessCommand]] | None'


class Path:

	'''
	This is the path as it is stored in the config file.
	It needs to be processed before usage.
	In the easiest case that is as easy as calling os.path.expanduser
	but you may want to do more like checking that the path exists
	or mounting an external drive.
	'''

	type_name = 'path'
	help = 'The path to a file or directory'

	def __init__(self, value: str) -> None:
		self.raw = value

	def __str__(self) -> str:
		return self.raw

	def __repr__(self) -> str:
		return '%s(%r)' % (type(self).__name__, self.raw)

	def __bool__(self) -> bool:
		return bool(self.raw)


class Regex(str):

	type_name = 'regular expression'
	help = 'https://docs.python.org/3/library/re.html#regular-expression-syntax'


class SubprocessCommand:

	type_name = 'command'
	help = '''\
	A command to be executed as a subprocess.
	The command is executed without a shell so redirection or wildcard expansion is not possible.
	Setting environment variables and piping like in a POSIX shell, however, are implemented in python and should work platform independently.
	If you need a shell write the command to a file, insert an appropriate shebang line, make the file executable and set this value to the file.
	'''

	python_callbacks: 'MutableMapping[str, Callable[[SubprocessCommand, TYPE_CONTEXT], None]]' = {}

	@classmethod
	def register_python_callback(cls, name: str, func: 'Callable[[SubprocessCommand, TYPE_CONTEXT], None]') -> None:
		cls.python_callbacks[name] = func

	@classmethod
	def unregister_python_callback(cls, name: str) -> None:
		del cls.python_callbacks[name]

	@classmethod
	def has_python_callback(cls, name: str) -> bool:
		return name in cls.python_callbacks


	def __init__(self, arg: 'SubprocessCommand|Sequence[str]|str', *, env: 'Mapping[str, str]|None' = None) -> None:
		self.cmd: 'Sequence[str]'
		self.env: 'Mapping[str, str]|None'
		if isinstance(arg, str):
			assert env is None
			self.parse_str(arg)
		elif isinstance(arg, SubprocessCommand):
			self.cmd = list(arg.cmd)
			self.env = dict(arg.env) if arg.env else None
			if env:
				if self.env:
					self.env.update(env)
				else:
					self.env = env
		else:
			self.cmd = list(arg)
			self.env = env

	def parse_str(self, arg: str) -> None:
		'''
		Parses a string as returned by :meth:`__str__` and initializes this objcet accordingly

		:param arg: The string to be parsed
		:raises ValueError: if arg is invalid

		Example:
			If the input is ``arg = 'ENVVAR1=val ENVVAR2= cmd --arg1 --arg2'``
			this function sets
			.. code-block::

				self.env = {'ENVVAR1' : 'val', 'ENVVAR2' : ''}
				self.cmd = ['cmd', '--arg1', '--arg2']
		'''
		if not arg:
			raise ValueError('cmd is empty')

		cmd = shlex.split(arg)

		self.env = {}
		for i in range(len(cmd)):
			if '=' in cmd[i]:
				var, val = cmd[i].split('=', 1)
				self.env[var] = val
			else:
				self.cmd = cmd[i:]
				if not self.env:
					self.env = None
				return

		raise ValueError('cmd consists of environment variables only, there is no command to be executed')

	# ------- compare -------

	def __eq__(self, other: typing.Any) -> bool:
		if isinstance(other, SubprocessCommand):
			return self.cmd == other.cmd and self.env == other.env
		return NotImplemented

	# ------- custom methods -------

	def replace(self, wildcard: str, replacement: str) -> 'SubprocessCommand':
		return SubprocessCommand([replacement if word == wildcard else word for word in self.cmd], env=self.env)

	def run(self, *, context: 'TYPE_CONTEXT|None') -> 'CompletedProcess[bytes]|None':
		'''
		Runs this command and returns when the command is finished.

		:param context: returns a context manager which can be used to stop and start an urwid screen.
		It takes the command to be executed so that it can log the command
		and it returns the command to be executed so that it can modify the command,
		e.g. processing and intercepting some environment variables.

		:return: The completed process
		:raises OSError: e.g. if the program was not found
		:raises CalledProcessError: if the called program failed
		'''
		if self.cmd[0] in self.python_callbacks:
			self.python_callbacks[self.cmd[0]](self, context)
			return None

		if context is None:
			return run_and_pipe(self.cmd, env=self._add_os_environ(self.env))

		with context(self) as command:
			return run_and_pipe(command.cmd, env=self._add_os_environ(command.env))

	@staticmethod
	def _add_os_environ(env: 'Mapping[str, str]|None') -> 'Mapping[str, str]|None':
		if env is None:
			return env
		return dict(os.environ, **env)

	def is_installed(self) -> bool:
		return self.cmd[0] in self.python_callbacks or bool(shutil.which(self.cmd[0]))

	# ------- to str -------

	def __str__(self) -> str:
		if self.env:
			env = ' '.join('%s=%s' % (var, shlex.quote(val)) for var, val in self.env.items())
			env += ' '
		else:
			env = ''
		return env + ' '.join(shlex.quote(word) for word in self.cmd)

	def __repr__(self) -> str:
		return '%s(%r, env=%r)' % (type(self).__name__, self.cmd, self.env)

class SubprocessCommandWithAlternatives:

	type_name = 'command with alternatives'
	help = '''
	One or more commands separated by ||.
	The first command where the program is installed is executed. The other commands are ignored.

	The command is executed without a shell so redirection or wildcard expansion is not possible.
	Setting environment variables and piping like in a POSIX shell, however, are implemented in python and should work platform independently.
	If you need a shell write the command to a file, insert an appropriate shebang line, make the file executable and set this value to the file.
	'''

	SEP = '||'

	def get_preferred_command(self) -> SubprocessCommand:
		for cmd in self.commands:
			if cmd.is_installed():
				return cmd

		raise FileNotFoundError('none of the commands is installed: %s' % self)


	def __init__(self, commands: 'Sequence[SubprocessCommand|Sequence[str]|str]|str') -> None:
		if isinstance(commands, str):
			self.commands = [SubprocessCommand(cmd) for cmd in commands.split(self.SEP)]
		else:
			self.commands = [SubprocessCommand(cmd) for cmd in commands]


	def __str__(self) -> str:
		return self.SEP.join(str(cmd) for cmd in self.commands)

	def __repr__(self) -> str:
		return '%s(%s)' % (type(self).__name__, self.commands)


	def replace(self, wildcard: str, replacement: str) -> SubprocessCommand:
		return self.get_preferred_command().replace(wildcard, replacement)

	def run(self, context: 'TYPE_CONTEXT|None' = None) -> 'CompletedProcess[bytes]|None':
		return self.get_preferred_command().run(context=context)
