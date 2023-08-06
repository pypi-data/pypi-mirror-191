# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynkets']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=65.6.3,<66.0.0', 'wheel>=0.38.4,<0.39.0']

setup_kwargs = {
    'name': 'asynkets',
    'version': '0.1.2',
    'description': '',
    'long_description': "\n# asynkets\n\n`asynkets` is a Python library which provides miscellaneous utilities that are useful when writing `asyncio` code.\n\nProvided utilities include:\n\n- *`Switch`*: A class that allows waiting for state changes of a switch that can be turned on or off. It provides async methods for waiting until it is in a specific state, and for waiting until it switches to a different state.\n- *`EventfulCounter`*: A counter that can be incremented or decremented and has optional minimum and maximum values. It also provides async methods for waiting until some threshold (either low or high) is reached, or until some threshold is reached or left, by leveraging Switches.\n- *`Fuse`*: Similar to asyncio's Event, but can only be set once.\n- *`Pulse`*: A pulse that can be triggered and waited for. It can also be given a function to call when it is triggered and can be used as an async iterator.\n- *`PeriodicPulse`*: A pulse that fires periodically at a specified interval and delay. It can be closed and used as an async iterator like the Pulse class.\n- *`ensure_coroutine_function`* and *`ensure_async_iterator`*: return guaranteed async versions of a sync or async function or iterable, respectively. If the function or iterable is synchronous, it will be wrapped to be async; if it is already async, it will be returned as-is.\n- *`merge_async_iterables`*: Merges multiple iterables or async iterables into one, yielding items as they are received.\n\n\n## Installation\n\n`asynkets` is available on PyPI and can be installed with `pip` or your favorite package manager.\n\n```bash\npip install asynkets\n```\n\n## Usage\n\n(todo)\n\n## License\n\nThe library is provided under the MIT license. See the [LICENSE](LICENSE) file for more information.\n",
    'author': 'Pedro Batista',
    'author_email': 'pedrovhb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
