#!./runmodule.sh

'''
This module defines the ConfigFile class
which can be used to load and save config files.
'''

import os
import shlex
import enum
import functools
import argparse
import inspect
import io
import abc
import typing
from collections.abc import Iterable, Iterator, Sequence, Callable

import appdirs

from .config import Config, DictConfig, MultiConfig, ConfigId
from .utils import HelpFormatter, HelpFormatterWrapper

if typing.TYPE_CHECKING:
	from typing_extensions import Unpack, Required, Self


#: If the name or an alias of :class:`ConfigFileCommand` is this value that command is used by :meth:`ConfigFile.parse_splitted_line` if an undefined command is encountered.
DEFAULT_COMMAND = ''


def readable_quote(value: str) -> str:
	'''
	This function has the same goal like :func:`shlex.quote` but tries to generate better readable output.

	:param value: A value which is intended to be used as a command line argument
	:return: A POSIX compliant quoted version of :paramref:`value`
	'''
	out = shlex.quote(value)
	if out == value:
		return out

	if '"\'"' in out and '"' not in value:
		return '"' + value + '"'

	return out


# ---------- UI notifier ----------

@functools.total_ordering
class SortedEnum(enum.Enum):

	'''
	By default it is assumed that the values are defined in ascending order ``ONE='one'; TWO='two'; THREE='three'``.
	If you want to define them in descending order ``THREE='three'; TWO='two'; ONE='one'`` you can pass ``descending = True`` to the subclass.
	Passing :paramref:`descending` requires Python 3.10.0a4 or newer.
	On older versions it causes a ``TypeError: __prepare__() got an unexpected keyword argument 'descending'``.
	This was fixed in `commit 6ec0adefad <https://github.com/python/cpython/commit/6ec0adefad60ec7cdec61c44baecf1dccc1461ab>`_.
	'''

	descending: bool

	@classmethod
	def __init_subclass__(cls, descending: bool = False):
		cls.descending = descending

	def __lt__(self, other: typing.Any) -> bool:
		if self.__class__ is other.__class__:
			l: 'Sequence[SortedEnum]' = list(type(self))
			if self.descending:
				left = other
				right = self
			else:
				left = self
				right = other
			return l.index(left) < l.index(right)
		return NotImplemented

	def __add__(self, other: object) -> 'Self':  #type: ignore [valid-type]  # bug in mypy. merged but not yet released. https://github.com/python/mypy/pull/14041
		if isinstance(other, int):
			l: 'Sequence[Self]' = list(type(self))  #type: ignore [valid-type]  # bug in mypy. merged but not yet released. https://github.com/python/mypy/pull/14041
			i = l.index(self)
			if self.descending:
				other = -other
			i += other
			if i < 0:
				i = 0
			elif i >= len(l):
				i = len(l) - 1
			return l[i]
		return NotImplemented

	def __sub__(self, other: object) -> 'Self':  #type: ignore [valid-type]  # bug in mypy. merged but not yet released. https://github.com/python/mypy/pull/14041
		if isinstance(other, int):
			return self + (-other)
		return NotImplemented



@enum.unique
class NotificationLevel(SortedEnum):
	INFO = 'info'
	ERROR = 'error'

UiCallback: 'typing.TypeAlias' = 'Callable[[NotificationLevel, str|BaseException], None]'

class UiNotifier:

	'''
	Most likely you will want to load the config file before creating the UI (user interface).
	But if there are errors in the config file the user will want to know about them.
	This class takes the messages from :class:`ConfigFile` and stores them until the UI is ready.
	When you call :meth:`set_ui_callback` the stored messages will be forwarded and cleared.

	This object can also filter the messages.
	:class:`ConfigFile` calls :meth:`show_info` every time a setting is changed.
	If you load an entire config file this can be many messages and the user probably does not want to see them all.
	Therefore this object drops all messages of :const:`NotificationLevel.INFO` by default.
	Pass :obj:`notification_level` to the constructor if you don't want that.
	'''

	# ------- public methods -------

	def __init__(self, notification_level: 'Config[NotificationLevel]|NotificationLevel' = NotificationLevel.ERROR) -> None:
		self._messages: 'list[tuple[NotificationLevel, str|BaseException]]' = []
		self._callback: 'UiCallback|None' = None
		self._notification_level = notification_level

	def set_ui_callback(self, callback: UiCallback) -> None:
		'''
		Call :paramref:`callback` for all messages which have been saved by :meth:`show` and clear all saved messages afterwards.
		Save :paramref:`callback` for :meth:`show` to call.
		'''
		self._callback = callback

		for lvl, msg in self._messages:
			callback(lvl, msg)
		self._messages.clear()


	@property
	def notification_level(self) -> NotificationLevel:
		'''
		Ignore messages that are less important than this level.
		'''
		if isinstance(self._notification_level, Config):
			return self._notification_level.value
		else:
			return self._notification_level

	@notification_level.setter
	def notification_level(self, val: NotificationLevel) -> None:
		if isinstance(self._notification_level, Config):
			self._notification_level.value = val
		else:
			self._notification_level = val


	# ------- called by ConfigFile -------

	def show_info(self, msg: str, *, ignore_filter: bool = False) -> None:
		'''
		Call :meth:`show` with :obj:`NotificationLevel.INFO`.
		'''
		self.show(NotificationLevel.INFO, msg, ignore_filter=ignore_filter)

	def show_error(self, msg: 'str|BaseException', *, ignore_filter: bool = False) -> None:
		'''
		Call :meth:`show` with :obj:`NotificationLevel.ERROR`.
		'''
		self.show(NotificationLevel.ERROR, msg, ignore_filter=ignore_filter)


	# ------- internal methods -------

	def show(self, notification_level: NotificationLevel, msg: 'str|BaseException', *, ignore_filter: bool = False) -> None:
		'''
		If a callback for the user interface has been registered with :meth:`set_ui_callback` call that callback.
		Otherwise save the message so that :meth:`set_ui_callback` can forward the message when :meth:`set_ui_callback` is called.

		:param notification_level: The importance of the message
		:param msg: The message to be displayed on the user interface
		:param ignore_filter: If true: Show the message even if :paramref:`notification_level` is smaller then the :paramref:`UiNotifier.notification_level`.
		'''
		if notification_level < self.notification_level and not ignore_filter:
			return

		if self._callback:
			self._callback(notification_level, msg)
		else:
			self._messages.append((notification_level, msg))


# ---------- format help ----------

class SectionLevel(SortedEnum):

	#: Is used to separate different commands in :meth:`ConfigFile.write_help` and :meth:`ConfigFileCommand.save`
	SECTION = 'section'

	#: Is used for subsections in :meth:`ConfigFileCommand.save` such as the "data types" section in the help of the set command
	SUB_SECTION = 'sub-section'


