#!../venv/bin/pytest -s

from collections.abc import Iterator

import pytest

from confattr.configfile import ConfigFileCommand, Set, Include

default_commands = [Set, Include]

@pytest.fixture(autouse=True)
def reset_command_subclasses() -> 'Iterator[None]':
	yield
	ConfigFileCommand._subclasses = list(default_commands)
	ConfigFileCommand._used_names = {name for cmd in default_commands for name in cmd.get_names()}



# ------- replace = False -------

def test_custom_subclass() -> None:
	class SetAndLog(Set):
		pass

	assert Set in ConfigFileCommand.get_command_types()
	assert SetAndLog in ConfigFileCommand.get_command_types()
	assert SetAndLog.get_name() != Set.get_name()
	assert list(SetAndLog.get_names()) == [SetAndLog.get_name()]

def test_custom_classes() -> None:
	class Parent(ConfigFileCommand):
		name = 'foo'

	class Child(Parent):
		pass

	assert Parent in ConfigFileCommand.get_command_types()
	assert Child in ConfigFileCommand.get_command_types()
	assert Child.get_name() != Parent.get_name()
	assert list(Child.get_names()) == [Child.get_name()]

	assert Parent.get_name() == 'foo'
	assert Child.get_name() == 'child'

def test_custom_classes_with_aliases() -> None:
	class Parent(ConfigFileCommand):
		name = 'foo'
		aliases = ('bar', 'baz')

	class Child(Parent):
		pass

	assert Parent in ConfigFileCommand.get_command_types()
	assert Child in ConfigFileCommand.get_command_types()
	assert Child.get_name() != Parent.get_name()
	assert list(Child.get_names()) == [Child.get_name()]

	assert list(Parent.get_names()) == ['foo', 'bar', 'baz']
	assert list(Child.get_names()) == ['child']



def test_error_duplicate_name() -> None:
	class Cmd1(ConfigFileCommand):
		name = 'foo'

	with pytest.raises(ValueError, match="duplicate command name 'foo'"):
		class Cmd2(ConfigFileCommand):
			name = 'foo'


# ------- replace = True -------

def test_replace() -> None:
	class MySet(Set, replace=True):
		pass

	assert Set not in ConfigFileCommand.get_command_types()
	assert MySet in ConfigFileCommand.get_command_types()
	assert MySet.name == Set.get_name()
	assert list(MySet.get_names()) == list(Set.get_names())

def test_replace_with_explicit_name() -> None:
	class Parent(ConfigFileCommand):
		name = 'foo'

	class Replacement(Parent, replace=True):
		pass

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.name == Parent.name
	assert list(Replacement.get_names()) == list(Parent.get_names())

def test_replace_with_aliases() -> None:
	class Parent(ConfigFileCommand):
		aliases = ('foo', 'bar')

	class Replacement(Parent, replace=True):
		pass

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.get_name() == Parent.get_name()
	assert list(Replacement.get_names()) == list(Parent.get_names())
	assert list(Replacement.get_names()) == ['parent', 'foo', 'bar']

def test_replace_with_new_name() -> None:
	class Parent(ConfigFileCommand):
		pass

	class Replacement(Parent, replace=True):
		name = 'new'

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.name != Parent.get_name()
	assert Replacement.name == 'new'
	assert list(Replacement.get_names())[1:] == list(Parent.get_names())[1:]

def test_replace_with_new_aliases() -> None:
	class Parent(ConfigFileCommand):
		aliases = ['not-existing']

	class Replacement(Parent, replace=True):
		name = 'new'
		aliases = ['repl']

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.name != Parent.get_name()
	assert Replacement.name == 'new'
	assert list(Replacement.get_names()) == ['new', 'repl']



def test_double_replace() -> None:
	class Set1(Set, replace=True):
		name = 'set1'
	class Set2(Set, replace=True):
		name = 'set2'
