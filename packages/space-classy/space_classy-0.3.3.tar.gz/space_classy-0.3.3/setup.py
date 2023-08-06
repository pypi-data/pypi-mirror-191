# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy']

package_data = \
{'': ['*'],
 'classy': ['data/*',
            'data/classy/*',
            'data/input/*',
            'data/mcfa/*',
            'data/mixnorm/*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'furo>=2022.9.15,<2023.0.0',
 'importlib-resources>=5.10.2,<6.0.0',
 'mcfa>=0.1,<0.2',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'rich>=12.2.0,<13.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'space-rocks>=1.7.2,<2.0.0',
 'sphinx-copybutton>=0.5.0,<0.6.0',
 'sphinx_design>=0.3.0,<0.4.0',
 'tox>=4.4.5,<5.0.0']

extras_require = \
{'docs': ['sphinx>=4,<5', 'sphinx-redactor-theme>=0.0.1,<0.0.2']}

entry_points = \
{'console_scripts': ['classy = classy.cli:cli_classy']}

setup_kwargs = {
    'name': 'space-classy',
    'version': '0.3.3',
    'description': 'classification tool for minor bodies using reflectance spectra and visual albedos',
    'long_description': '![PyPI](https://img.shields.io/pypi/v/space-classy) [![arXiv](https://img.shields.io/badge/arXiv-2203.11229-f9f107.svg)](https://arxiv.org/abs/2203.11229) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n<p align="center">\n  <img width="260" src="https://raw.githubusercontent.com/maxmahlke/classy/main/docs/gfx/logo_classy.png">\n</p>\n\nNote: The classification pipeline is implemented yet the user-interface is\nminimal so far. I am currently writing my PhD thesis and intend to make `classy`\nmore user-friendly in July / August of this year. For questions or issues, please use the [Issues](https://github.com/maxmahlke/classy/issues) page of this repository\nor contact me [via email](https://www.oca.eu/en/max-mahlke).\n\n[Features](#features) - [Install](#install) - [Documentation](#documentation) - [Data](#data) - [Development](#development)\n\n# Features\n\nClassify asteroids in the taxonomic scheme by [Mahlke, Carry, Mattei 2022](https://arxiv.org/abs/2203.11229).\n\n``` sh\n\n$ classy classify path/to/observations.csv\nINFO     Looks like we got 2 S, 1 Ee, 1 B, 1 X, 1 Q\n\n```\n\n# Install\n\n`classy` is available on the [python package index](https://pypi.org) as *space-classy*:\n\n``` sh\n$ pip install space-classy\n```\n\n# Documentation\n\nCheck out the documentation at [classy.readthedocs.io](https://classy.readthedocs.io/en/latest/).\nor run\n\n     $ classy docs\n\n# Data\n\nThe following data files are provided in this repository (format `csv` and `txt`) and at the CDS (format `txt`):\n\n| File `csv` | File `txt` |  Content | Description|\n|-----------|--------|----|------------|\n| `class_templates.csv` | `template.txt` | Class templates |  Mean and standard deviation of the VisNIR spectra and visual albedos for each class. |\n| `class_visnir.csv` | `classvni.txt` | Classifications of the VisNIR sample. |  Classes derived for the 2983 input observations used to derive the taxonomy. |\n| `class_vis.csv` | `classvis.txt` | Classifications of the vis-only sample. |  Classes derived for the 2923 input observations containing only visible spectra and albedos. |\n| `class_asteroid.csv` | `asteroid.txt` | Class per asteroid |  Aggregated classifications in VisNIR and vis-only samples with one class per asteroid. |\n| `ref_spectra.csv` | `refspect.txt` | References of spectra | The key to the spectra references used in the classification tables. |\n| `ref_albedo.csv` | `refalbed.txt` | References of albedos |  The key to the albedo references used in the classification tables. |\n\nMore information on each file can be found in the [data/ReadMe](https://github.com/maxmahlke/classy/blob/main/data/ReadMe).\n\n<!-- # Development -->\n<!---->\n<!-- To be implemented: -->\n<!---->\n<!-- - [ ] Graphical User Interface -->\n<!-- - [ ] Optional automatic addition of SMASS spectra to observations -->\n<!-- - [ ] Automatic determination of best smoothing parameters -->\n\n<!-- # Contribute -->\n\n<!-- Computation of asteroid class by weighted average -->\n',
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/maxmahlke/classy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