class FormattedWriter(abc.ABC):

	@abc.abstractmethod
	def write_line(self, ln: str) -> None:
		'''
		Write a single line of documentation.
		:paramref:`ln` may *not* contain a newline.
		If :paramref:`ln` is empty it does not need to be prefixed with a comment character.
		Empty lines should be dropped if no other lines have been written before.
		'''
		pass

	def write_lines(self, text: str) -> None:
		'''
		Write one or more lines of documentation.
		'''
		for ln in text.splitlines():
			self.write_line(ln)

	@abc.abstractmethod
	def write_heading(self, lvl: SectionLevel, heading: str) -> None:
		'''
		Write a heading.

		This object should *not* add an indentation depending on the section
		because if the indentation is increased the line width should be decreased
		in order to keep the line wrapping consistent.
		Wrapping lines is handled by :class:`confattr.utils.HelpFormatter`,
		i.e. before the text is passed to this object.
		It would be possible to use :class:`argparse.RawTextHelpFormatter` instead
		and handle line wrapping on a higher level but that would require
		to understand the help generated by argparse
		in order to know how far to indent a broken line.
		One of the trickiest parts would probably be to get the indentation of the usage right.
		Keep in mind that the term "usage" can differ depending on the language settings of the user.

		:param lvl: How to format the heading
		:param heading: The heading
		'''
		pass

	@abc.abstractmethod
	def write_command(self, cmd: str) -> None:
		'''
		Write a config file command.
		'''
		pass


class TextIOWriter(FormattedWriter):

	def __init__(self, f: 'typing.TextIO|None') -> None:
		self.f = f
		self.ignore_empty_lines = True

	def write_line_raw(self, ln: str) -> None:
		if self.ignore_empty_lines and not ln:
			return

		print(ln, file=self.f)
		self.ignore_empty_lines = False


class ConfigFileWriter(TextIOWriter):

	def __init__(self, f: 'typing.TextIO|None', prefix: str) -> None:
		super().__init__(f)
		self.prefix = prefix

	def write_command(self, cmd: str) -> None:
		self.write_line_raw(cmd)

	def write_line(self, ln: str) -> None:
		if ln:
			ln = self.prefix + ln

		self.write_line_raw(ln)

	def write_heading(self, lvl: SectionLevel, heading: str) -> None:
		self.write_line('')
		if lvl is SectionLevel.SECTION:
			self.write_line('=' * len(heading))
			self.write_line(heading)
			self.write_line('=' * len(heading))
		else:
			self.write_line(heading)
			self.write_line('-' * len(heading))

class HelpWriter(TextIOWriter):

	def write_line(self, ln: str) -> None:
		self.write_line_raw(ln)

	def write_heading(self, lvl: SectionLevel, heading: str) -> None:
		self.write_line('')
		if lvl is SectionLevel.SECTION:
			self.write_line(heading)
			self.write_line('=' * len(heading))
		else:
			self.write_line(heading)
			self.write_line('-' * len(heading))

	def write_command(self, cmd: str) -> None:
		pass


# ---------- internal exceptions ----------

class ParseException(Exception):

	'''
	This is raised and caught inside of :class:`ConfigFile` to communicate errors while parsing a config file.
	If you don't intend to subclass :class:`ConfigFile` you do not need to worry about this class.
	'''

class MultipleParseExceptions(Exception):

	'''
	This is raised and caught inside of :class:`ConfigFile` to communicate errors while parsing a config file where multiple settings are set in the same line.
	If you don't intend to subclass :class:`ConfigFile` you do not need to worry about this class.
	'''

	def __init__(self, exceptions: 'Sequence[ParseException]') -> None:
		super().__init__()
		self.exceptions = exceptions

	def __iter__(self) -> 'Iterator[ParseException]':
		return iter(self.exceptions)


# ---------- data types for **kw args ----------

if hasattr(typing, 'TypedDict'):  # python >= 3.8
	class SaveKwargs(typing.TypedDict, total=False):
		config_instances: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]]'
		ignore: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None'
		no_multi: bool
		comments: bool

	class ParseLineKwargs(typing.TypedDict, total=False):
		file_name: str
		line_number: int

	class ParseSplittedLineKwargs(ParseLineKwargs, total=False):
		line: 'Required[str]'


# ---------- ConfigFile class ----------

