# Mkdocs Bulma Classes Plugin

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Add support to [Bulma CSS framework](https://bulma.io) in [Mkdocs](https://www.mkdocs.org).

Inspired by [mkdocs-bootstrap-tables-plugin](https://github.com/byrnereese/mkdocs-bootstrap-tables-plugin/blob/master/mkdocs_bootstrap_tables_plugin/plugin.py).

This plugin inject first in the Markdown of the page and then in the raw html elements produced by Mkdocs from Markdown all necessary classes for styling with Bulma framework. I'll try to follow in the most pedantic way the last [CommonMark](https://commonmark.org/) specification released before supporting other versions.

**Table of Contents**:

- [How to Install](#how-to-install)
- [How to use](#how-to-use)
- [See also](#see-also)

## How to Install

Use pip to install the plugin (or use your preferred dep manager for Python, like [Poetry](https://python-poetry.org/) for me):

    pip install mkdocs-bulma-classes-plugin

## How to use

Activate the plugin in your `mkdocs.yml` config file:

    plugins:
      - bulma-classes

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

You doesn't need to do anything. When you build your docs with Mkdocs, after HTML page generation, this pluging inject in your tags the proper CSS class for Bulma. For example, your `# Heading 1` will produce the following HTML code:

    <h1 id="heading-1">Heading 1</h1>

but enabling this plugin will produce this:

    <h1 id="heading-1" class="title is-1">Heading 1</h1>

necessary for Bulma to render this title:

![Bulma title is-1](docs/img/bulma_heading_1.png)

For more info, look at [docs](https://daniele-tentoni.github.io/mkdocs-bulma-classes-plugin).

## See also

Take a look at my [Bulma Theme](https://github.com/daniele-tentoni/mkdocs-bulma-theme) for Mkdocs.

## Contributing

Contributions are welcome.
