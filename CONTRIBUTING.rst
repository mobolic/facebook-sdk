Contributing
============

Use Github Pull Requests
------------------------

All potential code changes should be submitted as pull requests on Github. A
pull request should only include commits directly applicable to its change
(e.g. a pull request that adds a new feature should not include PEP8 changes in
an unrelated area of the code).

Code Style
----------

Code *must* be compliant with `PEP 8`_. Use the latest version of `pep8`_ or
`flake8`_ to catch issues.

Git commit messages should include `a summary and proper line wrapping`_.

.. _PEP 8: https://www.python.org/dev/peps/pep-0008/
.. _pep8: https://pypi.python.org/pypi/pep8
.. _flake8: https://pypi.python.org/pypi/flake8
.. _a summary and proper line wrapping: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

Update Tests and Documentation
------------------------------

All non-trivial changes should include full test coverage. Please review
the package's documentation to ensure that it is up to date with any changes.
