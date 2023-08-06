# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitflux']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pygithub>=1.57,<2.0']

entry_points = \
{'console_scripts': ['gitflux = gitflux.__main__:cli']}

setup_kwargs = {
    'name': 'gitflux',
    'version': '0.2.0',
    'description': 'A command-line utility to help you manage Git repositories.',
    'long_description': '# gitflux\n\n**gitflux** is a command-line utility to help you manage Git repositories.\n\n## License\n\nCopyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>\n\nThe GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).\n',
    'author': 'HE Yaowen',
    'author_email': 'he.yaowen@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
