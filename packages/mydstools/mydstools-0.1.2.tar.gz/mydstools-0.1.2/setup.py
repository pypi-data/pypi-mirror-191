# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mydstools', 'mydstools.connectors']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'simple-salesforce>=1.12.3,<2.0.0']

setup_kwargs = {
    'name': 'mydstools',
    'version': '0.1.2',
    'description': 'Data Science Toolbox',
    'long_description': '# mydstools\n\n`mydstools`: **Data Science Toolbox**\n\nFollow the project on:\n\n* [Github](https://github.com/antobzzll/mydstools)\n* [PyPI](https://pypi.org/project/mydstools/)\n\n## Installation\n\n```bash\n$ pip install mydstools\n```\n\n## Usage\n\nFor a complete usage guide, please refer to the [example notebook](docs/example.ipynb).\n\n## Contributing\n\nInterested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`mydstools` was created by Antonio Buzzelli. It is licensed under the terms of the [MIT license](LICENSE).\n\n## Credits\n\n`mydstools` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Antonio Buzzelli',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
