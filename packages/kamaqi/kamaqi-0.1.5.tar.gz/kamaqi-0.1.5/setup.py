# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kamaqi',
 'kamaqi.add',
 'kamaqi.app',
 'kamaqi.init',
 'kamaqi.remove',
 'kamaqi.run',
 'kamaqi.show',
 'kamaqi.templates',
 'kamaqi.upgrade',
 'kamaqi.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['kamaqi = kamaqi.main:app']}

setup_kwargs = {
    'name': 'kamaqi',
    'version': '0.1.5',
    'description': 'A command line app for creating Backends with FastAPI',
    'long_description': '# Kamaqi\n\nA command line app for creating Backends with FastAPI, inspired in Artisan from Laravel and manage.py from Django.\n\n## The key features are:\n\n- Create a normal project and a project with `Docker`.\n- Choose a different databases  `MySQL`, `PostgreSQL` and `SQLite`.\n- Work as `Djando` creating apps.\n- Every app created with Kamaqi, contains a minimal CRUD.\n\n## Installation:\n\nInstall Kamaqi in the global environment.\n```bash \npip install kamaqi\n```\nFor explore Kamaqi commands and options use.\n```bash\nkamaqi --help \nkamaqi command --help\n```\n## Basic Usage:\n\n### Init your project:\n```bash\nkamaqi init project you_project_name\n```\nChoose the options, for setting your project. Remember for create projects\nwith docker requires **docker** and **docker-compose** installed.\n\n### Run your project\n```bash\ncd your_project_name\n```\n```bash\nkamaqi run project you_project_name\n```\n- Explore your API documentation\n- For default kamaqi use the port 8000\n- Open in your browser http://localhost:8000/docs\n### Add apps to your project\nAdd an app \n```bash\nkamaqi add app users\n```\nAdd multiple apps\n```bash\nkamaqi add apps users products sales... etc\n```\n### Create files for your apps\n```bash\nKamaqi upgrade apps \n```\n- Refresh files in your editor.\n- Refresh your API documentation\n### Review your project settings\n```bash\nkamaqi show config\n```\n### Review your project apps\n```bash\nkamaqi show apps\n```\n\n## Project Status\n- The project currently is in  development and will be\nbugs.\n\n- Your can contribute to this project, reporting bugs, writing documentation, writing tests, with pull requests ... etc.\n\nFor more information visit [GitHub repository](https://github.com/Mitchell-Mirano/kamaqi)\n\n\n\n\n\n',
    'author': 'Mitchell Mirano',
    'author_email': 'mitchellmirano25@gmail.com',
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
