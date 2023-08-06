# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['obsidian_to_latex']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'colored-traceback>=0.3.0,<0.4.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'pydantic>=1.10.4,<2.0.0']

entry_points = \
{'console_scripts': ['obsidian_to_latex = '
                     'obsidian_to_latex.obsidian_to_latex:main']}

setup_kwargs = {
    'name': 'obsidian-to-latex',
    'version': '0.1.4',
    'description': 'Convert Obsidian vault documents to latex',
    'long_description': '# Obsidian to Latex\n\nThis utility attempts to make it easy to convert markdown documents written using obsidian into PDFs.\n\n## Requirements\n\n- latex\n- mermaid\n\n## Getting Started\n\nThis project uses python [poetry](https://python-poetry.org/).  Follow the [intallation instructions](https://python-poetry.org/docs/#installation) for poetry.\n\nI\'m using miktex for latex support.  On windows, you can run `winget install miktex`\n\nRun `poetry install` and `poetry shell` to install and and activate the python virtual environment.\n\nThan, run `obsidian_to_latex .\\examples\\feature_guide\\Widget.md` to convert the example document to a PDF.  The PDF will be placed in `.\\examples\\feature_guide\\output\\Widget.pdf`.\n\n```powershell\nwatchexec.exe -crd500 -e py "isort . && black . && pytest && obsidian_to_latex.cmd .\\examples\\feature_guide\\Widget.md"\n```\n',
    'author': 'Ryan Bartling',
    'author_email': 'ryan.bartling@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drbartling/obsidian-to-latex',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
