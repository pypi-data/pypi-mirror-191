# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_analytics']

package_data = \
{'': ['*'], 'git_analytics': ['static/*', 'static/css/*', 'static/js/*']}

install_requires = \
['GitPython>=3.1.30,<4.0.0', 'falcon>=3.1.1,<4.0.0']

setup_kwargs = {
    'name': 'git-analytics',
    'version': '0.1.0',
    'description': 'The detailed analysis tool for git repositories.',
    'long_description': '# Git-Analytics\n\nThe detailed analysis tool for git repositories.\n\n## Installation\n\nThe latest stable version can be installed directly from PyPI:\n\n```sh\npip install git-analytics\n```\n\n## Usage\n\nTo run, enter the command and open the browser at [http://localhost:8000/](http://localhost:8000/).\n\n```sh\ngit-analytics\n```\n\n## Screenshots\n\n![screenshot 1](https://live.staticflickr.com/65535/52679528807_48caac329f_k.jpg)\n\n![screenshot 2](https://live.staticflickr.com/65535/52680543193_c676158df2_k.jpg)\n\n![screenshot 3](https://live.staticflickr.com/65535/52679528732_1f7b9351cd_k.jpg)\n',
    'author': 'n0rfas',
    'author_email': 'antsa@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.7.15',
}


setup(**setup_kwargs)
