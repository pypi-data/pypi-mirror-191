# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'confattr'
copyright = '2022, erzo'
author = 'erzo'
release = 'v0.7.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx_paramlinks']

templates_path = ['_templates']
exclude_patterns = []
intersphinx_mapping = {
	'python': ('https://docs.python.org/3', None),
	'pytest': ('https://docs.pytest.org/en/latest', None),
}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options = {
	'display_version': True,
}

# https://stackoverflow.com/a/63054018
try:
	html_context
except NameError:
	html_context = dict()
html_context['version'] = release

html_css_files = ['no-ligatures-in-code.css']

#https://docutils.sourceforge.io/docs/ref/rst/definitions.html
rst_prolog = '''
.. |WARNING| replace:: **Warning**
.. |nbsp|   unicode:: U+000A0 .. NO-BREAK SPACE
.. |quad|   unicode:: U+02003 .. EM SPACE
.. |emdash| unicode:: U+2014  .. EM DASH
.. |endash| unicode:: U+2013  .. EM DASH
.. role:: python(code)
   :language: python
'''


# -- autodoc configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

autoclass_content = 'both'  # 'class', 'both', 'init'
#autodoc_class_signature = 'separated'  # 'mixed', 'separated'
#autodoc_member_order = 'bysource'  # 'alphabetical', 'groupwise', 'bysource'
#autodoc_typehints = 'description'  # 'signature', 'description', 'none', 'both'
#autodoc_typehints_description_target = 'documented_params'  # 'all', 'documented', 'documented_params'
#autodoc_type_aliases = {}
#autodoc_typehints_format = 'fully-qualified'  # 'fully-qualified', 'short'
#autodoc_preserve_defaults = True  # True, False
#autodoc_warningiserror = True  # True, False
#autodoc_inherit_docstrings = True  # True, False
