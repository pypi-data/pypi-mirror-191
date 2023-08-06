# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rics',
 'rics._internal_support',
 'rics._internal_support.changelog',
 'rics.collections',
 'rics.mapping',
 'rics.pandas',
 'rics.performance',
 'rics.wip']

package_data = \
{'': ['*'], 'rics.performance': ['templates/*']}

install_requires = \
['pandas>=1.1']

extras_require = \
{'cli': ['click'], 'plotting': ['matplotlib', 'seaborn']}

entry_points = \
{'console_scripts': ['mtimeit = rics.performance.cli:main']}

setup_kwargs = {
    'name': 'rics',
    'version': '2.1.0',
    'description': 'My personal little ML engineering library.',
    'long_description': '<div align="center">\n  <img src="https://github.com/rsundqvist/rics/raw/master/docs/logo-text.png"><br>\n</div>\n\n-----------------\n\n# RiCS: my personal little ML engineering library. <!-- omit in toc -->\n[![PyPI - Version](https://img.shields.io/pypi/v/rics.svg)](https://pypi.python.org/pypi/rics)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rics.svg)](https://pypi.python.org/pypi/rics)\n[![Tests](https://github.com/rsundqvist/rics/workflows/tests/badge.svg)](https://github.com/rsundqvist/rics/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/rsundqvist/rics/branch/master/graph/badge.svg)](https://codecov.io/gh/rsundqvist/rics)\n[![Read the Docs](https://readthedocs.org/projects/rics/badge/)](https://rics.readthedocs.io/)\n[![PyPI - License](https://img.shields.io/pypi/l/rics.svg)](https://pypi.python.org/pypi/rics)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n## What is it?\nAn assorted collections of generic functions that used to live in a Dropbox folder where I used to keep useful snippets.\nRiCS, pronounced _"rix_", is short for _**Ri**chard\'s **C**ode **S**tash_. I started this project with the purpose of \nlearning more about Python best practices, typing and the Python ecosystem. It has grown organically since then, and now\nprovides a wide variety of utility functions. The [id-translation](https://pypi.org/project/id-translation/) suite \n(installed separately) relies heavily on [rics.mapping][mapping], as well as a number of other functions provided herein.\n\n## Highlighted Features\n- Multivariate [performance testing][perf].\n- Highly configurable [element mapping][mapping];\n  - Provides a wide variety of filtering, scoring and heuristic functions. \n  - Powers Name-to-source mapping for the [id-translation](https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html#name-to-source-mapping) \n    suite (installed separately).\n- Various other [utilities][utility], ranging from [logging] to [plotting] to specialized [dict] functions.\n- Temporal folds ([compatible with sklearn][time-fold]) for heterogeneous `pandas` types, meant for time-series cross validation.\n\n[perf]: https://rics.readthedocs.io/en/stable/_autosummary/rics.performance.html#rics.performance.run_multivariate_test\n[perf-plot]: https://rics.readthedocs.io/en/stable/_autosummary/rics.performance.html#rics.performance.plot_run\n\n[mapping]: https://rics.readthedocs.io/en/stable/_autosummary/rics.mapping.html\n\n[utility]: https://rics.readthedocs.io/en/stable/_autosummary/rics.misc.html\n[logging]: https://rics.readthedocs.io/en/stable/_autosummary/rics.logs.html\n[plotting]: https://rics.readthedocs.io/en/stable/_autosummary/rics.plotting.html\n[dict]: https://rics.readthedocs.io/en/stable/_autosummary/rics.collections.dicts.html\n[time-fold]: https://rics.readthedocs.io/en/stable/_autosummary/rics.pandas.html#rics.pandas.TimeFold.make_sklearn_splitter\n\n## Installation\nThe package is published through the [Python Package Index (PyPI)]. Source code\nis available on GitHub: https://github.com/rsundqvist/rics\n\n```sh\npip install -U rics\n```\n\nThis is the preferred method to install ``rics``, as it will always install the\nmost recent stable release.\n\nIf you don\'t have [pip] installed, this [Python installation guide] can guide\nyou through the process.\n\n## License\n[MIT](LICENSE.md)\n\n## Documentation\nHosted on Read the Docs: https://rics.readthedocs.io\n\n## Contributing\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. To get \nstarted, see the [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).\n\n[Python Package Index (PyPI)]: https://pypi.org/project/rics\n[pip]: https://pip.pypa.io\n[Python installation guide]: http://docs.python-guide.org/en/stable/starting/installation/\n',
    'author': 'Richard Sundqvist',
    'author_email': 'richard.sundqvist@live.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rsundqvist/rics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
