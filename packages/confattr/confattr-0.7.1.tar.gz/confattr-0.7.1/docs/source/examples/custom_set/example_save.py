# This is not an example but a test
# but I cannot insert this into test_example.py
# or call this file test because if pytest loads it
# the default implementation of Set is replaced
# and the following tests are screwed up.
# Instead I am calling this via subprocess in test_example.py

from confattr import Config, ConfigFile
import example  # type: ignore [import]  # mypy wants `from . import example` but that would cause ModuleNotFoundError: No module named 'confattr' at run time

cs = Config('some string', 'hello world')
cb = Config('some bool', True)
cl = Config('some list', [1,2,3], unit='')

config_file = ConfigFile(appname='test')
def fail(msg: str) -> None:
	raise AssertionError(msg)
config_file.set_ui_callback(lambda lvl, msg: fail(str(msg)))

config_file.save()

cs.value = 'foo'
cb.value = False
cl.value = [42]
assert cs.value == 'foo'
assert cb.value == False
assert cl.value == [42]

config_file.load()
assert cs.value == 'hello world'
assert cb.value == True
assert cl.value == [1,2,3]
