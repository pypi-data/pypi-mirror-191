# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pitchmark', 'pitchmark.osm']

package_data = \
{'': ['*']}

install_requires = \
['osmium>=3.6.0,<4.0.0', 'shapely>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'pitchmark',
    'version': '0.1.0',
    'description': 'Exploring golf shot strategy.',
    'long_description': '# pitchmark\n\nExploring golf shot strategy.\n\n## Installation\n\n```bash\n$ pip install pitchmark\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pitchmark` was created by Istvan Kleijn. It is licensed under the terms of the MIT license.\n\n## Credits\n\nThe test suite includes raw map data from [OpenStreetMap](https://www.openstreetmap.org/copyright).\n\n`pitchmark` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Istvan Kleijn',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
