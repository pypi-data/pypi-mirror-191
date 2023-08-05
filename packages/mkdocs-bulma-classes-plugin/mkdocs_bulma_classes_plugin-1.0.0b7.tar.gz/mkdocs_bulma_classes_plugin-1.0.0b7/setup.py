# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_bulma_classes_plugin', 'mkdocs_bulma_classes_plugin.regexs']

package_data = \
{'': ['*']}

entry_points = \
{'mkdocs.plugins': ['bulma-classes = '
                    'mkdocs_bulma_classes_plugin.plugin:BulmaClassesPlugin']}

setup_kwargs = {
    'name': 'mkdocs-bulma-classes-plugin',
    'version': '1.0.0b7',
    'description': 'Add support to Bulma css framework in Mkdocs',
    'long_description': '# Mkdocs Bulma Classes Plugin\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nAdd support to [Bulma CSS framework](https://bulma.io) in [Mkdocs](https://www.mkdocs.org).\n\nInspired by [mkdocs-bootstrap-tables-plugin](https://github.com/byrnereese/mkdocs-bootstrap-tables-plugin/blob/master/mkdocs_bootstrap_tables_plugin/plugin.py).\n\nThis plugin inject first in the Markdown of the page and then in the raw html elements produced by Mkdocs from Markdown all necessary classes for styling with Bulma framework. I\'ll try to follow in the most pedantic way the last [CommonMark](https://commonmark.org/) specification released before supporting other versions.\n\n**Table of Contents**:\n\n- [How to Install](#how-to-install)\n- [How to use](#how-to-use)\n- [See also](#see-also)\n\n## How to Install\n\nUse pip to install the plugin (or use your preferred dep manager for Python, like [Poetry](https://python-poetry.org/) for me):\n\n    pip install mkdocs-bulma-classes-plugin\n\n## How to use\n\nActivate the plugin in your `mkdocs.yml` config file:\n\n    plugins:\n      - bulma-classes\n\n> If you have no `plugins` entry in your config file yet, you\'ll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.\n\nYou doesn\'t need to do anything. When you build your docs with Mkdocs, after HTML page generation, this pluging inject in your tags the proper CSS class for Bulma. For example, your `# Heading 1` will produce the following HTML code:\n\n    <h1 id="heading-1">Heading 1</h1>\n\nbut enabling this plugin will produce this:\n\n    <h1 id="heading-1" class="title is-1">Heading 1</h1>\n\nnecessary for Bulma to render this title:\n\n![Bulma title is-1](docs/img/bulma_heading_1.png)\n\nFor more info, look at [docs](https://daniele-tentoni.github.io/mkdocs-bulma-classes-plugin).\n\n## See also\n\nTake a look at my [Bulma Theme](https://github.com/daniele-tentoni/mkdocs-bulma-theme) for Mkdocs.\n\n## Contributing\n\nContributions are welcome.\n',
    'author': 'Daniele Tentoni',
    'author_email': 'daniele.tentoni.1996@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://daniele-tentoni.github.io/mkdocs-bulma-classes-plugin',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
