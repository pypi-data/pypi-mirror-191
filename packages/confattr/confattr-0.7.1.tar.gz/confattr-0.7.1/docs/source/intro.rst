.. py:currentmodule:: confattr

=========================
Introduction and examples
=========================

.. _exp-config:
.. _exp-save:

Config and ConfigFile
=====================

:mod:`confattr` (config attributes) is a python library to make applications configurable.
This library defines the :class:`Config` class to create attributes which can be changed in a config file.
It uses the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`_ to return it's value when used as an instance attribute.

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- start -------
   :end-before: # ------- 01 -------

If you want to access the Config object itself you need to access it as a class attribute:

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- 01 -------
   :end-before: # ------- 02 -------

You load a config file with a :class:`ConfigFile` object.
In order to create a ConfigFile instance you need to provide a callback function which informs the user if the config file contains invalid lines.
This callback function takes two arguments: (1) a :class:`NotificationLevel` which says whether the notification is an error or an information and (2) the message to be presented to the user, either a :class:`str` or a :class:`BaseException`.
When you load a config file with :meth:`ConfigFile.load` all :class:`Config` objects which are set in the config file are updated automatically.

It is recognized automatically that the setting ``traffic-law.speed-limit`` has an integer value.
A value given in a config file is therefore automatically parsed to an integer.
If the parsing fails the user interface callback function is called.

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- 02 -------
   :end-before: # ------- 02-end -------

Given the following config file (the location of the config file is determined by :meth:`ConfigFile.iter_config_paths`):

.. literalinclude:: examples/config_and_configfile/config

The script will give the following output:

.. literalinclude:: examples/config_and_configfile/output.txt
   :language: text

You can save the current configuration with :meth:`ConfigFile.save` if you want to write it to the default location
or with :meth:`ConfigFile.save_file` if you want to specify the path yourself.

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- 03-begin -------

This will write the following file:

.. literalinclude:: examples/config_and_configfile/exported-config


Config file syntax
==================

I have looked at the config files of different applications trying to come up with a syntax as intuitive as possible.
Two extremes which have heavily inspired me are the config files of `vim <https://www.vim.org/>`_ and `ranger <https://ranger.github.io/>`_.
Quoting and inline comments work like in a POSIX shell (except that there is no difference between single quotes and double quotes) as I am using :func:`shlex.split` to split the lines.

Lines starting with a ``"`` or ``#`` are ignored.

The ``set`` command has two different forms.
I recommend to *not* mix them in order to improve readability.

- ``set key1=val1 [key2=val2 ...]`` |quad| (inspired by vimrc)

  ``set`` takes an arbitrary number of arguments, each argument sets one setting.

  Has the advantage that several settings can be changed at once.
  This is useful if you want to bind a set command to a key and process that command with :meth:`ConfigFile.parse_line` if the key is pressed.

  If the value contains one or more spaces it must be quoted.
  ``set greeting='hello world'`` and ``set 'greeting=hello world'`` are equivalent.

- ``set key [=] val`` |quad| (inspired by ranger config)

  ``set`` takes two arguments, the key and the value.
  Optionally a single equals character may be added in between as third argument.

  Has the advantage that key and value are separated by one or more spaces which can improve the readability of a config file.

  If the value contains one or more spaces it must be quoted:
  ``set greeting 'hello world'`` and ``set greeting = 'hello world'`` are equivalent.

I recommend to not use spaces in key names so that they don't need to be wrapped in quotes.


It is possible to include another config file:

- ``include filename``

  If ``filename`` is a relative path it is relative to the directory of the config file it appears in.

  This command is explained in more detail in :ref:`this example <exp-include>`.



.. _exp-multi:

Different values for different objects
======================================

A :class:`Config` object always returns the same value, regardless of the owning object it is an attribute of:

.. literalinclude:: examples/config_same_value/example.py
   :language: python
   :start-after: # ------- start -------

Output:

.. literalinclude:: examples/config_same_value/output.txt
   :language: text



