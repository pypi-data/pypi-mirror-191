# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiecutter_poetry']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0']

entry_points = \
{'console_scripts': ['ccp = cookiecutter_poetry.cli:main']}

setup_kwargs = {
    'name': 'cookiecutter-poetry',
    'version': '0.5.3',
    'description': 'A python cookiecutter application to create a new python project that uses poetry to manage its dependencies.',
    'long_description': '\n\n<p align="center">\n  <img width="600" src="https://raw.githubusercontent.com/fpgmaas/cookiecutter-poetry/main/docs/static/cookiecutter.svg">\n</p style = "margin-bottom: 2rem;">\n\n---\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/cookiecutter-poetry)](https://pypi.org/project/cookiecutter-poetry/)\n[![Build status](https://img.shields.io/github/actions/workflow/status/fpgmaas/cookiecutter-poetry/main.yml?branch=main)](https://github.com/fpgmaas/cookiecutter-poetry/actions/workflows/main.yml?query=branch%3Amain)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/cookiecutter-poetry)](https://pypi.org/project/cookiecutter-poetry/)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://fpgmaas.github.io/cookiecutter-poetry/)\n[![License](https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry)](https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry)\n\n\nThis is a modern Cookiecutter template that can be used to initiate a Python project with all the necessary tools for development, testing, and deployment. It supports the following features:\n\n- [Poetry](https://python-poetry.org/) for dependency management\n- CI/CD with [GitHub Actions](https://github.com/features/actions)\n- Pre-commit hooks with [pre-commit](https://pre-commit.com/)\n- Code quality with [black](https://pypi.org/project/black/), [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), and [deptry](https://github.com/fpgmaas/deptry/)\n- Publishing to [Pypi](https://pypi.org) or [Artifactory](https://jfrog.com/artifactory) by creating a new release on GitHub\n- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)\n- Documentation with [MkDocs](https://www.mkdocs.org/)\n- Compatibility testing for multiple versions of Python with [Tox](https://tox.wiki/en/latest/)\n- Containerization with [Docker](https://www.docker.com/)\n\n---\n<p align="center">\n  <a href="https://fpgmaas.github.io/cookiecutter-poetry/">Documentation</a> - <a href="https://github.com/fpgmaas/cookiecutter-poetry-example">Example</a> -\n  <a href="https://pypi.org/project/cookiecutter-poetry/">PyPi</a>\n</p>\n\n---\n\n\n\n\n## Quickstart\n\nOn your local machine, navigate to the directory in which you want to\ncreate a project directory, and run the following two commands:\n\n``` bash\npip install cookiecutter-poetry \nccp\n```\n\nAlternatively, install `cookiecutter` and directly pass the URL to this\nGithub repository to the `cookiecutter` command:\n\n``` bash\npip install cookiecutter\ncookiecutter https://github.com/fpgmaas/cookiecutter-poetry.git\n```\n\nCreate a repository on GitHub, and then run the following commands, replacing `<project-name>`, with the name that you gave the Github repository and\n`<github_author_handle>` with your Github username.\n\n``` bash\ncd <project_name>\ngit init -b main\ngit add .\ngit commit -m "Init commit"\ngit remote add origin git@github.com:<github_author_handle>/<project_name>.git\ngit push -u origin main\n```\n\nFinally, install the environment and the pre-commit hooks with\n\n ```bash\n make install\n ```\n\nYou are now ready to start development on your project! The CI/CD\npipeline will be triggered when you open a pull request, merge to main,\nor when you create a new release.\n\nTo finalize the set-up for publishing to PyPi or Artifactory, see\n[here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).\nFor activating the automatic documentation with MkDocs, see\n[here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).\nTo enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).\n\n## Acknowledgements\n\nThis project is partially based on [Audrey\nFeldroy\\\'s](https://github.com/audreyfeldroy)\\\'s great\n[cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)\nrepository.\n',
    'author': 'Florian Maas',
    'author_email': 'fpgmaas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fpgmaas/cookiecutter-poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
