# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['i21y', 'i21y.loaders']

package_data = \
{'': ['*']}

extras_require = \
{'fast-json': ['orjson>=3.8.6,<4.0.0'], 'yaml': ['pyyaml>=6.0,<7.0']}

setup_kwargs = {
    'name': 'i21y',
    'version': '0.1.0b3',
    'description': 'The library for i18n support.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/i21y)](https://pypi.org/project/i21y/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/i21y) ![PyPI - Downloads](https://img.shields.io/pypi/dm/i21y) ![PyPI - License](https://img.shields.io/pypi/l/i21y) [![Documentation Status](https://readthedocs.org/projects/i21y/badge/?version=latest)](https://i21y.readthedocs.io/en/latest/?badge=latest) [![Buy Me a Coffee](https://img.shields.io/badge/-tasuren-E9EEF3?label=Buy%20Me%20a%20Coffee&logo=buymeacoffee)](https://www.buymeacoffee.com/tasuren)\n# i21y\ni21y (a.k.a internationalization.py) is library for support i18n in Python. It is easy to use.\n\n**WARNING**  \nIt is still in beta.\n\n## Installation\nNormal: `pip install i21y`  \nYAML supported: `pip install i21y[yaml]`  \nFast JSON (orjson) supported: `pip install i21y[fast-json]`\n\n## Example\n```python\nfrom i21y import Translator\nfrom i21y.loaders.json import Loader\n\nt = Translator(Loader("locale"))\n\nassert t("main.responses.not_found", locale="ja") == "見つからなかった。"\n```\n\n## Documentation\nSee the [documentation](https://i21y.readthedocs.io/) for usage and details.\n\n## License\ni21y is licensed under the [MIT license](https://github.com/tasuren/i21y/blob/main/LICENSE).',
    'author': 'Takagi Tasuku',
    'author_email': 'tasuren@outlook.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
