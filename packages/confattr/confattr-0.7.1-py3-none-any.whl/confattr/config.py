#!./runmodule.sh

import enum
import typing
from collections.abc import Iterable, Iterator, Container, Sequence


VALUE_TRUE = 'true'
VALUE_FALSE = 'false'
VALUE_NONE = 'none'
VALUE_AUTO = 'auto'

TYPES_REQUIRING_UNIT = {int, float}
CONTAINER_TYPES = {list}


ConfigId = typing.NewType('ConfigId', str)

T = typing.TypeVar('T')
T_KEY = typing.TypeVar('T_KEY')
T1 = typing.TypeVar('T1')


class Config(typing.Generic[T]):

	'''
	Each instance of this class represents a setting which can be changed in a config file.

	This class implements the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`_ to return :attr:`value` if an instance of this class is accessed as an instance attribute.
	If you want to get this object you need to access it as a class attribute.
	'''

	_Self = typing.TypeVar('_Self', bound='Config[T]')

	LIST_SEP = ','

	#: A mapping of all :class:`Config` instances. The key in the mapping is the :attr:`key` attribute. The value is the :class:`Config` instance. New :class:`Config` instances add themselves automatically in their constructor.
	instances: 'dict[str, Config[typing.Any]]' = {}

	default_config_id = ConfigId('general')

	#: The value of this setting.
	value: 'T'

	#: The unit of :attr:`value` if :attr:`value` is a number.
	unit: 'str|None'

	#: A description of this setting or a description for each allowed value.
	help: 'str|dict[T, str]|None'

	#: The values which are allowed for this setting. Trying to set this setting to a different value in the config file is considered an error. If you set this setting in the program the value is *not* checked.
	allowed_values: 'Sequence[T]|None'

	def __init__(self,
		key: str,
		default: T, *,
		help: 'str|dict[T, str]|None' = None,
		unit: 'str|None' = None,
		parent: 'DictConfig[typing.Any, T]|None' = None,
		allowed_values: 'Sequence[T]|None' = None,
	):
		'''
		:param key: The name of this setting in the config file
		:param default: The default value of this setting
		:param help: A description of this setting
		:param unit: The unit of an int or float value
		:param parent: Applies only if this is part of a :class:`DictConfig`
		:param allowed_values: The possible values this setting can have. Values read from a config file or an environment variable are checked against this. The :paramref:`default` value is *not* checked.

		:const:`T` can be one of:
			* :class:`str`
			* :class:`int`
			* :class:`float`
			* :class:`bool`
			* a subclass of :class:`enum.Enum` (the value used in the config file is the name in lower case letters with hyphens instead of underscores)
			* a class where :meth:`__str__` returns a string representation which can be passed to the constructor to create an equal object. \
			  A help which is written to the config file must be provided as a str in the class attribute :attr:`help` or by calling :meth:`Set.set_help_for_type`. \
			  If that class has a str attribute :attr:`type_name` this is used instead of the class name inside of config file.
			* a :class:`list` of any of the afore mentioned data types. The list may not be empty when it is passed to this constructor so that the item type can be derived but it can be emptied immediately afterwards. (The type of the items is not dynamically enforced—that's the job of a static type checker—but the type is mentioned in the help.)

		:raises ValueError: if key is not unique
		:raises ValueError: if :paramref:`default` is an empty list because the first element is used to infer the data type to which a value given in a config file is converted
		:raises TypeError: if this setting is a number or a list of numbers and :paramref:`unit` is not given
		'''
		self._key = key
		self.value = default
		self.type = type(default)
		self.help = help
		self.unit = unit
		self.parent = parent
		self.allowed_values = allowed_values

		if self.type == list:
			if not default:
				raise ValueError('I cannot infer the type from an empty list')
			self.item_type = type(default[0])  # type: ignore [index]  # mypy does not understand that I just checked that default is a list
			needs_unit = self.item_type in TYPES_REQUIRING_UNIT
		else:
			needs_unit = self.type in TYPES_REQUIRING_UNIT
		if needs_unit and self.unit is None:
			raise TypeError(f'missing argument unit for {self.key}, pass an empty string if the number really has no unit')

		cls = type(self)
		if key in cls.instances:
			raise ValueError(f'duplicate config key {key!r}')
		cls.instances[key] = self

	@property
	def key(self) -> str:
		'''The name of this setting which is used in the config file. This must be unique.'''
		return self._key

	@key.setter
	def key(self, key: str) -> None:
		if key in self.instances:
			raise ValueError(f'duplicate config key {key!r}')
		del self.instances[self._key]
		self._key = key
		self.instances[key] = self


	@typing.overload
	def __get__(self: _Self, instance: None, owner: typing.Any = None) -> _Self:
		pass

	@typing.overload
	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> T:
		pass

	def __get__(self: _Self, instance: typing.Any, owner: typing.Any = None) -> 'T|_Self':
		if instance is None:
			return self

		return self.value

	def __set__(self, instance: typing.Any, value: T) -> None:
		self.value = value

	def __repr__(self) -> str:
		return '%s(%s, ...)' % (type(self).__name__, ', '.join(repr(a) for a in (self.key, self.value)))

	def parse_and_set_value(self, config_id: 'ConfigId|None', value: str) -> None:
		if config_id is None:
			config_id = self.default_config_id
		if config_id != self.default_config_id:
			raise ValueError(f'{self.key} cannot be set for specific groups, config_id must be the default {self.default_config_id!r} not {config_id!r}')
		self.value = self.parse_value(value)

	def parse_value(self, value: str) -> T:
		return self.parse_value_part(self.type, value)

	def parse_value_part(self, t: 'type[T1]', value: str) -> T1:
		''':raises ValueError: if value is invalid'''
		if t == str:
			value = value.replace(r'\n', '\n')
			out = typing.cast(T1, value)
		elif t == int:
			out = typing.cast(T1, int(value, base=0))
		elif t == float:
			out = typing.cast(T1, float(value))
		elif t == bool:
			if value == VALUE_TRUE:
				out = typing.cast(T1, True)
			elif value == VALUE_FALSE:
				out = typing.cast(T1, False)
			else:
				raise ValueError(f'invalid value for {self.key}: {value!r} (should be {self.format_allowed_values_or_type(t)})')
		elif t == list:
			return typing.cast(T1, [self.parse_value_part(self.item_type, v) for v in value.split(self.LIST_SEP)])
		elif issubclass(t, enum.Enum):
			for enum_item in t:
				if self.format_any_value(typing.cast(T1, enum_item)) == value:
					out = typing.cast(T1, enum_item)
					break
			else:
				raise ValueError(f'invalid value for {self.key}: {value!r} (should be {self.format_allowed_values_or_type(t)})')
		else:
			try:
				out = t(value)  # type: ignore [call-arg]
			except ValueError:
				raise ValueError(f'invalid value for {self.key}: {value!r} (should be {self.format_allowed_values_or_type(t)})')

		if self.allowed_values is not None and out not in self.allowed_values:
			raise ValueError(f'invalid value for {self.key}: {value!r} (should be {self.format_allowed_values_or_type(t)})')
		return out


	def format_allowed_values_or_type(self, t: 'type[typing.Any]|None' = None) -> str:
		out = self.format_allowed_values(t)
		if out:
			return 'one of ' + out

		out = self.format_type(t)

		# getting the article right is not so easy, so a user can specify the correct article with type_article
		# this also gives the possibility to omit the article
		# https://en.wiktionary.org/wiki/Appendix:English_articles#Indefinite_singular_articles
		if hasattr(self.type, 'type_article'):
			article = getattr(self.type, 'type_article')
			if not article:
				return out
			assert isinstance(article, str)
			return article + ' ' + out
		if out[0].lower() in 'aeio':
			return 'an ' + out
		return 'a ' + out

	def format_allowed_values(self, t: 'type[typing.Any]|None' = None) -> str:
		if t is None:
			t = self.type
		allowed_values: 'Iterable[typing.Any]'
		if t not in CONTAINER_TYPES and self.allowed_values is not None:
			allowed_values = self.allowed_values
		elif t == bool:
			allowed_values = (True, False)
		elif issubclass(t, enum.Enum):
			allowed_values = t
		else:
			return ''

		out = ', '.join(self.format_any_value(val) for val in allowed_values)
		if self.unit:
			out += ' (unit: %s)' % self.unit
		return out


	def wants_to_be_exported(self) -> bool:
		return True

	def format_type(self, t: 'type[typing.Any]|None' = None) -> str:
		if t is None:
			if self.type is list:
				t = self.item_type
				item_type = self.format_allowed_values(t)
				if not item_type:
					item_type = self.format_type(t)
				return 'comma separated list of %s' % item_type

			t = self.type

		out = getattr(t, 'type_name', t.__name__)
		if self.unit:
			out += ' in %s' % self.unit
		return out

	def format_value(self, config_id: 'ConfigId|None') -> str:
		return self.format_any_value(self.value)

	def format_any_value(self, value: typing.Any) -> str:
		if isinstance(value, str):
			value = value.replace('\n', r'\n')
		if isinstance(value, enum.Enum):
			return value.name.lower().replace('_', '-')
		if isinstance(value, bool):
			return VALUE_TRUE if value else VALUE_FALSE
		if isinstance(value, list):
			return self.LIST_SEP.join(self.format_any_value(v) for v in value)
		return str(value)


