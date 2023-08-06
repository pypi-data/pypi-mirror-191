#!../../../../venv/bin/python3
__package__ = 'example_app'

# ------- start -------
from confattr import Config, ConfigFile
greeting = Config('ui.greeting', 'hello world')
ConfigFile(appname=__package__).load()
print(greeting.value)
