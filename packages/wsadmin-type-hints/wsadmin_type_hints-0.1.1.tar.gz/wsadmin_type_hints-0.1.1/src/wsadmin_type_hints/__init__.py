"""
Include `wsadmin.sh` Jython language objects:
- `AdminControl`
- `AdminConfig`
- `AdminApp`
- `AdminTask`
- `Help`


Use it like this:
```python
try:
	(AdminControl, AdminConfig, AdminApp, AdminTask, Help)
except NameError:
	from wsadmin_language import *
else:
	print("AdminControl is already defined, no shim needed")
```
"""


__all__ = [
	"AdminApp",
	"AdminConfig",
	"AdminTask",
	"AdminControl",
	"Help",
]


# import sys
# if sys.version_info <= (3, 5):
#     # Specific minor version features can be easily checked with tuples.
# 	raise Exception("Your Python version does not satisfy the minimum requirements")

# Additional try/except to ensure that even if installed in a real environment,
# the original modules do not get overwritten.
try:
	(AdminControl, AdminConfig, AdminApp, AdminTask, Help)
except NameError:
	# ----- Interact with a configuration object    -----
	from . import AdminApp
	from . import AdminConfig
	from . import AdminTask


	# -----     Interact with a runtime object      -----
	from . import AdminControl


	# -----              Helper module              -----
	from . import Help

	print(Help.__doc__)