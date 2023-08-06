# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corpus_sc_toolkit',
 'corpus_sc_toolkit.html',
 'corpus_sc_toolkit.justice',
 'corpus_sc_toolkit.meta',
 'corpus_sc_toolkit.pdf']

package_data = \
{'': ['*'],
 'corpus_sc_toolkit.justice': ['sql/*'],
 'corpus_sc_toolkit.pdf': ['sql/*']}

install_requires = \
['citation-docket>=0.1.1,<0.2.0',
 'httpx>=0.23.3,<0.24.0',
 'loguru>=0.6.0,<0.7.0',
 'markdownify>=0.11.6,<0.12.0',
 'pylts>=0.0.7,<0.0.8',
 'python-dotenv>=0.21,<0.22',
 'sqlpyd>=0.1.4,<0.2.0',
 'unidecode>=1.3.6,<2.0.0']

setup_kwargs = {
    'name': 'corpus-sc-toolkit',
    'version': '0.0.3',
    'description': 'Toolkit to process component elements of a Philippine Supreme Court decision.',
    'long_description': '# corpus-toolkit\n\n![Github CI](https://github.com/justmars/corpus-toolkit/actions/workflows/main.yml/badge.svg)\n\nToolkit to process component elements of a Philippine Supreme Court decision.\n\n## Development\n\nSee [documentation](https://justmars.github.io/corpus-toolkit).\n\n1. Run `poetry shell`\n2. Run `poetry update`\n3. Run `pytest`\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mv3.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
