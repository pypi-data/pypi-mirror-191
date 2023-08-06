# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['znflow']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0', 'networkx>=3.0,<4.0']

setup_kwargs = {
    'name': 'znflow',
    'version': '0.1.1',
    'description': '',
    'long_description': '[![zincware](https://img.shields.io/badge/Powered%20by-zincware-darkcyan)](https://github.com/zincware)\n[![Coverage Status](https://coveralls.io/repos/github/zincware/ZnFlow/badge.svg?branch=main)](https://coveralls.io/github/zincware/ZnFlow?branch=main)\n[![PyPI version](https://badge.fury.io/py/znflow.svg)](https://badge.fury.io/py/znflow)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zincware/ZnFlow/HEAD)\n\n# ZnFlow\n\nThe `ZnFlow` package provides a basic structure for building computational graphs based on functions or classes. It is designed as a lightweight abstraction layer to \n- learn graph computing.\n- build your own packages on top of it.\n\n## Installation\n```shell\npip install znflow\n```\n\n## Usage\n\n### Connecting Functions\n\nWith ZnFlow you can connect functions to each other by using the `@nodify` decorator. Inside the ``znflow.DiGraph`` the decorator will return a `FunctionFuture` object that can be used to connect the function to other nodes. The `FunctionFuture` object will also be used to retrieve the result of the function.\nOutside the ``znflow.DiGraph`` the function behaves as a normal function.\n```python\nimport znflow\n\n@znflow.nodify\ndef compute_mean(x, y):\n    return (x + y) / 2\n\nprint(compute_mean(2, 8))\n# >>> 5\n\nwith znflow.DiGraph() as graph:\n    mean = compute_mean(2, 8)\n\ngraph.run()\nprint(mean.result)\n# >>> 5\n\nwith znflow.DiGraph() as graph:\n    n1 = compute_mean(2, 8)\n    n2 = compute_mean(13, 7)\n    n3 = compute_mean(n1, n2)\n\ngraph.run()\nprint(n3.result)\n# >>> 7.5\n```\n\n### Connecting Classes\nIt is also possible to connect classes.\nThey can be connected either directly or via class attributes.\nThis is possible by returning ``znflow.Connections`` inside the ``znflow.DiGraph`` context manager.\nOutside the ``znflow.DiGraph`` the class behaves as a normal class.\n\nIn the following example we use a dataclass, but it works with all Python classes that inherit from ``znflow.Node``.\n\n```python\nimport znflow\nimport dataclasses\n\n@znflow.nodify\ndef compute_mean(x, y):\n    return (x + y) / 2\n\n@dataclasses.dataclass\nclass ComputeMean(znflow.Node):\n    x: float\n    y: float\n    \n    results: float = None\n    \n    def run(self):\n        self.results = (self.x + self.y) / 2\n        \nwith znflow.DiGraph() as graph:\n    n1 = ComputeMean(2, 8)\n    n2 = compute_mean(13, 7)\n    # connecting classes and functions to a Node\n    n3 = ComputeMean(n1.results, n2) \n    \ngraph.run()\nprint(n3.results)\n# >>> 7.5\n```\n',
    'author': 'zincwarecode',
    'author_email': 'zincwarecode@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
