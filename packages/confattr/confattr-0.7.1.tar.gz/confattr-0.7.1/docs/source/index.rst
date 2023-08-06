.. confattr documentation master file, created by
   sphinx-quickstart on Sun Nov 20 08:25:23 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. py:currentmodule:: confattr


===================================
Welcome to confattr's documentation
===================================

:mod:`confattr` (config attributes) is a python library to read and write config files with the following features:

- Static type checking of the code is possible with e.g. `mypy <https://mypy-lang.org/>`_.
- Values are checked and if the config file contains invalid syntax, unknown keys or invalid values a useful error messages is given to the user via a callback registered with :meth:`ConfigFile.set_ui_callback`.
- It is possible to create a default config file with comments giving help and allowed values via :meth:`ConfigFile.save`. :ref:`[example] <exp-save>`
- It is possible to generate a help via :meth:`ConfigFile.write_help` and :meth:`ConfigFile.get_help`. :ref:`[example] <exp-generating-help>`
- Settings can be changed via environment variables, too. :ref:`[example] <exp-env>`
- It is easy to integrate into existing projects, just replace an existing attribute with a :class:`Config` instance.
  For example, assume a class has the attribute :python:`color = 'red'`.
  Replace it with :python:`color = Config('color', 'red', allowed_values=['red', 'green', 'blue'])` and call :meth:`ConfigFile.load` (after the attribute has been created but before it's value is used).
  Then a user can create a config file in the :meth:`expected location <ConfigFile.iter_config_paths>` and can change the attribute with ``set color=green``.
  You don't need to change the usage of the attribute because :class:`Config` implements the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`_.
- It is easy to add custom commands by subclassing :class:`ConfigFileCommand`. :ref:`[example] <exp-extend>`
- It can be used to parse single lines, e.g. from a command line, too, with :meth:`ConfigFile.parse_line`.
- It is well documented.
- Includes an example for test automation. :ref:`[example] <exp-pytest>`


Introduction and examples
=========================

.. toctree::
   :maxdepth: 2

   intro


Reference
=========

.. toctree::
   :maxdepth: 2

   confattr
   confattr.config
   confattr.configfile
   confattr.subprocess_pipe
   confattr.types
   confattr.utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Links
=====

* `Source code <https://gitlab.com/erzo/confattr>`_
* `Bug tracker <https://gitlab.com/erzo/confattr/-/issues>`_
* `Change log <https://gitlab.com/erzo/confattr/-/tags>`_
* `PyPI <https://pypi.org/project/confattr/>`_
