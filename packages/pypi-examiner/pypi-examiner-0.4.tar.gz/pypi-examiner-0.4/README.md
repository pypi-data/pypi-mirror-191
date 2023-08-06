# pypi-examiner

[![License](https://img.shields.io/github/license/tweedge/pypi-examiner)](https://github.com/tweedge/pypi-examiner)
[![Downloads](https://img.shields.io/pypi/dm/pypi-examiner)](https://pypi.org/project/pypi-examiner/)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

PyPI Examiner scrapes PyPI for a few things the JSON API doesn't provide. Currently, this supports:

* Finding the current maintainers' usernames for any package
* Finding all packages that a given user maintains

This package should not be considered especially stable at this time, and may cease to function or may be heavily revised without notice.

### Usage

```
from pypi_examiner import examiner

pypi = examiner()
who = pypi.who_maintains("unishox2_py3")
# who is: ["tweedge"]

maint = pypi.maintained_by("tweedge")
# maint is: ["unishox2-py3", "pypi-examiner", "dns-mollusc"]
```

If the package does not exist, the maintainer owns no packages, or another error has arose: expect the result to be `[]`
