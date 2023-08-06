# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shiny_api', 'shiny_api.classes', 'shiny_api.config', 'shiny_api.modules']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'beautifulsoup4>=4.11.2,<5.0.0',
 'chatgpt>=2.2212.0,<3.0.0',
 'discord>=2.1.0,<3.0.0',
 'kivy>=2.1.0,<3.0.0',
 'opencv-python>=4.7.0.68,<5.0.0.0',
 'py-trello>=0.19.0,<0.20.0',
 'pygsheets>=2.0.6,<3.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'selenium>=4.8.0,<5.0.0',
 'sqlalchemy>=2.0.1,<3.0.0',
 'zpl>=0.1.10,<0.2.0']

extras_require = \
{':sys_platform == "darwin"': ['python-dotenv>=0.21.1,<0.22.0'],
 ':sys_platform == "windows"': ['dotenv>=0.0.5,<0.0.6']}

entry_points = \
{'console_scripts': ['shiny_serial_camera = '
                     'shiny_api.shiny_serial_camera:start_gui',
                     'shiny_start_gui = shiny_api.main:start_gui']}

setup_kwargs = {
    'name': 'shiny-api',
    'version': '0.1.24',
    'description': 'Interface with LS and Camera Scanner',
    'long_description': 'None',
    'author': 'Chris Busillo',
    'author_email': 'info@shinycomputers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
