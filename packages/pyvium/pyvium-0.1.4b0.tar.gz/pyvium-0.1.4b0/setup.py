# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvium', 'pyvium.errors', 'pyvium.util']

package_data = \
{'': ['*']}

install_requires = \
['cffi>=1.15.1,<2.0.0']

setup_kwargs = {
    'name': 'pyvium',
    'version': '0.1.4b0',
    'description': 'A tiny Python wrapper around the <Software development driver DLL> for IviumSoft.',
    'long_description': '# PYVIUM\n\nTiny Python wrapper around the "Software development driver DLL" for IviumSoft.\n\n# Important:\n\nThis module uses a dll from the IviumSoft application. You need to have this software installed on a Windows machine. The IviumSoft application can be downloaded from here: https://www.ivium.com/support/#Software%20update\n\nThis version of Pyvium has been tested for IviumSoft release 4.1100.\n\n## Installation\n\nInstall PYVIUM easily with pip:\n\n```\npip install pyvium\n```\n\nOr with poetry:\n\n```\npoetry add pyvium\n```\n\n## Usage Example (Using IviumSoft Core functions)\n\nTo use the same functions available in the "IviumSoft driver DLL" you can import the Core class as follows. All functions return a result code (integer) and a result value if available. For further information you can check the IviumSoft documentation.\n\n```\nfrom pyvium import Core\n\nCore.IV_open()\nCore.IV_getdevicestatus()\nCore.IV_close()\n```\n\n## Usage Example (Using Pyvium methods)\n\nThis is a wrapper around the Core functions that adds a few things:\n\n- Exception management (you can find an example [here](https://github.com/SF-Tec/pyvium/blob/main/docs/error_management.md))\n- New functionalities\n\n```\nfrom pyvium import Pyvium\n\nPyvium.open_driver()\nPyvium.get_device_status()\nPyvium.close_driver()\n\n```\n\n## Supported functions\n\nThe list of currently supported and implemented functions can be found [here](https://github.com/SF-Tec/pyvium/blob/main/docs/method_list.md).\n\n## Links\n\n- [See on GitHub](https://github.com/sf-tec/pyvium)\n- [See on PyPI](https://pypi.org/project/pyvium)\n',
    'author': 'Alejandro Gutiérrez',
    'author_email': 'agutierrez@stec.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SF-Tec/pyvium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
