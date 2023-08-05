# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evidence_ext']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.0,<7.0.0',
 'click>=8.1.3,<9.0.0',
 'meltano.edk>=0.3.0,<0.4.0',
 'nodejs-bin[cmd]>=18.4.0a4,<19.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['evidence_extension = evidence_ext.main:app']}

setup_kwargs = {
    'name': 'evidence-ext',
    'version': '0.4.0',
    'description': '`evidence-ext` is a Meltano utility extension.',
    'long_description': '# evidence-ext\n\n`evidence-ext` is A Meltano utility extension for [Evidence.dev](https://evidence.dev) 📊\n\n## Testing with Meltano\n\nThis extension includes a sample Evidence project, along with a `meltano.yml` project file, allowing you to test Evidence with Meltano.\n\n```shell\n# install the Meltano project locally\nmeltano install\n# run evidence in dev mode\nmeltano invoke evidence dev\n# build the example evidence project\nmeltano invoke evidence build\n```\n\n## Installing this extension for local development\n\n1. Install the project dependencies with `poetry install`:\n\n```shell\ncd path/to/your/project\npoetry install\n```\n\n2. Verify that you can invoke the extension:\n\n```shell\npoetry run evidence_extension --help\npoetry run evidence_extension describe --format=yaml\npoetry run evidence_invoker --help # if you have are wrapping another tool\n```\n\n## Template updates\n\nThis project was generated with [copier](https://copier.readthedocs.io/en/stable/) from the [Meltano EDK template](https://github.com/meltano/edk).\nAnswers to the questions asked during the generation process are stored in the `.copier_answers.yml` file.\n\nRemoving this file can potentially cause unwanted changes to the project if the supplied answers differ from the original when using `copier update`.\n',
    'author': 'Ken Payne',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
