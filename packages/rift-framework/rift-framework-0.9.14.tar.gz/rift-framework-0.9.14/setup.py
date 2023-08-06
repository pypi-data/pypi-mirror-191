# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rift',
 'rift.ast',
 'rift.ast.patchers',
 'rift.ast.types',
 'rift.bases',
 'rift.cli',
 'rift.cli.commands',
 'rift.cli.util',
 'rift.core',
 'rift.cst',
 'rift.fift',
 'rift.fift.types',
 'rift.func',
 'rift.func.types',
 'rift.keys',
 'rift.keys.mnemonic',
 'rift.keys.mnemonic.bip39',
 'rift.library',
 'rift.logging',
 'rift.meta',
 'rift.native',
 'rift.network',
 'rift.runtime',
 'rift.types',
 'rift.types.bases',
 'rift.util',
 'rift.wallet']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<6.1',
 'appdirs>=1.4.4,<1.5.0',
 'astpretty>=3.0.0,<3.1.0',
 'click>=8.1.3,<8.2.0',
 'colorful>=0.5.4,<0.6.0',
 'cryptography>=39.0.0,<40.0.0',
 'libcst>=0.4.7,<0.5.0',
 'pynacl>=1.5.0,<2.0.0',
 'rich>=13.3.1,<14.0.0',
 'rift-tonlib>=0.0.3,<0.0.4',
 'setuptools>=65.6.3,<66.0.0',
 'tomlkit>=0.11.4,<0.12.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['rift = rift.cli.entry:entry']}

setup_kwargs = {
    'name': 'rift-framework',
    'version': '0.9.14',
    'description': 'The magical Python -> TON Portal',
    'long_description': '<img align="left" width="64" height="64" src="https://github.com/sky-ring/rift/blob/main/assets/rift-icon.png">\n\n# Rift\n\n[![PyPI version](https://img.shields.io/badge/rift--framework-0.9.14-informational?style=flat-square&color=FFFF91&labelColor=360825)](https://pypi.org/project/rift-framework/)\n[![Telegram](https://img.shields.io/badge/Telegram-@skyring__org-informational?style=flat-square&color=0088cc&labelColor=360825)](https://t.me/skyring_org)\n[![Telegram](https://img.shields.io/badge/Docs-docs.skyring.io/rift-informational?style=flat-square&color=6A0F49&labelColor=360825)](https://docs.skyring.io/rift/)\n\n> _A magical **Python3** -> **TON** portal_\n\nRift is a full-stack development framework for [TON (The Open Network)](https://ton.org) that makes it easy for developers to use Python to develop, test, and deploy smart contracts on the TON network. With Rift, you can leverage the simplicity and versatility of Python to build and interact with TON, without having to learn the complexities of FunC or Fift. For examples of how Rift simplifies these processes, visit [Rift\'s website](https://rift.skyring.io).\n\n## Features\n\n- Develop smart contracts using Python syntax and OOP features\n- Interact with the TON network to query data and deploy contracts\n- Test smart contracts with an easy-to-use testing framework\n- Standalone framework that only requires `Python 3.10`\n- Can be used at any stage of the project, from development to testing to deployment\n\n## Quick Start\n\n0. Install `Python 3.10+`\n1. Install `rift`\n    ```bash\n    pip install rift-framework\n    # or from source\n    git clone https://github.com/sky-ring/rift\n    cd rift\n    pip install -e .\n    ```\n2. Initialize your project:\n    ```bash\n    rift init <project-name>\n    ```\n3. Develop your contracts in `<project>/contracts/`\n4. Write your tests in `<project>/tests/`\n5. Place your deploy scripts in `<project>/deployers/`\n6. Use `rift` to build, test, or deploy:\n    ```bash\n    # in project folder\n    # builds TARGET\n    rift build TARGET\n    # tests TARGET\n    rift test TARGET\n    # deploys TARGET\n    rift deploy TARGET\n    ```\n7. For more information, visit the documentation website at [docs.skyring.io/rift](https://docs.skyring.io/rift).\n\n## Guides\n\n- Step-by-step guide on how to use `Rift` to develop on TON: [Link](https://rift.skyring.io/guide-full)\n- Step-by-step guide on integrating `Rift` into existing `FunC` projects: [Link](https://rift.skyring.io/guide-func)\n\n## Standard Contracts Implementation\n- [x] Jetton Implementation ([jettons](https://github.com/sky-ring/jettons))\n- [ ] NFT Implementation\n- [ ] DEX Implementation\n\n\n## Roadmap\n\n### Milestone 1: Python Framework for Contract Development\n- [x] Semi One-to-One Mapping of Functions and Expressions (Base Compiler, Python -> FunC)\n- [x] First Higher Layer over the Base Mappings to Simplify Type Calls (leveraging OOP Capabilities)\n- [x] Second Higher Layer over the Base, Simplifying Contract Development towards Maximizing Code Reusability and Simplicity (leveraging Meta Programming Capabilities)\n- [x] Providing Standard Smart Contracts Implementation with Rift\n\n### Milestone 2: Deploying, Testing, Interaction Capabilities\n- [x] Simple Interaction Interface with TON Blockchain\n- [x] Simple Deploying Options of Developed Contracts\n- [x] Testing Framework for the Contracts Developed with Rift\n\n### Milestone 3: What\'s Next?\n- Stay Tuned! We have extra plans that we will share soon with the community to further develop `Rift`.\n\n## Support the Project\n1. If `Rift` has been a lifesaver for you, giving it a star on GitHub is the ultimate high five!\n2. You can also show your love by contributing to `Rift` through code, ideas, or even a kind word.\n3. Feeling extra generous? Treat `Rift` to a coffee by donating to this TON address: `EQAIhZCDT7-pvweWh6c_76X7Dnv6Qlzt7-l1NNP8upZ_Areu`\n4. Finally, spreading the word about `Rift` is a big boost for the project and helps us reach more people.\n\n## Contributing\nIf you\'re interested in contributing to Rift, please see [CONTRIBUTING.md](https://github.com/sky-ring/rift/blob/main/CONTRIBUTING.md) for the necessary specifications and procedures.\n\n## Supporters\nSpecial thanks to the [TON Society](https://society.ton.org/) for their support and grant, without which the project would not be feasible.\n',
    'author': 'Amin Rezaei',
    'author_email': 'AminRezaei0x443@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
