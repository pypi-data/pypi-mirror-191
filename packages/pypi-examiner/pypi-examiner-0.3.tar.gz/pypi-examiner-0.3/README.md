# pypi-examiner

[![License](https://img.shields.io/github/license/tweedge/pypi-examiner)](https://github.com/tweedge/pypi-examiner)
[![Downloads](https://img.shields.io/pypi/dm/pypi-examiner)](https://pypi.org/project/pypi-examiner/)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

PyPI Examiner scrapes PyPI for a few things the JSON API doesn't provide. Currently, this supports:

* Finding the current maintainer's usernames for any package

This package should not be considered especially stable at this time, and may cease to function or may be heavily revised without notice.

### Usage

```
pypi = examiner()
result = pypi.who_maintains("unishox2_py3")
# result is: ["tweedge"]
```

If the package does not exist or another error has arose, then the result is `[""]`