class DictConfig(typing.Generic[T_KEY, T]):

	def __init__(self,
		key_prefix: str,
		default_values: 'dict[T_KEY, T]', *,
		ignore_keys: 'Container[T_KEY]' = set(),
		unit: 'str|None' = None,
		help: 'str|None' = None,
		allowed_values: 'Sequence[T]|None' = None,
	) -> None:
		'''
		:param key_prefix:
		:param default:
		:param ignore_keys:
		:param unit:
		:param help:

		:raises ValueError: if a key is not unique
		'''
		self._values: 'dict[T_KEY, Config[T]]' = {}
		self._ignored_values: 'dict[T_KEY, T]' = {}
		self.allowed_values = allowed_values

		self.key_prefix = key_prefix
		self.unit = unit
		self.help = help
		self.ignore_keys = ignore_keys

		for key, val in default_values.items():
			self[key] = val

	def format_key(self, key: T_KEY) -> str:
		if isinstance(key, enum.Enum):
			key_str = key.name.lower().replace('_', '-')
		elif isinstance(key, bool):
			key_str = VALUE_TRUE if key else VALUE_FALSE
		else:
			key_str = str(key)

		return '%s.%s' % (self.key_prefix, key_str)

	def __setitem__(self, key: T_KEY, val: T) -> None:
		if key in self.ignore_keys:
			self._ignored_values[key] = val
			return

		c = self._values.get(key)
		if c is None:
			self._values[key] = self.new_config(self.format_key(key), val, unit=self.unit, help=self.help)
		else:
			c.value = val

	def new_config(self, key: str, default: T, *, unit: 'str|None', help: 'str|dict[T, str]|None') -> Config[T]:
		return Config(key, default, unit=unit, help=help, parent=self, allowed_values=self.allowed_values)

	def __getitem__(self, key: T_KEY) -> T:
		if key in self.ignore_keys:
			return self._ignored_values[key]
		else:
			return self._values[key].value

	def __repr__(self) -> str:
		values = {key:val.value for key,val in self._values.items()}
		values.update({key:val for key,val in self._ignored_values.items()})
		return '%s(%r, ignore_keys=%r, ...)' % (type(self).__name__, values, self.ignore_keys)

	def __contains__(self, key: T_KEY) -> bool:
		if key in self.ignore_keys:
			return key in self._ignored_values
		else:
			return key in self._values

	def __iter__(self) -> 'Iterator[T_KEY]':
		yield from self._values
		yield from self._ignored_values

	def iter_keys(self) -> 'Iterator[str]':
		for key in self._values:
			yield self.format_key(key)