If you want to have different values for different objects you need to use :class:`MultiConfig` instead.
This requires the owning object to have a special attribute called :attr:`config_id`.
All objects which have the same :attr:`config_id` share the same value.
All objects which have different :attr:`config_id` can have different values (but don't need to have different values).

.. literalinclude:: examples/multiconfig/example.py
   :language: python
   :start-after: # ------- start -------

Given the following config file:

.. literalinclude:: examples/multiconfig/config

It creates the following output:

.. literalinclude:: examples/multiconfig/output.txt
   :language: text



``another-car`` gets the default color black as it is not set in the config file.
You can change this default color in the config file by setting it before specifying a config id or after specifying the special config id ``general`` (:attr:`Config.default_config_id`).
Note how this adds ``general`` to :attr:`MultiConfig.config_ids`.

.. literalinclude:: examples/multiconfig/config2

Creates the following output:

.. literalinclude:: examples/multiconfig/output2.txt
   :language: text



.. _exp-include:

Include
=======

Consider a backup application which synchronizes one or more directory pairs.
The following code might be a menu for it to choose which side should be changed:

.. literalinclude:: examples/include/example.py
   :language: python
   :start-after: # ------- start -------

Let's assume there are many more settings how to synchronize a pair of directories than just the direction.
You might want to use the same synchronization settings for several directory pairs.
You can write these settings to a separate config file and include it for the corresponding directory pairs:

.. literalinclude:: examples/include/config
   :caption: main config file: config
.. literalinclude:: examples/include/mirror
   :caption: included config file: mirror
.. literalinclude:: examples/include/two-way
   :caption: included config file: two-way

This produces the following display:

.. literalinclude:: examples/include/output.txt
   :emphasize-lines: 1

The config id of the included file starts with the value of the config id that the including file has at the moment of calling ``include``.
Otherwise the pattern shown above of reusing a config file for several config ids would not be possible.

If the included file changes the config id the config id is reset to the value it had at the beginning of the include when reaching the end of the included file.
Otherwise changing an included file might unexpectedly change the meaning of the main config file or another config file which is included later on.

It is possible to change this default behavior by using ``include --reset-config-id-before filename`` or ``include --no-reset-config-id-after filename``.


.. _exp-generating-help:

Generating help
===============

You can generate a help with :meth:`ConfigFile.write_help` or :meth:`ConfigFile.get_help`.

:meth:`ConfigFile.get_help` is a wrapper around :meth:`ConfigFile.write_help`.
If you want to print the help to stdout :python:`config_file.write_help(HelpWriter(None))` would be more efficient than :python:`print(config_file.get_help())`.
If you want to display the help in a graphical user interface you can implement a custom :class:`FormattedWriter` which you can pass to :meth:`ConfigFile.write_help` instead of parsing the output of :meth:`ConfigFile.get_help`.

.. literalinclude:: examples/generating_help/example.py
   :language: python
   :start-after: # ------- start -------

Assuming the above file was contained in a package called ``exampleapp`` it would output the following:

.. literalinclude:: examples/generating_help/output.txt
   :language: text



The help is formatted on two levels:

1. :class:`argparse.HelpFormatter` does the merging of lines, wrapping of lines and indentation. It formats the usage and all the command line arguments and options.
   Unfortunately "All the methods provided by the class are considered an implementation detail" according to it's `doc string <https://github.com/python/cpython/blob/main/Lib/argparse.py#L157>`_.
   The only safe way to customize this level of formatting is by handing one of the predefined standard classes to the :paramref:`~ConfigFile.formatter_class` parameter of the :class:`ConfigFile` constructor:

   - :class:`argparse.HelpFormatter`
   - :class:`argparse.RawDescriptionHelpFormatter`
   - :class:`argparse.RawTextHelpFormatter`
   - :class:`argparse.ArgumentDefaultsHelpFormatter`
   - :class:`argparse.MetavarTypeHelpFormatter`

   Additionally I provide another subclass :class:`confattr.utils.HelpFormatter` which has a few class attributes for customization which I am trying to keep backward compatible.
   So you can subclass this class and change these attributes.
   But I cannot guarantee to always support the newest python version.

   If you want any more customization take a look at the `source code <https://github.com/python/cpython/blob/main/Lib/argparse.py#L157>`_ but be prepared that you may need to change your code with any future python version.

2. :class:`FormattedWriter` is intended to do stuff like underlining sections and inserting comment characters at the beginning of lines (when writing help to a config file).
   This package defines two subclasses:
   :class:`ConfigFileWriter` which is used by default in :meth:`ConfigFile.save` and
   :class:`HelpWriter` which is used in :meth:`ConfigFile.get_help`.

   If you want to customize this level of formatting implement your own :class:`FormattedWriter`
   and override :meth:`ConfigFile.get_help` or :meth:`ConfigFile.save_to_open_file` to use your class.


Custom data types
=================

It is possible to use custom data types.
You can use that for example to avoid repeating a part of help which applies to several settings:

.. literalinclude:: examples/regex/example.py
   :language: python
   :start-after: # ------- start -------

This exports the following config file:

.. literalinclude:: examples/regex/config

:meth:`__str__` must return a string representation suitable for the config file and the constructor must create an equal object if it is passed the return value of :meth:`__str__`. This is fulfilled by inheriting from :class:`str`.

:attr:`type_name` is a special str attribute which specifies how the type is called in the config file. If it is missing it is derived from the class name.

:attr:`help` is a special str attribute which contains a description which is printed to the config file. If this is missing a help must be provided via :meth:`Set.set_help_for_type`.

:mod:`confattr.types` defines several such types, including the above definition of :class:`Regex`.

For more information on the supported data types see :class:`Config`.


.. _exp-extend:

Adding new commands to the config file syntax
=============================================

You can extend this library by defining new commands which can be used in the config file.
All you need to do is subclass :class:`ConfigFileCommand` and implement the :meth:`ConfigFileCommand.run` method.
Additionally I recommend to provide a doc string explaining how to use the command in the config file. The doc string is used by :meth:`get_help` which may be used by an in-app help.
Optionally you can set :attr:`ConfigFileCommand.name` and :attr:`ConfigFileCommand.aliases` and implement the :meth:`ConfigFileCommand.save` method.

Alternatively :class:`ConfigFileArgparseCommand` can be subclassed instead, it aims to make the parsing easier and avoid redundancy in the doc string by using the :mod:`argparse` module.
You must implement :meth:`init_parser` and :meth:`run_parsed`.
You should give a doc string describing what the command does.
In contrast to :class:`ConfigFileCommand` :mod:`argparse` adds usage and the allowed arguments to the output of :meth:`ConfigFileArgparseCommand.get_help` automatically.

For example you may want to add a new command to bind keys to whatever kind of command.
The following example assumes `urwid`_ as user interface framework.

.. literalinclude:: examples/map/example.py
   :language: python
   :start-after: # ------- start -------

Given the following config file it is possible to move the cursor upward and downward with ``j`` and ``k`` like in vim:

.. literalinclude:: examples/map/config


The help for the newly defined command looks like this:

.. literalinclude:: examples/map/example_print_help.py
   :language: python
   :start-after: # ------- start -------

.. literalinclude:: examples/map/output_help.txt



(All subclasses of :class:`ConfigFileCommand` are saved in :meth:`ConfigFileCommand.__init_subclass__` and can be retrieved with :meth:`ConfigFileCommand.get_command_types`.
The :class:`ConfigFile` constructor uses that if :paramref:`commands` is not given.)


Writing custom commands to the config file
==========================================

The previous example has shown how to define new commands so that they can be used in the config file.
Let's continue that example so that calls to the custom command ``map`` are written with :meth:`ConfigFile.save`.

All you need to do for that is implementing the :meth:`ConfigFileCommand.save` method.

:attr:`~ConfigFileCommand.should_write_heading` is True if there are several commands which implement the :meth:`~ConfigFileCommand.save` method.

Experimental support for type checking ``**kw`` has been added in `mypy 0.981 <https://mypy-lang.blogspot.com/2022/09/mypy-0981-released.html>`_.
:class:`SaveKwargs` depends on :class:`typing.TypedDict` and therefore is not available before Python 3.8.

.. literalinclude:: examples/map_save/example_1.py
   :language: python
   :start-after: # ------- start -------

However, :data:`urwid.command_map` contains more commands than the example app uses so writing all of them might be confusing.
Therefore let's add a keyword argument to write only the specified commands:

.. literalinclude:: examples/map_save/example_3.py
   :language: python
   :start-after: # ------- start -------

This produces the following config file:

.. literalinclude:: examples/map_save/config


If you don't care about Python < 3.8 you can import :class:`SaveKwargs` normally and save a line when calling :meth:`ConfigFile.save`:

.. code-block:: python

       kw: SaveKwargs = MapSaveKwargs(urwid_commands=...)
       config_file.save(**kw)


Customizing the config file syntax
==================================

If you want to make minor changes to the syntax of the config file you can subclass the corresponding command, i.e. :class:`Set` or :class:`Include`.

For example if you want to use a ``key: value`` syntax you could do the following.

I am setting :attr:`name` to an empty string (i.e. :const:`confattr.DEFAULT_COMMAND`) to make this the default command which is used if an unknown command is encountered.
This makes it possible to use this command without writing out it's name in the config file.

.. literalinclude:: examples/custom_set/example.py
   :language: python
   :start-after: # ------- start -------

Then a config file might look like this:

.. literalinclude:: examples/custom_set/config
   :end-before: # ------- end -------

Please note that it's still possible to use the ``include`` command.
If you want to avoid that use

.. literalinclude:: examples/custom_set/example_no_include.py
   :language: python
   :start-after: # ------- start -------
   :end-before: # ------- end -------

If you want to make bigger changes like using JSON you need to subclass :class:`ConfigFile`.


Config without classes
======================

If you want to use :class:`Config` objects without custom classes you can access the value via the :attr:`Config.value` attribute:

.. literalinclude:: examples/config_without_classes/example.py
   :language: python
   :start-after: # ------- start -------

Given the following config file (the location of the config file is determined by :meth:`ConfigFile.iter_config_paths`):

.. literalinclude:: examples/config_without_classes/config

The script will give the following output:

.. literalinclude:: examples/config_without_classes/output.txt
   :language: text



.. _exp-pytest:

Testing your application
========================

I recommend doing static type checking with `mypy <https://mypy-lang.org/>`_
in `strict mode <https://mypy.readthedocs.io/en/latest/getting_started.html#strict-mode-and-configuration>`_
and dynamic testing with `pytest`_.
`tox <https://tox.wiki/en/latest/>`_ can run both in a single command and automatically handles virtual environments for you.
While you can configure tox to run your tests on several specific python versions you can also simply use ``py3`` which will use whatever python 3 version you have installed.
For packaging and publishing your application I recommend `flit <https://flit.pypa.io/en/stable/>`_
over the older `setuptools <https://setuptools.pypa.io/en/latest/setuptools.html>`_
because flit is much more intuitive and less error prone.

For dynamic testing you need to consider two things:

1. Your application must not load a config file from the usual paths so that the tests always have the same outcome no matter which user is running them and on which computer.
   You can achieve that by setting one of the attributes :attr:`ConfigFile.config_directory` or :attr:`ConfigFile.config_path` or one of the corresponding environment variables ``APPNAME_CONFIG_DIRECTORY`` or ``APPNAME_CONFIG_PATH`` in the setup of your tests.

   In `pytest`_ you can do this with an `auto use <https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request>`_ `fixture <https://docs.pytest.org/en/6.2.x/fixture.html#what-fixtures-are>`_.
   `tmp_path <https://docs.pytest.org/en/6.2.x/reference.html#tmp-path>`_ creates an empty directory for you and `monkeypatch`_ cleans up for you after the test is done.
   If all of your tests are defined in a single file you can define this fixture in that file.
   Otherwise the definition goes into `conftest.py <https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files>`_.

   .. literalinclude:: examples/testing_tmp_path/example.py
      :language: python
      :start-after: # ------- start -------

2. Your tests need to change settings in order to test all possibilities but all settings which have been changed in a test must be reset after each test so that the tests always have the same outcome no matter whether they are executed all together or alone.

   Of course you could just save a config file in the setup and load it in the teardown.
   But keep in mind that you may have many settings and many tests and that they may become more in the future.
   It is more efficient to let `monkeypatch`_ clean up only those settings that you have changed.

   Let's assume we want to test our car from the :ref:`first example <exp-config>`:

   .. literalinclude:: examples/testing_monkeypatch_config/example.py
      :language: python
      :start-after: # ------- start -------


   If we want to change the value of a :class:`MultiConfig` setting like in :ref:`this example <exp-multi>` for a specific object
   we would use :meth:`monkeypatch.setitem() <pytest.MonkeyPatch.setitem>` to change :attr:`MultiConfig.values`:

   .. literalinclude:: examples/testing_monkeypatch_multiconfig/example.py
      :language: python
      :start-after: # ------- start -------



.. _pytest: https://docs.pytest.org/en/stable/
.. _monkeypatch: https://docs.pytest.org/en/6.2.x/reference.html#std-fixture-monkeypatch



.. _exp-env:

Environment variables
=====================

Settings can be changed via environment variables, too.
For example if you have an application called ``example-app`` with the following code

.. literalinclude:: examples/env/example.py
   :language: python
   :start-after: # ------- start -------

and you call it like this

.. literalinclude:: examples/env/example.sh
   :language: bash
   :start-after: # ------- start -------

it will print

.. literalinclude:: examples/env/expected_output.txt
   :language: bash

For the exact rules how the names of the environment variables are created are described in :meth:`ConfigFile.get_env_name`.

Environment variables which start with the name of the application but do not match a setting (and are not one those listed below) or have an invalid value are reported as :obj:`~NotificationLevel.ERROR` to the callback registered with :meth:`ConfigFile.set_ui_callback`.


Furthermore this library is influenced by the following environment variables:

- ``XDG_CONFIG_HOME`` defines the base directory relative to which user-specific configuration files should be stored on Linux. [1]_ [2]_
- ``XDG_CONFIG_DIRS`` defines the preference-ordered set of base directories to search for configuration files in addition to the ``XDG_CONFIG_HOME`` base directory on Linux. The directories in ``XDG_CONFIG_DIRS`` should be separated with a colon. [1]_ [2]_
- ``APPNAME_CONFIG_PATH`` defines the value of :attr:`ConfigFile.config_path`. [2]_ [3]_
- ``APPNAME_CONFIG_DIRECTORY`` defines the value of :attr:`ConfigFile.config_directory`. [2]_ [3]_
- ``APPNAME_CONFIG_NAME``  defines the value of :attr:`ConfigFile.config_name`. [2]_ [3]_


.. [1] is not queried directly but outsourced to `platformdirs <https://pypi.org/project/platformdirs/>`_, `xdgappdirs <https://pypi.org/project/xdgappdirs/>`_ or `appdirs <https://pypi.org/project/appdirs/>`_, see :meth:`ConfigFile.get_app_dirs`.
   See also https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html#variables.
.. [2] influences :meth:`ConfigFile.iter_config_paths`
.. [3] where ``APPNAME`` is the value of :paramref:`appname <ConfigFile.appname>` which is passed to the constructor of :class:`ConfigFile` but in all upper case letters and hyphens, dots and spaces replaced by underscores, see :meth:`ConfigFile.get_env_name`.



.. _urwid: http://urwid.org/