class ConfigFile:

	'''
	Read or write a config file.
	'''

	COMMENT = '#'
	COMMENT_PREFIXES = ('"', '#')
	ENTER_GROUP_PREFIX = '['
	ENTER_GROUP_SUFFIX = ']'


	#: Override the config file which is returned by :meth:`iter_config_paths`.
	#: You should set either this attribute or :attr:`config_directory` in your tests with :meth:`monkeypatch.setattr <pytest.MonkeyPatch.setattr>`.
	#: If the environment variable ``APPNAME_CONFIG_PATH`` is set this attribute is set to it's value in the constructor (where ``APPNAME`` is the value which is passed as :paramref:`appname <ConfigFile.appname>` to the constructor but in all upper case letters and hyphens and spaces replaced by underscores.)
	config_path: 'str|None' = None

	#: Override the config directory which is returned by :meth:`iter_user_site_config_paths`.
	#: You should set either this attribute or :attr:`config_path` in your tests with :meth:`monkeypatch.setattr <pytest.MonkeyPatch.setattr>`.
	#: If the environment variable ``APPNAME_CONFIG_DIRECTORY`` is set this attribute is set to it's value in the constructor (where ``APPNAME`` is the value which is passed as :paramref:`appname <ConfigFile.appname>` to the constructor but in all upper case letters and hyphens and spaces replaced by underscores.)
	config_directory: 'str|None' = None

	#: The name of the config file used by :meth:`iter_config_paths`.
	#: Can be changed with the environment variable ``APPNAME_CONFIG_NAME`` (where ``APPNAME`` is the value which is passed as :paramref:`appname <ConfigFile.appname>` to the constructor but in all upper case letters and hyphens and spaces replaced by underscores.).
	config_name = 'config'


	def __init__(self, *,
		notification_level: 'Config[NotificationLevel]|NotificationLevel' = NotificationLevel.ERROR,
		appname: str,
		authorname: 'str|None' = None,
		config_instances: 'dict[str, Config[typing.Any]]' = Config.instances,
		commands: 'Sequence[type[ConfigFileCommand]]|None' = None,
		formatter_class: 'type[argparse.HelpFormatter]' = HelpFormatter,
	) -> None:
		'''
		:param notification_level: Messages of a lower priority are *not* passed to the callback registered with :meth:`set_ui_callback`
		:param appname: The name of the application, required for generating the path of the config file if you use :meth:`load` or :meth:`save` and as prefix of environment variable names
		:param authorname: The name of the developer of the application, on MS Windows useful for generating the path of the config file if you use :meth:`load` or :meth:`save`
		:param config_instances: The Config instances to load or save, defaults to :attr:`Config.instances`
		:param commands: The :class:`ConfigFileCommand`s allowed in this config file, if this is :const:`None`: use the return value of :meth:`ConfigFileCommand.get_command_types`
		:param formatter_class: Is used to clean up doc strings and wrap lines in the help
		'''
		self.appname = appname
		self.authorname = authorname
		self.ui_notifier = UiNotifier(notification_level)
		self.config_instances = config_instances
		self.config_id: 'ConfigId|None' = None
		self.formatter_class = formatter_class
		self.env_variables: 'list[str]' = []

		if not appname:
			# Avoid an exception if appname is None.
			# Although mypy does not allow passing None directly
			# passing __package__ is (and should be) allowed.
			# And __package__ is None if the module is not part of a package.
			appname = ''
		self.envprefix = ''
		self.envprefix = self.get_env_name(appname + '_')
		envname = self.envprefix + 'CONFIG_PATH'
		self.env_variables.append(envname)
		if envname in os.environ:
			self.config_path = os.environ[envname]
		envname = self.envprefix + 'CONFIG_DIRECTORY'
		self.env_variables.append(envname)
		if envname in os.environ:
			self.config_directory = os.environ[envname]
		envname = self.envprefix + 'CONFIG_NAME'
		self.env_variables.append(envname)
		if envname in os.environ:
			self.config_name = os.environ[envname]

		if commands is None:
			commands = ConfigFileCommand.get_command_types()
		self.command_dict = {}
		self.commands = []
		for cmd_type in commands:
			cmd = cmd_type(self)
			self.commands.append(cmd)
			for name in cmd.get_names():
				self.command_dict[name] = cmd


	def set_ui_callback(self, callback: UiCallback) -> None:
		'''
		Register a callback to a user interface in order to show messages to the user like syntax errors or invalid values in the config file.

		Messages which occur before this method is called are stored and forwarded as soon as the callback is registered.

		:param ui_callback: A function to display messages to the user
		'''
		self.ui_notifier.set_ui_callback(callback)

	def get_app_dirs(self) -> 'appdirs.AppDirs':
		'''
		Create or get a cached `AppDirs <https://github.com/ActiveState/appdirs/blob/master/README.rst#appdirs-for-convenience>`_ instance with multipath support enabled.

		When creating a new instance, `platformdirs <https://pypi.org/project/platformdirs/>`_, `xdgappdirs <https://pypi.org/project/xdgappdirs/>`_ and `appdirs <https://pypi.org/project/appdirs/>`_ are tried, in that order.
		The first one installed is used.
		appdirs, the original of the two forks and the only one of the three with type stubs, is specified in pyproject.toml as a hard dependency so that at least one of the three should always be available.
		I am not very familiar with the differences but if a user finds that appdirs does not work for them they can choose to use an alternative with ``pipx inject appname xdgappdirs|platformdirs``.

		These libraries should respect the environment variables ``XDG_CONFIG_HOME`` and ``XDG_CONFIG_DIRS``.
		'''
		if not hasattr(self, '_appdirs'):
			try:
				import platformdirs  # type: ignore [import]  # this library is not typed and not necessarily installed, I am relying on it's compatibility with appdirs
				AppDirs = typing.cast('type[appdirs.AppDirs]', platformdirs.PlatformDirs)
			except ImportError:
				try:
					import xdgappdirs  # type: ignore [import]  # this library is not typed and not necessarily installed, I am relying on it's compatibility with appdirs
					AppDirs = typing.cast('type[appdirs.AppDirs]', xdgappdirs.AppDirs)
				except ImportError:
					AppDirs = appdirs.AppDirs

			self._appdirs = AppDirs(self.appname, self.authorname, multipath=True)

		return self._appdirs

	# ------- load -------

	def iter_user_site_config_paths(self) -> 'Iterator[str]':
		'''
		Iterate over all directories which are searched for config files, user specific first.

		The directories are based on :meth:`get_app_dirs`
		unless :attr:`config_directory` has been set.
		If :attr:`config_directory` has been set
		it's value is yielded and nothing else.
		'''
		if self.config_directory:
			yield self.config_directory
			return

		appdirs = self.get_app_dirs()
		yield from appdirs.user_config_dir.split(os.path.pathsep)
		yield from appdirs.site_config_dir.split(os.path.pathsep)

	def iter_config_paths(self) -> 'Iterator[str]':
		'''
		Iterate over all paths which are checked for config files, user specific first.

		Use this method if you want to tell the user where the application is looking for it's config file.
		The first existing file yielded by this method is used by :meth:`load`.

		The paths are generated by joining the directories yielded by :meth:`iter_user_site_config_paths` with
		:attr:`ConfigFile.config_name`.

		If :attr:`config_path` has been set this method yields that path instead and no other paths.
		'''
		if self.config_path:
			yield self.config_path
			return

		for path in self.iter_user_site_config_paths():
			yield os.path.join(path, self.config_name)

	def load(self, *, env: bool = True) -> None:
		'''
		Load the first existing config file returned by :meth:`iter_config_paths`.

		If there are several config files a user specific config file is preferred.
		If a user wants a system wide config file to be loaded, too, they can explicitly include it in their config file.
		:param env: If true: call :meth:`load_env` after loading the config file.
		'''
		for fn in self.iter_config_paths():
			if os.path.isfile(fn):
				self.load_file(fn)
				break

		if env:
			self.load_env()

	def load_env(self) -> None:
		'''
		Load settings from environment variables.
		The name of the environment variable belonging to a setting is generated with :meth:`get_env_name`.

		Environment variables not matching a setting or having an invalid value are reported with :meth:`self.ui_notifier.show_error() <UiNotifier.show_error>`.
		'''
		config_instances: 'dict[str, Config[object]]' = {}
		for key, instance in self.config_instances.items():
			name = self.get_env_name(key)
			if name in self.env_variables:
				self.ui_notifier.show_error(f'{instance.key} conflicts with environment variable {name}')
			elif name in config_instances:
				self.ui_notifier.show_error(f'{instance.key} and {config_instances[name].key} result in the same environment variable name: {name}')
			else:
				config_instances[name] = instance

		for name, value in os.environ.items():
			if not name.startswith(self.envprefix):
				continue
			if name in self.env_variables:
				continue

			if name in config_instances:
				instance = config_instances[name]
				try:
					instance.parse_and_set_value(config_id=None, value=value)
					self.ui_notifier.show_info(f'set {instance.key} to {instance.format_value(config_id=None)}')
				except ValueError as e:
					self.ui_notifier.show_error(f"{e} while trying to parse environment variable {name}='{value}'")
			else:
				self.ui_notifier.show_error(f"unknown environment variable {name}='{value}'")


	def get_env_name(self, key: str) -> str:
		'''
		Convert the key of a setting to the name of the corresponding environment variable.

		:return: An all upper case version of :paramref:`key` with all hyphens, dots and spaces replaced by underscores and :attr:`envprefix` prepended to the result. (:attr:`envprefix` is set in the constructor by first setting it to an empty str and then passing the value of :paramref:`appname <ConfigFile.appname>` to this method and appending an underscore.)
		'''
		out = key
		out = out.upper()
		for c in ' .-':
			out = out.replace(c, '_')
		out = self.envprefix + out
		return out

	def load_file(self, fn: str) -> None:
		'''
		Load a config file and change the :class:`Config` objects accordingly.

		Use :meth:`set_ui_callback` to get error messages which appeared while loading the config file.
		You can call :meth:`set_ui_callback` after this method without loosing any messages.

		:param fn: The file name of the config file (absolute or relative path)
		'''
		self.config_id = None
		self.load_without_resetting_config_id(fn)

	def load_without_resetting_config_id(self, fn: str) -> None:
		with open(fn, 'rt') as f:
			for lnno, ln in enumerate(f, 1):
				self.parse_line(line=ln, line_number=lnno, file_name=f.name)

	def parse_line(self, line: str, **kw: 'Unpack[ParseLineKwargs]') -> None:
		'''
		:param line: The line to be parsed
		:param line_number: The number of the line, used in error messages
		:param file_name: The name of the file from which ln was read (absolute or relative path), used in error messages and for relative imports

		:paramref:`line_number` and :paramref:`file_name` don't need to be passed in case :paramref:`ln` is not read from a config file but from a command line.

		:meth:`parse_error` is called if something goes wrong, e.g. invalid key or invalid value.
		'''
		ln = line.strip()
		if not ln:
			return
		if self.is_comment(ln):
			return
		if self.enter_group(ln):
			return

		ln_splitted = shlex.split(ln, comments=True)
		kw2 = typing.cast('ParseSplittedLineKwargs', kw)
		kw2['line'] = ln
		self.parse_splitted_line(ln_splitted, **kw2)

	def is_comment(self, ln: str) -> bool:
		'''
		Check if :paramref:`ln` is a comment.

		:param ln: The current line
		:return: :const:`True` if :paramref:`ln` is a comment
		'''
		for c in self.COMMENT_PREFIXES:
			if ln.startswith(c):
				return True
		return False

	def enter_group(self, ln: str) -> bool:
		'''
		Check if :paramref:`ln` starts a new group and set :attr:`config_id` if it does.

		:param ln: The current line
		:return: :const:`True` if :paramref:`ln` starts a new group
		'''
		if ln.startswith(self.ENTER_GROUP_PREFIX) and ln.endswith(self.ENTER_GROUP_SUFFIX):
			self.config_id = typing.cast(ConfigId, ln[len(self.ENTER_GROUP_PREFIX):-len(self.ENTER_GROUP_SUFFIX)])
			if self.config_id not in MultiConfig.config_ids:
				MultiConfig.config_ids.append(self.config_id)
			return True
		return False

	def parse_splitted_line(self, ln_splitted: 'Sequence[str]', **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		cmd_name = ln_splitted[0]

		try:
			if cmd_name in self.command_dict:
				cmd = self.command_dict[cmd_name]
			elif DEFAULT_COMMAND in self.command_dict:
				cmd = self.command_dict[DEFAULT_COMMAND]
			else:
				cmd = UnknownCommand(self)
			cmd.run(ln_splitted, **kw)
		except ParseException as e:
			self.parse_error(str(e), **kw)
		except MultipleParseExceptions as exceptions:
			for exc in exceptions:
				self.parse_error(str(exc), **kw)


	# ------- save -------

	def get_save_path(self) -> str:
		'''
		:return: The first existing and writable file returned by :meth:`iter_config_paths` or the first path if none of the files are existing and writable.
		'''
		paths = tuple(self.iter_config_paths())
		for fn in paths:
			if os.path.isfile(fn) and os.access(fn, os.W_OK):
				return fn

		return paths[0]

	def save(self,
		**kw: 'Unpack[SaveKwargs]',
	) -> str:
		'''
		Save the current values of all settings to the file returned by :meth:`get_save_path`.
		Directories are created as necessary.

		:param config_instances: Do not save all settings but only those given. If this is a :class:`list` they are written in the given order. If this is a :class:`set` they are sorted by their keys.
		:param ignore: Do not write these settings to the file.
		:param no_multi: Do not write several sections. For :class:`MultiConfig` instances write the default values only.
		:param comments: Write comments with allowed values and help.
		:return: The path to the file which has been written
		'''
		fn = self.get_save_path()
		# "If, when attempting to write a file, the destination directory is non-existent an attempt should be made to create it with permission 0700.
		#  If the destination directory exists already the permissions should not be changed."
		# https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
		os.makedirs(os.path.dirname(fn), exist_ok=True, mode=0o0700)
		self.save_file(fn, **kw)
		return fn

	def save_file(self,
		fn: str,
		**kw: 'Unpack[SaveKwargs]'
	) -> None:
		'''
		Save the current values of all settings to a specific file.

		:param fn: The name of the file to write to. If this is not an absolute path it is relative to the current working directory.
		:raises FileNotFoundError: if the directory does not exist

		For an explanation of the other parameters see :meth:`save`.
		'''
		with open(fn, 'wt') as f:
			self.save_to_open_file(f, **kw)


	def save_to_open_file(self,
		f: typing.TextIO,
		**kw: 'Unpack[SaveKwargs]',
	) -> None:
		'''
		Save the current values of all settings to a file-like object
		by creating a :class:`ConfigFileWriter` object and calling :meth:`save_to_writer`.

		:param f: The file to write to

		For an explanation of the other parameters see :meth:`save`.
		'''
		writer = ConfigFileWriter(f, prefix=self.COMMENT + ' ')
		self.save_to_writer(writer, **kw)

	def save_to_writer(self, writer: FormattedWriter, **kw: 'Unpack[SaveKwargs]') -> None:
		'''
		Save the current values of all settings.

		Ensure that all keyword arguments are passed with :meth:`set_save_default_arguments`.
		Iterate over all :class:`ConfigFileCommand` objects in :attr:`self.commands` and do for each of them:

		- set :attr:`~ConfigFileCommand.should_write_heading` to :obj:`True` if :python:`getattr(cmd.save, 'implemented', True)` is true for two or more of those commands or to :obj:`False` otherwise
		- call :meth:`~ConfigFileCommand.save`
		'''
		self.set_save_default_arguments(kw)
		commands = self.commands
		write_headings = len(tuple(cmd for cmd in commands if getattr(cmd.save, 'implemented', True))) >= 2
		for cmd in commands:
			cmd.should_write_heading = write_headings
			cmd.save(writer, **kw)

	def set_save_default_arguments(self, kw: 'SaveKwargs') -> None:
		'''
		Ensure that all arguments are given in :paramref:`kw`.
		'''
		kw.setdefault('config_instances', set(self.config_instances.values()))
		kw.setdefault('ignore', None)
		kw.setdefault('no_multi', False)
		kw.setdefault('comments', True)


	def quote(self, val: str) -> str:
		'''
		Quote a value if necessary so that it will be interpreted as one argument.

		The default implementation calls :func:`readable_quote`.
		'''
		return readable_quote(val)

	def write_config_id(self, writer: FormattedWriter, config_id: ConfigId) -> None:
		'''
		Start a new group in the config file so that all following commands refer to the given :paramref:`config_id`.
		'''
		writer.write_command(self.ENTER_GROUP_PREFIX + config_id + self.ENTER_GROUP_SUFFIX)

	def get_help_config_id(self) -> str:
		'''
		:return: A help how to use :class:`MultiConfig`. The return value still needs to be cleaned with :meth:`inspect.cleandoc`.
		'''
		return f'''
			You can specify the object that a value shall refer to by inserting the line `{self.ENTER_GROUP_PREFIX}config-id{self.ENTER_GROUP_SUFFIX}` above.
			`config-id` must be replaced by the corresponding identifier for the object.
		'''


	# ------- help -------

	def write_help(self, writer: FormattedWriter) -> None:
		import platform
		formatter = self.create_formatter()
		writer.write_lines('The first existing file of the following paths is loaded:')
		for path in self.iter_config_paths():
			writer.write_line('- %s' % path)

		writer.write_line('')
		writer.write_line('This can be influenced with the following environment variables:')
		if platform.system() == 'Linux':
			writer.write_line('- XDG_CONFIG_HOME')
			writer.write_line('- XDG_CONFIG_DIRS')
		for env in self.env_variables:
			writer.write_line(f'- {env}')

		writer.write_line('')
		writer.write_lines(formatter.format_text(f'''\
You can also use environment variables to change the values of the settings listed under `set` command.
The corresponding environment variable name is the name of the setting in all upper case letters
with dots, hypens and spaces replaced by underscores and prefixed with "{self.envprefix}".'''))

		writer.write_lines(formatter.format_text('Lines in the config file which start with a %s are ignored.' % ' or '.join('`%s`' % c for c in self.COMMENT_PREFIXES)))

		writer.write_lines('The config file may contain the following commands:')
		for cmd in self.commands:
			names = '|'.join(cmd.get_names())
			writer.write_heading(SectionLevel.SECTION, names)
			writer.write_lines(cmd.get_help())

	def create_formatter(self) -> HelpFormatterWrapper:
		return HelpFormatterWrapper(self.formatter_class)

	def get_help(self) -> str:
		'''
		A convenience wrapper around :meth:`write_help`
		to return the help as a str instead of writing it to a file.

		This uses :class:`HelpWriter`.
		'''
		doc = io.StringIO()
		self.write_help(HelpWriter(doc))
		# The generated help ends with a \n which is implicitly added by print.
		# If I was writing to stdout or a file that would be desired.
		# But if I return it as a string and then print it, the print adds another \n which would be too much.
		# Therefore I am stripping the trailing \n.
		return doc.getvalue().rstrip('\n')


	# ------- error handling -------

	def parse_error(self, msg: str, **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		'''
		Is called if something went wrong while trying to load a config file.

		This method is called when a :class:`ParseException` or :class:`MultipleParseExceptions` is caught.
		This method compiles the given information into an error message and calls :meth:`self.ui_notifier.show_error() <UiNotifier.show_error>`.

		:param msg: The error message
		:param line: The line where the error occured
		:param line_number: The number of the line
		:param file_name: The name of the config file from which the line has been read
		'''
		ln = kw['line']
		lnno = kw.get('line_number', None)
		if lnno is not None:
			lnref = 'line %s' % lnno
		else:
			lnref = 'line'
		msg +=  f' while trying to parse {lnref} {ln!r}'
		self.ui_notifier.show_error(msg)


# ---------- base classes for commands which can be used in config files ----------

class ConfigFileCommand(abc.ABC):

	'''
	An abstract base class for commands which can be used in a config file.

	Subclasses must implement the :meth:`run` method which is called when :class:`ConfigFile` is loading a file.
	Subclasses should contain a doc string so that :meth:`get_help` can provide a description to the user.
	Subclasses may set the :attr:`name` and :attr:`aliases` attributes to change the output of :meth:`get_name` and :meth:`get_names`.

	All subclasses are remembered and can be retrieved with :meth:`get_command_types`.
	They are instantiated in the constructor of :class:`ConfigFile`.
	'''

	#: The name which is used in the config file to call this command. Use an empty string to define a default command which is used if an undefined command is encountered. If this is not set :meth:`get_name` returns the name of this class in lower case letters and underscores replaced by hyphens.
	name: str

	#: Alternative names which can be used in the config file.
	aliases: 'tuple[str, ...]|list[str]'

	#: A description which may be used by an in-app help. If this is not set :meth:`get_help` uses the doc string instead.
	help: str

	#: If a config file contains only a single section it makes no sense to write a heading for it. This attribute is set by :meth:`ConfigFile.save_to_writer` if there are several commands which implement the :meth:`save` method. If you implement :meth:`save` and this attribute is set then :meth:`save` should write a section header. If :meth:`save` writes several sections it should always write the headings regardless of this attribute.
	should_write_heading: bool = False

	_subclasses: 'list[type[ConfigFileCommand]]' = []
	_used_names: 'set[str]' = set()

	@classmethod
	def get_command_types(cls) -> 'tuple[type[ConfigFileCommand], ...]':
		'''
		:return: All subclasses of :class:`ConfigFileCommand` which have not been deleted with :meth:`delete_command_type`
		'''
		return tuple(cls._subclasses)

	@classmethod
	def delete_command_type(cls, cmd: 'type[ConfigFileCommand]') -> None:
		'''
		Delete :paramref:`cmd` so that it is not returned anymore by :meth:`get_command_types` and that it's name can be used by another command.
		Do nothing if :paramref:`cmd` has already been deleted.
		'''
		if cmd in cls._subclasses:
			cls._subclasses.remove(cmd)
			for name in cmd.get_names():
				cls._used_names.remove(name)

	@classmethod
	def __init_subclass__(cls, replace: bool = False, abstract: bool = False) -> None:
		'''
		Add the new subclass to :attr:`subclass`.

		:param replace: Set :attr:`name` and :attr:`aliases` to the values of the parent class if they are not set explicitly, delete the parent class with :meth:`delete_command_type` and replace any commands with the same name
		:param abstract: This class is a base class for the implementation of other commands and shall *not* be returned by :meth:`get_command_types`
		:raises ValueError: if the name or one of it's aliases is already in use and :paramref:`replace` is not true
		'''
		if replace:
			parent_commands = [parent for parent in cls.__bases__ if issubclass(parent, ConfigFileCommand)]

			# set names of this class to that of the parent class(es)
			parent = parent_commands[0]
			if 'name' not in cls.__dict__:
				cls.name = parent.get_name()
			if 'aliases' not in cls.__dict__:
				cls.aliases = list(parent.get_names())[1:]
				for parent in parent_commands[1:]:
					cls.aliases.extend(parent.get_names())

			# remove parent class from the list of commands to be loaded or saved
			for parent in parent_commands:
				if issubclass(parent, ConfigFileCommand):
					cls.delete_command_type(parent)

		if not abstract:
			cls._subclasses.append(cls)
			for name in cls.get_names():
				if name in cls._used_names and not replace:
					raise ValueError('duplicate command name %r' % name)
				cls._used_names.add(name)

	@classmethod
	def get_name(cls) -> str:
		'''
		:return: The name which is used in config file to call this command.
		
		If :attr:`name` is set it is returned as it is.
		Otherwise a name is generated based on the class name.
		'''
		if 'name' in cls.__dict__:
			return cls.name
		return cls.__name__.lower().replace("_", "-")

	@classmethod
	def get_names(cls) -> 'Iterator[str]':
		'''
		:return: Several alternative names which can be used in a config file to call this command.
		
		The first one is always the return value of :meth:`get_name`.
		If :attr:`aliases` is set it's items are yielded afterwards.

		If one of the returned items is the empty string this class is the default command
		and :meth:`run` will be called if an undefined command is encountered.
		'''
		yield cls.get_name()
		if 'aliases' in cls.__dict__:
			for name in cls.aliases:
				yield name

	def __init__(self, config_file: ConfigFile) -> None:
		self.config_file = config_file
		self.ui_notifier = config_file.ui_notifier

	@abc.abstractmethod
	def run(self, ln: 'Sequence[str]', **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		'''
		Process one line which has been read from a config file

		:raises ParseException: if there is an error in the line (e.g. invalid syntax)
		:raises MultipleParseExceptions: if there are several errors in the same line
		'''
		raise NotImplementedError()

	def create_formatter(self) -> HelpFormatterWrapper:
		return self.config_file.create_formatter()

	def get_help_attr_or_doc_str(self) -> str:
		'''
		:return: The :attr:`help` attribute or the doc string if :attr:`help` has not been set, cleaned up with :meth:`inspect.cleandoc`.
		'''
		if hasattr(self, 'help'):
			doc = self.help
		elif self.__doc__:
			doc = self.__doc__
		else:
			doc = ''

		return inspect.cleandoc(doc)

	def add_help_to(self, formatter: HelpFormatterWrapper) -> None:
		'''
		Add the return value of :meth:`get_help_attr_or_doc_str` to :paramref:`formatter`.
		'''
		formatter.add_text(self.get_help_attr_or_doc_str())

	def get_help(self) -> str:
		'''
		:return: A help text which can be presented to the user.

		This is generated by creating a formatter with :meth:`create_formatter`,
		adding the help to it with :meth:`add_help_to` and
		stripping trailing new line characters from the result of :meth:`HelpFormatterWrapper.format_help`.

		Most likely you don't want to override this method but :meth:`add_help_to` instead.
		'''
		formatter = self.create_formatter()
		self.add_help_to(formatter)
		return formatter.format_help().rstrip('\n')

	def save(self,
		writer: FormattedWriter,
		**kw: 'Unpack[SaveKwargs]',
	) -> None:
		'''
		Write as many calls to this command as necessary to the config file in order to create the current state.
		There is the :attr:`config_file` attribute (which was passed to the constructor) which you can use to:

		- quote arguments with :meth:`ConfigFile.quote`
		- get the comment character :attr:`ConfigFile.COMMENT`
		- call :attr:`ConfigFile.write_config_id`

		The default implementation does nothing.
		'''
		pass

	save.implemented = False  # type: ignore [attr-defined]


class ArgumentParser(argparse.ArgumentParser):

	def error(self, message: str) -> 'typing.NoReturn':
		raise ParseException(message)

class ConfigFileArgparseCommand(ConfigFileCommand, abstract=True):

	'''
	An abstract subclass of :class:`ConfigFileCommand` which uses :mod:`argparse` to make parsing and providing help easier.

	You must implement the class method :meth:`init_parser` to add the arguments to :attr:`parser`.
	Instead of :meth:`run` you must implement :meth:`run_parsed`.
	You don't need to add a usage or the possible arguments to the doc string as :mod:`argparse` will do that for you.
	You should, however, still give a description what this command does in the doc string.

	You may specify :attr:`ConfigFileCommand.name`, :attr:`ConfigFileCommand.aliases` and :meth:`ConfigFileCommand.save` like for :class:`ConfigFileCommand`.
	'''

	def __init__(self, config_file: ConfigFile) -> None:
		super().__init__(config_file)
		self._names = set(self.get_names())
		self.parser = ArgumentParser(prog=self.get_name(), description=self.get_help_attr_or_doc_str(), add_help=False, formatter_class=self.config_file.formatter_class)
		self.init_parser(self.parser)

	@abc.abstractmethod
	def init_parser(self, parser: ArgumentParser) -> None:
		'''
		:param parser: The parser to add arguments to. This is the same object like :attr:`parser`.

		This is an abstract method which must be implemented by subclasses.
		Use :meth:`ArgumentParser.add_argument` to add arguments to :paramref:`parser`.
		'''
		pass

	def get_help(self) -> str:
		'''
		Creates a help text which can be presented to the user by calling :meth:`parser.format_help`.
		The return value of :meth:`ConfigFileCommand.write_help` has been passed as :paramref:`description` to the constructor of :class:`ArgumentParser`, therefore :attr:`help`/the doc string are included as well.
		'''
		return self.parser.format_help().rstrip('\n')

	def run(self, ln: 'Sequence[str]', **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		# if the line was empty this method should not be called but an empty line should be ignored either way
		if not ln:
			return
		# ln[0] does not need to be in self._names if this is the default command, i.e. if '' in self._names
		if ln[0] in self._names:
			ln = ln[1:]
		args = self.parser.parse_args(ln)
		self.run_parsed(args)

	@abc.abstractmethod
	def run_parsed(self, args: argparse.Namespace) -> None:
		'''
		This is an abstract method which must be implemented by subclasses.
		'''
		pass


# ---------- implementations of commands which can be used in config files ----------

class Set(ConfigFileCommand):

	r'''
	usage: set key1=val1 [key2=val2 ...] \\
	       set key [=] val

	Change the value of a setting.

	In the first form set takes an arbitrary number of arguments, each argument sets one setting.
	This has the advantage that several settings can be changed at once.
	That is useful if you want to bind a set command to a key and process that command with ConfigFile.parse_line() if the key is pressed.

	In the second form set takes two arguments, the key and the value. Optionally a single equals character may be added in between as third argument.
	This has the advantage that key and value are separated by one or more spaces which can improve the readability of a config file.
	'''

	#: The separator which is used between a key and it's value
	KEY_VAL_SEP = '='

	#: Help for data types. This is used by :meth:`get_help_for_data_types`. Change this with :meth:`set_help_for_type`.
	help_for_types = {
		str : 'A text. If it contains spaces it must be wrapped in single or double quotes.',
		int : '''\
			An integer number in python 3 syntax, as decimal (e.g. 42), hexadecimal (e.g. 0x2a), octal (e.g. 0o52) or binary (e.g. 0b101010).
			Leading zeroes are not permitted to avoid confusion with python 2's syntax for octal numbers.
			It is permissible to group digits with underscores for better readability, e.g. 1_000_000.''',
		#bool,
		float : 'A floating point number in python syntax, e.g. 23, 1.414, -1e3, 3.14_15_93.',
	}


	# ------- load -------

	def run(self, cmd: 'Sequence[str]', **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		'''
		Call :meth:`set_multiple` if the first argument contains :attr:`KEY_VAL_SEP` otherwise :meth:`set_with_spaces`.

		:raises ParseException: if something is wrong (no arguments given, invalid syntax, invalid key, invalid value)
		'''
		if len(cmd) < 2:
			raise ParseException('no settings given')

		if self.KEY_VAL_SEP in cmd[1]:  # cmd[0] is the name of the command, cmd[1] is the first argument
			self.set_multiple(cmd)
		else:
			self.set_with_spaces(cmd)

	def set_with_spaces(self, cmd: 'Sequence[str]') -> None:
		'''
		Process one line of the format ``set key [=] value``

		:raises ParseException: if something is wrong (invalid syntax, invalid key, invalid value)
		'''
		n = len(cmd)
		if n == 3:
			cmdname, key, value = cmd
			self.parse_key_and_set_value(key, value)
		elif n == 4:
			cmdname, key, sep, value = cmd
			if sep != self.KEY_VAL_SEP:
				raise ParseException(f'seperator between key and value should be {self.KEY_VAL_SEP}, not {sep!r}')
			self.parse_key_and_set_value(key, value)
		elif n == 2:
			raise ParseException(f'missing value or missing {self.KEY_VAL_SEP}')
		else:
			assert n >= 5
			raise ParseException(f'too many arguments given or missing {self.KEY_VAL_SEP} in first argument')

	def set_multiple(self, cmd: 'Sequence[str]') -> None:
		'''
		Process one line of the format ``set key=value [key2=value2 ...]``

		:raises MultipleParseExceptions: if something is wrong (invalid syntax, invalid key, invalid value)
		'''
		exceptions = []
		for arg in cmd[1:]:
			if not self.KEY_VAL_SEP in arg:
				raise ParseException(f'missing {self.KEY_VAL_SEP} in {arg!r}')
			key, value = arg.split(self.KEY_VAL_SEP, 1)
			try:
				self.parse_key_and_set_value(key, value)
			except ParseException as e:
				exceptions.append(e)
		if exceptions:
			raise MultipleParseExceptions(exceptions)

	def parse_key_and_set_value(self, key: str, value: str) -> None:
		'''
		Find the corresponding :class:`Config` instance for :paramref:`key` and pass it to :meth:`parse_and_set_value`.

		:raises ParseException: if key is invalid or :meth:`parse_and_set_value` raises a :class:`ValueError`
		'''
		if key not in self.config_file.config_instances:
			raise ParseException(f'invalid key {key!r}')

		instance = self.config_file.config_instances[key]
		try:
			self.parse_and_set_value(instance, value)
		except ValueError as e:
			raise ParseException(str(e))

	def parse_and_set_value(self, instance: Config[typing.Any], value: str) -> None:
		'''
		Parse the given value str and assign it to the given instance by calling :meth:`Config.parse_and_set_value` with :attr:`ConfigFile.config_id` of :attr:`config_file`.
		Afterwards call :meth:`UiNotifier.show_info`.
		'''
		instance.parse_and_set_value(self.config_file.config_id, value)
		self.ui_notifier.show_info(f'set {instance.key} to {instance.format_value(self.config_file.config_id)}')


	# ------- save -------

	def iter_config_instances_to_be_saved(self, **kw: 'Unpack[SaveKwargs]') -> 'Iterator[Config[object]]':
		'''
		:param config_instances: The settings to consider
		:param ignore: Skip these settings

		Iterate over all given :paramref:`config_instances` and expand all :class:`DictConfig` instances into the :class:`Config` instances they consist of.
		Sort the resulting list if :paramref:`config_instances` is not a :class:`list` or a :class:`tuple`.
		Yield all :class:`Config` instances which are not (directly or indirectly) contained in :paramref:`ignore` and where :meth:`Config.wants_to_be_exported` returns true.
		'''
		config_instances = kw['config_instances']
		ignore = kw['ignore']

		config_keys = []
		for c in config_instances:
			if isinstance(c, DictConfig):
				config_keys.extend(sorted(c.iter_keys()))
			else:
				config_keys.append(c.key)
		if not isinstance(config_instances, (list, tuple)):
			config_keys = sorted(config_keys)

		if ignore is not None:
			tmp = set()
			for c in tuple(ignore):
				if isinstance(c, DictConfig):
					tmp |= set(c._values.values())
				else:
					tmp.add(c)
			ignore = tmp

		for key in config_keys:
			instance = self.config_file.config_instances[key]
			if not instance.wants_to_be_exported():
				continue

			if ignore is not None and instance in ignore:
				continue

			yield instance

	def save(self, writer: FormattedWriter, **kw: 'Unpack[SaveKwargs]') -> None:
		'''
		:param writer: The file to write to
		:param bool no_multi: If true: treat :class:`MultiConfig` instances like normal :class:`Config` instances and only write their default value. If false: Separate :class:`MultiConfig` instances and print them once for every :attr:`MultiConfig.config_ids`.
		:param bool comments: If false: don't write help for data types

		Iterate over all :class:`Config` instances with :meth:`iter_config_instances_to_be_saved`,
		split them into normal :class:`Config` and :class:`MultiConfig` and write them with :meth:`save_config_instance`.
		But before that set :attr:`last_name` to None (which is used by :meth:`write_config_help`)
		and write help for data types based on :meth:`get_help_for_data_types`.
		'''
		no_multi = kw['no_multi']
		comments = kw['comments']

		if self.should_write_heading:
			writer.write_heading(SectionLevel.SECTION, 'Settings')

		self.last_name: 'str|None' = None

		config_instances = list(self.iter_config_instances_to_be_saved(**kw))
		if comments:
			type_help = self.get_help_for_data_types(config_instances)
			if type_help:
				writer.write_heading(SectionLevel.SUB_SECTION, 'Data types')
				writer.write_lines(type_help)

		multi_configs = []
		for instance in config_instances:
			if not no_multi and isinstance(instance, MultiConfig):
				multi_configs.append(instance)
				continue

			self.save_config_instance(writer, instance, config_id=None, **kw)

		if multi_configs:
			for config_id in MultiConfig.config_ids:
				writer.write_line('')
				self.config_file.write_config_id(writer, config_id)
				for instance in multi_configs:
					self.save_config_instance(writer, instance, config_id, **kw)

	def save_config_instance(self, writer: FormattedWriter, instance: 'Config[object]', config_id: 'ConfigId|None', **kw: 'Unpack[SaveKwargs]') -> None:
		'''
		:param writer: The file to write to
		:param instance: The config value to be saved
		:param config_id: Which value to be written in case of a :class:`MultiConfig`, should be :const:`None` for a normal :class:`Config` instance
		:param bool comments: If true: call :meth:`write_config_help`

		Convert the :class:`Config` instance into a value str with :meth:`format_value`,
		wrap it in quotes if necessary with :meth:`config_file.quote` and write it to :paramref:`writer`.
		'''
		if kw['comments']:
			self.write_config_help(writer, instance)
		value = self.format_value(instance, config_id)
		value = self.config_file.quote(value)
		ln = f'{self.get_name()} {instance.key} = {value}'
		writer.write_command(ln)

	def format_value(self, instance: Config[typing.Any], config_id: 'ConfigId|None') -> str:
		'''
		:param instance: The config value to be saved
		:param config_id: Which value to be written in case of a :class:`MultiConfig`, should be :const:`None` for a normal :class:`Config` instance
		:return: A str representation to be written to the config file

		Convert the value of the :class:`Config` instance into a str with :meth:`Config.format_value`.
		'''
		return instance.format_value(config_id)

	def write_config_help(self, writer: FormattedWriter, instance: Config[typing.Any], *, group_dict_configs: bool = True) -> None:
		'''
		:param writer: The output to write to
		:param instance: The config value to be saved

		Write a comment which explains the meaning and usage of this setting
		based on :meth:`Config.format_allowed_values_or_type` and :attr:`Config.help`.

		Use :attr:`last_name` to write the help only once for all :class:`Config` instances belonging to the same :class:`DictConfig` instance.
		'''
		if group_dict_configs and instance.parent is not None:
			name = instance.parent.key_prefix
		else:
			name = instance.key
		if name == self.last_name:
			return

		formatter = HelpFormatterWrapper(self.config_file.formatter_class)
		writer.write_heading(SectionLevel.SUB_SECTION, name)
		writer.write_lines(formatter.format_text(instance.format_allowed_values_or_type()).rstrip())
		#if instance.unit:
		#	writer.write_line('unit: %s' % instance.unit)
		if isinstance(instance.help, dict):
			for key, val in instance.help.items():
				key_name = instance.format_any_value(key)
				val = inspect.cleandoc(val)
				writer.write_lines(formatter.format_item(bullet=key_name+': ', text=val).rstrip())
		elif isinstance(instance.help, str):
			writer.write_lines(formatter.format_text(inspect.cleandoc(instance.help)).rstrip())

		self.last_name = name


	@classmethod
	def set_help_for_type(cls, t: 'type[object]', help_text: str) -> None:
		'''
		:meth:`get_help_for_data_types` is used by :meth:`save` and :meth:`get_help`.
		Usually it uses the :attr:`help` attribute of the class.
		But if the class does not have a :attr:`help` attribute or if you want a different help text
		you can set the help with this method.

		:param t: The type for which you want to specify a help
		:param help_text: The help for :paramref:`t`. It is cleaned up in :meth:`get_help_for_data_types` with :meth:`HelpFormatterWrapper.format_text` depending on :attr:`self.config_file.formatter_class`.
		'''
		cls.help_for_types[t] = help_text

	def get_data_type_name_to_help_map(self, config_instances: 'Iterable[Config[object]]') -> 'dict[str, str]':
		'''
		:param config_instances: All config values to be saved
		:return: A dictionary containing the type names as keys and the help as values

		The returned dictionary contains the help for all data types except enumerations
		which occur in :paramref:`config_instances`.
		The help is gathered from the :attr:`help` attribute of the type
		or the str registered with :meth:`set_help_for_type`.
		'''
		help_text: 'dict[str, str]' = {}
		for instance in config_instances:
			t = instance.type if instance.type != list else instance.item_type
			name = getattr(t, 'type_name', t.__name__)

			if t in self.help_for_types:
				h = self.help_for_types[t]
			elif hasattr(t, 'help'):
				h = t.help
			elif issubclass(t, enum.Enum) or t is bool:
				# an enum does not need a help if the values have self explanatory names
				# bool is treated like an enum
				continue
			else:
				raise AttributeError('No help given for {cmdname} ({classname}). Please specify it as help attribute or with set_help_for_type.'.format(cmdname=name, classname=t.__name__))

			help_text[name] = inspect.cleandoc(h)

		return help_text

	def add_help_for_data_types(self, formatter: HelpFormatterWrapper, config_instances: 'Iterable[Config[object]]') -> None:
		help_map = self.get_data_type_name_to_help_map(config_instances)
		if not help_map:
			return

		for name in sorted(help_map.keys()):
			formatter.add_start_section(name)
			formatter.add_text(help_map[name])
			formatter.add_end_section()

	def get_help_for_data_types(self, config_instances: 'Iterable[Config[object]]') -> str:
		formatter = self.create_formatter()
		self.add_help_for_data_types(formatter, config_instances)
		return formatter.format_help().rstrip('\n')

	# ------- help -------

	def add_help_to(self, formatter: HelpFormatterWrapper) -> None:
		super().add_help_to(formatter)

		kw: 'SaveKwargs' = {}
		self.config_file.set_save_default_arguments(kw)
		config_instances = list(self.iter_config_instances_to_be_saved(**kw))
		self.last_name = None

		formatter.add_start_section('data types')
		self.add_help_for_data_types(formatter, config_instances)
		formatter.add_end_section()

		normal_configs = []
		multi_configs = []
		for instance in config_instances:
			if isinstance(instance, MultiConfig):
				multi_configs.append(instance)
			else:
				normal_configs.append(instance)

		if normal_configs:
			formatter.add_start_section('application wide settings')
			for instance in normal_configs:
				self.add_config_help(formatter, instance)
			formatter.add_end_section()

		if multi_configs:
			formatter.add_start_section('settings which can have different values for different objects')
			formatter.add_text(inspect.cleandoc(self.config_file.get_help_config_id()))
			for instance in multi_configs:
				self.add_config_help(formatter, instance)
			formatter.add_end_section()

	def add_config_help(self, formatter: HelpFormatterWrapper, instance: Config[typing.Any]) -> None:
		formatter.add_start_section(instance.key)
		formatter.add_text(instance.format_allowed_values_or_type())
		#if instance.unit:
		#	formatter.add_item(bullet='unit: ', text=instance.unit)
		if isinstance(instance.help, dict):
			for key, val in instance.help.items():
				key_name = instance.format_any_value(key)
				val = inspect.cleandoc(val)
				formatter.add_item(bullet=key_name+': ', text=val)
		elif isinstance(instance.help, str):
			formatter.add_text(inspect.cleandoc(instance.help))
		formatter.add_end_section()


class Include(ConfigFileArgparseCommand):

	'''
	Load another config file.

	This is useful if a config file is getting so big that you want to split it up
	or if you want to have different config files for different use cases which all include the same standard config file to avoid redundancy
	or if you want to bind several commands to one key which executes one command with ConfigFile.parse_line().

	By default the loaded config file starts with which ever config id is currently active.
	This is useful if you want to use the same values for several config ids:
	Write the set commands without a config id to a separate config file and include this file for every config id where these settings shall apply.

	After the include the config id is reset to the config id which was active at the beginning of the include
	because otherwise it might lead to confusion if the config id is changed in the included config file.
	'''

	def init_parser(self, parser: ArgumentParser) -> None:
		parser.add_argument('path', help='The config file to load. Slashes are replaced with the directory separator appropriate for the current operating system.')
		group = parser.add_mutually_exclusive_group()
		group.add_argument('--reset-config-id-before', action='store_true', help='Ignore any config id which might be active when starting the include')
		group.add_argument('--no-reset-config-id-after', action='store_true', help='Treat the included lines as if they were written in the same config file instead of the include command')

		self.nested_includes: 'list[str]' = []

	def run(self, cmd: 'Sequence[str]', **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		self.file_name = kw.get('file_name', None)
		super().run(cmd, **kw)

	def run_parsed(self, args: argparse.Namespace) -> None:
		fn_imp = args.path
		fn_imp = fn_imp.replace('/', os.path.sep)
		fn_imp = os.path.expanduser(fn_imp)
		if not os.path.isabs(fn_imp):
			fn = self.file_name
			if fn is None:
				fn = self.config_file.get_save_path()
			fn_imp = os.path.join(os.path.dirname(os.path.abspath(fn)), fn_imp)

		if fn_imp in self.nested_includes:
			raise ParseException(f'circular include of file {fn_imp!r}')
		if not os.path.isfile(fn_imp):
			raise ParseException(f'no such file {fn_imp!r}')

		self.nested_includes.append(fn_imp)

		if args.no_reset_config_id_after:
			self.config_file.load_without_resetting_config_id(fn_imp)
		elif args.reset_config_id_before:
			config_id = self.config_file.config_id
			self.config_file.load_file(fn_imp)
			self.config_file.config_id = config_id
		else:
			config_id = self.config_file.config_id
			self.config_file.load_without_resetting_config_id(fn_imp)
			self.config_file.config_id = config_id

		assert self.nested_includes[-1] == fn_imp
		del self.nested_includes[-1]


class UnknownCommand(ConfigFileCommand, abstract=True):

	name = DEFAULT_COMMAND

	def run(self, splitted_line: 'Sequence[str]', **kw: 'Unpack[ParseSplittedLineKwargs]') -> None:
		raise ParseException('unknown command %r' % splitted_line[0])
