# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obiba_mica']

package_data = \
{'': ['*']}

install_requires = \
['pycurl>=7.45.2,<8.0.0']

entry_points = \
{'console_scripts': ['mica = obiba_mica.console:run']}

setup_kwargs = {
    'name': 'obiba-mica',
    'version': '5.0.0',
    'description': 'OBiBa/Mica python client.',
    'long_description': '# Mica Python [![Build Status](https://app.travis-ci.com/obiba/mica-python-client.svg?branch=master)](https://app.travis-ci.com/github/obiba/mica-python-client)\n\nThis Python-based command line tool allows to access to a Mica server through its REST API. This is the perfect tool\nfor automating tasks in Mica. This will be the preferred client developed when new features are added to the REST API.\n\n* Read the [documentation](http://micadoc.obiba.org).\n* Have a bug or a question? Please create an issue on [GitHub](https://github.com/obiba/mica-python-client/issues).\n* Continuous integration is on [Travis](https://travis-ci.org/obiba/mica-python-client).\n\n## Usage\n\nInstall with:\n\n```\npip install obiba-mica\n```\n\nTo get the options of the command line:\n\n```\nmica --help\n```\n\nThis command will display which sub-commands are available. For each sub-command you can get the help message as well:\n\n```\nmica <subcommand> --help\n```\n\nThe objective of having sub-command is to hide the complexity of applying some use cases to the Mica REST API. More\nsub-commands will be developed in the future.\n\n## Development\n\nMica Python client can be easily extended by using the classes defined in `core.py` file.\n\n## Mailing list\n\nHave a question? Ask on our mailing list!\n\nobiba-users@googlegroups.com\n\n[http://groups.google.com/group/obiba-users](http://groups.google.com/group/obiba-users)\n\n## License\n\nOBiBa software are open source and made available under the [GPL3 licence](http://www.obiba.org/pages/license/). OBiBa software are free of charge.\n\n## OBiBa acknowledgments\n\nIf you are using OBiBa software, please cite our work in your code, websites, publications or reports.\n\n"The work presented herein was made possible using the OBiBa suite (www.obiba.org), a  software suite developed by Maelstrom Research (www.maelstrom-research.org)"\n',
    'author': 'Yannick Marcon',
    'author_email': 'yannick.marcon@obiba.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
