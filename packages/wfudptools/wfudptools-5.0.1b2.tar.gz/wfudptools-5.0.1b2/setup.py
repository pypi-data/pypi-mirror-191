# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wfudptools']

package_data = \
{'': ['*']}

install_requires = \
['certifi==2022.12.7',
 'charset-normalizer==3.0.1',
 'idna==3.4',
 'influxdb==5.3.1',
 'msgpack==1.0.4',
 'paho-mqtt==1.6.1',
 'python-dateutil==2.8.2',
 'pytz==2022.7.1',
 'requests==2.28.2',
 'six==1.16.0',
 'urllib3==1.26.14']

entry_points = \
{'console_scripts': ['wfudplistener = wfudptools.listener:main',
                     'wfudpsimulator = wfudptools.simulator:main']}

setup_kwargs = {
    'name': 'wfudptools',
    'version': '5.0.1b2',
    'description': 'WeatherFlow UDP API compliant python tools',
    'long_description': '## Description\n\nThese python3 utilities let you test (and simulate) a WeatherFlow station installation\n\nThey permit you to listen to UDP broadcasts from your Hub and:\n * print the received UDP broadcasts to stdout\n * print the decoded broadcasts in a more human-friendly form\n * publish derived topics to MQTT\n * publish derived topics to influxdb\n * support any combination of Air/Sky/Tempest\n * support multiple instances of Air/Sky/Tempest at your site\n\nThey also provide a utility to permit you to simulate a WeatherFlow Hub with minimal test data.\n\nNOTE - These utilities are tested using v119 of the WeatherFlow hub firmware.\n\n\n## Disclaimer\n\nThese utilities are provided as-is.  Please consult the Project Home Page for more details.\n',
    'author': 'Vince Skahan',
    'author_email': 'vinceskahan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vinceskahan/wfudptools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