class ConfigTrackingChanges(Config[T]):

	_has_changed = False

	@property  # type: ignore [override]  # This is a bug in mypy https://github.com/python/mypy/issues/4125
	def value(self) -> T:
		return self._value

	@value.setter
	def value(self, value: T) -> None:
		self._value = value
		self._has_changed = True

	def save_value(self, new_value: T) -> None:
		'''
		Save the current :attr:`value` and assign :paramref:`new_value` to :attr:`value`.
		'''
		self._last_value = self._value
		self._value = new_value
		self._has_changed = False

	def restore_value(self) -> None:
		'''
		Restore :attr:`value` to the value before the last call of :meth:`save_value`.
		'''
		self._value = self._last_value

	def has_changed(self) -> bool:
		'''
		:return: :const:`True` if :attr:`value` has been changed since the last call to :meth:`save_value`
		'''
		return self._has_changed


# ========== settings which can have different values for different groups ==========

class MultiConfig(Config[T]):

	_Self = typing.TypeVar('_Self', bound='MultiConfig[T]')
	config_ids: 'list[ConfigId]' = []

	#: Stores the values for specific objects.
	values: 'dict[ConfigId, T]'

	#: Stores the default value which is used if no value for the object is defined in :attr:`values`.
	value: 'T'

	@classmethod
	def reset(cls) -> None:
		cls.config_ids.clear()
		for cfg in Config.instances:
			if isinstance(cfg, MultiConfig):
				cfg.values.clear()

	def __init__(self,
		key: str,
		default: T, *,
		unit: 'str|None' = None,
		help: 'str|dict[T, str]|None' = None,
		parent: 'MultiDictConfig[typing.Any, T]|None' = None,
		allowed_values: 'Sequence[T]|None' = None,
	) -> None:
		super().__init__(key, default, unit=unit, help=help, parent=parent, allowed_values=allowed_values)
		self.values: 'dict[ConfigId, T]' = {}

	# I don't know why this code duplication is necessary,
	# I have declared the overloads in the parent class already.
	# But without copy-pasting this code mypy complains
	# "Signature of __get__ incompatible with supertype Config"
	@typing.overload
	def __get__(self: _Self, instance: None, owner: typing.Any = None) -> _Self:
		pass

	@typing.overload
	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> T:
		pass

	def __get__(self: _Self, instance: typing.Any, owner: typing.Any = None) -> 'T|_Self':
		if instance is None:
			return self

		return self.values.get(instance.config_id, self.value)

	def __set__(self, instance: typing.Any, value: T) -> None:
		config_id = instance.config_id
		self.values[config_id] = value
		if config_id not in self.config_ids:
			self.config_ids.append(config_id)

	def parse_and_set_value(self, config_id: 'ConfigId|None', value: str) -> None:
		if config_id is None:
			config_id = self.default_config_id
		if config_id == self.default_config_id:
			self.value = self.parse_value(value)
		else:
			self.values[config_id] = self.parse_value(value)
		if config_id not in self.config_ids:
			self.config_ids.append(config_id)

	def format_value(self, config_id: 'ConfigId|None') -> str:
		if config_id is None:
			config_id = self.default_config_id
		return self.format_any_value(self.values.get(config_id, self.value))


