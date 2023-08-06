# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genome_seq_finder', 'genome_seq_finder.lib']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.80,<2.0',
 'duckdb>=0.6.1,<0.7.0',
 'fastapi>=0.89.1,<0.90.0',
 'pandas>=1.5.3,<2.0.0',
 'pytest>=7.2.1,<8.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['genome_seq_finder = genome_seq_finder.main:app']}

setup_kwargs = {
    'name': 'genome-seq-finder',
    'version': '0.1.0',
    'description': 'Generates sequence matches given FNA files and a regex expression',
    'long_description': '## Genome\n\nGiven a list of regex sequences look on FNA files for its match\n\n## Usage\n\n```shell\n\npython3 main.py data --output csv\n\n```\n\n## Install locally\n\nRequires having pipx and poetry\n\n```\npipx install poetry\npoetry install\ngenome\n```\n\n## Example sequences\n\nPlease check the [patterns file](./data/patterns.txt)\n',
    'author': 'José Cabeda',
    'author_email': 'jecabeda@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
