# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gregtech',
 'gregtech.flow',
 'gregtech.flow.graph',
 'gregtech.flow.gtnh',
 'gregtech.flow.recipe']

package_data = \
{'': ['*'], 'gregtech.flow': ['resources/*']}

install_requires = \
['fastjsonschema>=2.16.2,<3.0.0',
 'graphviz>=0.20.1,<0.21.0',
 'prompt-toolkit>=3.0.36,<4.0.0',
 'rich>=13.0.0,<14.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'sympy>=1.11.1,<2.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['flow = gregtech.__main__:run_cli']}

setup_kwargs = {
    'name': 'gregtech-flow',
    'version': '1.0.0',
    'description': 'YAML Driven Flowcharts for Gregtech: New Horizons',
    'long_description': '<p></p>\n<p align="center"><img src="https://raw.githubusercontent.com/velolib/gregtech-flow/master/assets/gt_flow.png"/></p>\n<br>\n<p align="center">\n    <a href="https://pypi.org/project/gregtech-flow/">\n        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/gregtech.flow?style=for-the-badge">\n    </a>\n    <a href="https://pypi.org/project/gregtech-flow/" >\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/gregtech-flow?style=for-the-badge">\n    </a>\n    <a href="https://github.com/velolib/gregtech-flow/blob/master/LICENSE.txt" >\n        <img src="https://img.shields.io/github/license/velolib/gregtech-flow?style=for-the-badge" alt="License MIT"/>\n    </a>\n    <a href="https://codecov.io/github/velolib/gregtech-flow" >\n        <img src="https://img.shields.io/codecov/c/github/velolib/gregtech-flow?style=for-the-badge&token=Y59FTD1UC1" alt="Code Coverage"/>\n    </a>\n    <a href="https://velolib.github.io/gregtech-flow/">\n        <img alt="GitHub deployments" src="https://img.shields.io/github/deployments/velolib/gregtech-flow/github-pages?label=deployment&style=for-the-badge">\n    </a>\n</p>\n<p></p>\n\n## ❓ What is it?\n<img align="right" width="192" height="192" src="https://raw.githubusercontent.com/velolib/gregtech-flow/master/assets/logo_512x.png"/>\n\nThis is a fork of OrderedSet86\'s [gtnh-flow](https://github.com/OrderedSet86/gtnh-flow). In addition to the functionalities of the original tool, this fork has:\n1. Extended formatting of projects\n2. Added stylization add formatting of graphs\n3. Standards to increase readability\n4. A custom command line interface\n5. Full documentation\n\nTo view the full documentation see the official [GT: Flow website](https://velolib.github.io/gregtech-flow/).\n\n## 📖 Samples\nSamples of the graphs included in the repository.\n<details>\n    <summary><strong>Samples</strong></summary>\n    <img src="https://raw.githubusercontent.com/velolib/gregtech-flow/c5f8a9e02e2a1f2f84ab92f0ce28d2a6c3e620cc/samples/rutile-titanium.svg" alt="Rutile -> Titanium">\n    <img src="https://raw.githubusercontent.com/velolib/gregtech-flow/c5f8a9e02e2a1f2f84ab92f0ce28d2a6c3e620cc/samples/epoxid.svg" alt="Epoxid">\n</details>',
    'author': 'velolib',
    'author_email': 'vlocitize@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://velolib.github.io/gregtech-flow',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
