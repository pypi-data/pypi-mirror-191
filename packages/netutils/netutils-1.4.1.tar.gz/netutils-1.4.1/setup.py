# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netutils', 'netutils.config', 'netutils.data_files']

package_data = \
{'': ['*']}

extras_require = \
{'optionals': ['napalm>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'netutils',
    'version': '1.4.1',
    'description': 'Common helper functions useful in network automation.',
    'long_description': '# Netutils\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/networktocode/netutils/develop/docs/images/icon-Netutils.png" class="logo" height="200px">\n  <br>\n  <a href="https://github.com/networktocode/netutils/actions"><img src="https://github.com/networktocode/netutils/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n  <a href="https://netutils.readthedocs.io/en/latest"><img src="https://readthedocs.org/projects/netutils/badge/"></a>\n  <a href="https://pypi.org/project/netutils/"><img src="https://img.shields.io/pypi/v/netutils"></a>\n  <a href="https://pypi.org/project/netutils/"><img src="https://img.shields.io/pypi/dm/netutils"></a>\n  <br>\n</p>\n\n## Overview\n\nA Python library that is a collection of functions that are used in the common network automation tasks. Tasks such as converting a BGP ASN to and from dotted format, normalizing an interface name, or "type 5" encrypting a password. The intention is to centralize these functions while keeping the library light.\n\n## Documentation\n\nFull web-based HTML documentation for this library can be found over on the [Netutils Docs](https://netutils.readthedocs.io) website:\n\n- [User Guide](https://netutils.readthedocs.io/en/latest/user/lib_overview/) - Overview, Using the library, Getting Started.\n- [Administrator Guide](https://netutils.readthedocs.io/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the library.\n- [Developer Guide](https://netutils.readthedocs.io/en/latest/dev/contributing/) - Extending the library, Code Reference, Contribution Guide.\n- [Release Notes / Changelog](https://netutils.readthedocs.io/en/latest/admin/release_notes/).\n- [Frequently Asked Questions](https://netutils.readthedocs.io/en/latest/user/faq/).\n\n### Contributing to the Docs\n\nAll the Markdown source for the library documentation can be found under the [docs](https://github.com/networktocode/netutils/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient - clone the repository and edit away.\n\nIf you need to view the fully generated documentation site, you can build it with [mkdocs](https://www.mkdocs.org/). A container hosting the docs will be started using the invoke commands (details in the [Development Environment Guide](https://netutils.readthedocs.io/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). As your changes are saved, the live docs will be automatically reloaded.\n\nAny PRs with fixes or improvements are very welcome!\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](https://netutils.readthedocs.io/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#networktocode`), sign up [here](http://slack.networktocode.com/) if you don\'t have an account.\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://netutils.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
