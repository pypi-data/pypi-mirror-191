# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rename_kicad_project']

package_data = \
{'': ['*']}

install_requires = \
['pyproject-flake8>=0.0.1-alpha.2,<0.0.2',
 'rich>=10.16.0,<11.0.0',
 'typer[all]>=0.4.0,<0.5.0',
 'typing-extensions>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['rename-kicad-project = rename_kicad_project.cli:app']}

setup_kwargs = {
    'name': 'rename-kicad-project',
    'version': '1.1.0',
    'description': 'A nifty tool for renaming or cloning your KiCad project.',
    'long_description': "# rename-kicad-project\n[![PyPI version](https://badge.fury.io/py/rename-kicad-project.svg)](https://badge.fury.io/py/rename-kicad-project)\n[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/rename-kicad-project.svg)](https://pypi.python.org/pypi/rename-kicad-project/)\n[![CI](https://github.com/likeablob/rename-kicad-project/actions/workflows/ci.yml/badge.svg)](https://github.com/likeablob/rename-kicad-project/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/likeablob/rename-kicad-project/branch/main/graph/badge.svg)](https://codecov.io/gh/likeablob/rename-kicad-project)\n\n**rename-kicad-project** is a nifty tool for renaming or cloning your KiCad (v4, v5) project.\n\n## NOTE: From KiCad v6, renaming/cloning has been officially supported. Try `File -> Save As...`.\n\n## Install\n```sh\npython3 -m pip install --user rename-kicad-project\n```\nOr with [pipx](https://github.com/pypa/pipx),\n```sh\npipx install rename-kicad-project\n```\n\n## Usage\n```sh\n# Show helps\nrename-kicad-project --help\n\n# Show helps of `rename` sub-command (see below)\nrename-kicad-project rename --help\n```\nOr you can invoke this tool by \n```sh\npython3 -m rename_kicad_project --help\n```\n\n## `rename`\nIn the following example, `../foo/old_project_name{.pro, .sch, ...}` will be renamed as `../foo/new_project_name.pro`, ..., respectively.\n```sh\nrename-kicad-project rename ../foo new_project_name\n\n# ls ../foo\n# new_project_name.pro new_project_name.sch, ...\n```\nYou may want to run the command above with `--dry-run` (`-n`) beforehand;\n```sh\nrename-kicad-project -n rename ../foo new_project_name\n# Renaming: /path/to/old_project_name.kicad_pcb as new_project_name.kicad_pcb\n# ...\n```\n\n## `clone`\nIn the following example, `./foo/old_project_name{.pro, .sch, ...}` will be cloned into `/tmp/bar/new_project_name.pro`, ..., respectively.\n```sh\nrename-kicad-project clone ./foo /tmp/bar -p new_project_name\n\n# ls /tmp/bar\n# new_project_name.pro new_project_name.sch, ...\n```\nYou can omit `-p` to let the tool infer the new project name like `/tmp/bar/bar.pro`.\n```sh\nrename-kicad-project clone ./foo /tmp/bar\n\n# ls /tmp/bar\n# bar.pro bar.sch, ...\n```\nNote that `/tmp/bar` will be automatically created if it doesn't exist.  \nAnd as you expected, `--dry-run` also works with `clone`.\n\n## How it works\nFor the folks who wouldn't want to rely on someone's script, here is a basic explanation of how this tool works;\n1. In the given source directory, glob `*.pro` files and based on the first found one, determine the current project name. (`${PROJECT_NAME}.pro`)\n2. Determine target files with globbing `${PROJECT_NAME}.*` and including some special files like `fp-lib-table`.\n3. Rename the target files in place (`rename`) or copy the files into the specified destination (`clone`). That' it!\n\n## License\nMIT\n\n## Alternatives\n- https://github.com/bobc/KiRename\n  - As of 2021-12, it only runs on Python 2.\n",
    'author': 'likeablob',
    'author_email': '46628917+likeablob@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/likeablob/rename-kicad-project',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