class MultiDictConfig(DictConfig[T_KEY, T]):

	_Self = typing.TypeVar('_Self', bound='MultiDictConfig[T_KEY, T]')

	@typing.overload
	def __get__(self: _Self, instance: None, owner: typing.Any = None) -> _Self:
		pass

	@typing.overload
	def __get__(self, instance: typing.Any, owner: typing.Any = None) -> 'InstanceSpecificDictMultiConfig[T_KEY, T]':
		pass

	def __get__(self: _Self, instance: typing.Any, owner: typing.Any = None) -> 'InstanceSpecificDictMultiConfig[T_KEY, T]|_Self':
		if instance is None:
			return self

		return InstanceSpecificDictMultiConfig(self, instance.config_id)

	def __set__(self, instance: typing.Any, value: T) -> None:
		raise NotImplementedError()

	def new_config(self, key: str, default: T, *, unit: 'str|None', help: 'str|dict[T, str]|None') -> MultiConfig[T]:
		return MultiConfig(key, default, unit=unit, help=help, parent=self, allowed_values=self.allowed_values)

class InstanceSpecificDictMultiConfig(typing.Generic[T_KEY, T]):

	def __init__(self, dmc: 'MultiDictConfig[T_KEY, T]', config_id: ConfigId) -> None:
		self.dmc = dmc
		self.config_id = config_id

	def __setitem__(self, key: T_KEY, val: T) -> None:
		if key in self.dmc.ignore_keys:
			raise TypeError('cannot set value of ignored key %r' % key)

		c = self.dmc._values.get(key)
		if c is None:
			self.dmc._values[key] = MultiConfig(self.dmc.format_key(key), val, help=self.dmc.help)
		else:
			c.__set__(self, val)

	def __getitem__(self, key: T_KEY) -> T:
		if key in self.dmc.ignore_keys:
			return self.dmc._ignored_values[key]
		else:
			return self.dmc._values[key].__get__(self)
