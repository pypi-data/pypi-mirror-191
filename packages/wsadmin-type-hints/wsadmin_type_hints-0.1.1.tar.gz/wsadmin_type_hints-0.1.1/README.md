# `wsadmin-type-hints`
Python package providing **type hints** for `wsadmin` **Jython** commands.

This speeds up the development of `wsadmin` **Jython** scripts inside an IDE since it provides intellisense on every method of the 5 main objects provided at runtime by the `wsadmin`:
- `AdminControl`
- `AdminConfig`
- `AdminApp`
- `AdminTask`
- `Help`

[📚 **Read the full documentation**](https://lukesavefrogs.github.io/wsadmin-type-hints/)

# Disclaimer
This is an unofficial package created for speeding up the development process and is not in any way affiliated with IBM®. All trademarks and registered trademarks are the property of their respective company owners.

The code does not include any implementation detail, and includes only the informations (such as parameter numbers, types and descriptions) publicly available on the official Websphere Application Server® documentation.

# Informations

This projects uses type hints, which were introduced in **Python 3.5**, so ensure you're using a supported version of python.

From the [Python Stubs](https://typing.readthedocs.io/en/latest/source/stubs.html) documentation:
> Type stubs are syntactically valid Python 3.7 files with a .pyi suffix. The Python syntax used for type stubs is independent from the Python versions supported by the implementation, and from the Python version the type checker runs under (if any). Therefore, type stub authors should use the latest available syntax features in stubs (up to Python 3.7), even if the implementation supports older, pre-3.7 Python versions.
