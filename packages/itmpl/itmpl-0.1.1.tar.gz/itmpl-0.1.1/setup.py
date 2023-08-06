# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itmpl',
 'itmpl.templates.mkdocs-material-site',
 'itmpl.templates.mkdocs-material-site.docs',
 'itmpl.templates.poetry-project',
 'itmpl.templates.poetry-project.tests',
 'itmpl.templates.poetry-project.{{ project_name }}']

package_data = \
{'': ['*'],
 'itmpl.templates.mkdocs-material-site.docs': ['static/images/*',
                                               'stylesheets/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'rich>=13.3.1,<14.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['itmpl = itmpl.main:app']}

setup_kwargs = {
    'name': 'itmpl',
    'version': '0.1.1',
    'description': 'A project templating and scaffolding tool',
    'long_description': '![iTmpl Logo](https://isaacharrisholt.github.io/itmpl/static/images/itmpl-logo.png)\n\n<p align="center">\n    <em>iTmpl. A flexible, powerful project templating tool, written in Python.</em>\n</p>\n\n---\n\n**Documentation:** <https://itmpl.ihh.dev>\n\n**Source:** <https://github.com/isaacharrisholt/itmpl>\n\n---\n\niTmpl is a project templating tool that allows you to create and manage project\ntemplates. iTmpl is written in Python and is cross-platform.\n\nIt comes with some default templates, but you can also create your own. iTmpl\nalso allows you to run arbitrary Python code before and after the templating\nprocess, allowing you to do things like create a git repository, or install\ndependencies.\n\n## Installation\n\nAlthough iTmpl has a well-documented API, its primary aim it to be a command\nline tool. As such, the recommended installation method is via\n[`pipx`](https://pypa.github.io/pipx/):\n\n```bash\npipx install itmpl\n```\n\nHowever, you can also install iTmpl via `pip`, if you prefer:\n\n```bash\npip install itmpl\n```\n\n## Quick Start\n\nTo see available project templates, run:\n\n```bash\nitmpl list\n```\n\nTo create a new project from a template, run:\n\n```bash\nitmpl new <template> <project-name> [options]\n```\n\nFor example, to create a new Poetry project, run:\n\n```bash\nitmpl new poetry-project my-new-project\n```\n\n## Adding Custom Templates\n\nCustom templates are stored in an `extra_templates_dir` specified in the iTmpl\nconfiguration file. To find the default location for your machine, run:\n\n```bash\nitmpl config show extra_templates_dir\n```\n\nTo change the location of the `extra_templates_dir`, run:\n\n```bash\nitmpl config set extra_templates_dir <path>\n```\n\nTo create a new template, simple create a new directory in the\n`extra_templates_dir`. iTmpl will automatically detect the new template, and\nshow it in the list of available templates.\n\nTemplates can be configured through `.itmpl.toml` and `.itmpl.py` files. See\nthe\n[documentation](https://itmpl.ihh.dev/using_custom_templates)\nfor more details.\n\n## Contributing\n\nContributions are welcome! If you find a bug, or have a feature request, please\nopen a new issue. If you would like to contribute code, please open a new pull\nrequest.\n\nI\'m always open to new templates too! I don\'t know every possible use case for\nthis tool, so I\'ve only included a few templates that I thought would be useful\nto me. If you have a template that you think would be useful to others, please\nopen a new issue, or submit a pull request!',
    'author': 'Isaac Harris-Holt',
    'author_email': 'isaac@harris-holt.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://itmpl.ihh.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
