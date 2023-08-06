# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kamaqi',
 'kamaqi.add',
 'kamaqi.config',
 'kamaqi.init',
 'kamaqi.remove',
 'kamaqi.run',
 'kamaqi.show',
 'kamaqi.templates',
 'kamaqi.templates.app',
 'kamaqi.templates.database',
 'kamaqi.templates.docker',
 'kamaqi.templates.migrations',
 'kamaqi.templates.project',
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
    'version': '0.1.6',
    'description': 'A command line app for creating Backends with FastAPI',
    'long_description': '# Kamaqi\nA command line app for creating Backends with **FastAPI**, inspired in **Artisan** from **Laravel** and **manage.py** from **Django**.\n\n## The key features are:\n\n- Creates a normal project or a project with **Docker**.\n- Chooses a **MySQL**, **PostgreSQL** or **SQLite** database.\n- Works as with **Django** creating  apps.\n- Every application created with **Kamaqi** contains a minimum **CRUD**.\n\n## Installation:\n\nInstall Kamaqi in the global environment.\n```bash \npip install kamaqi\n```\nFor help on Kamaqi commands and parameters, use.\n```bash\nkamaqi --help \nkamaqi command --help\n```\n## Basic Usage:\n\n### Init your project:\n```bash\nkamaqi init project you_project_name\n```\nChoose the options, for setting your project. Remember for create projects\nwith docker requires **docker** and **docker-compose** installed.\n\n### Run your project\n```bash\ncd your_project_name\n```\n```bash\nkamaqi run project you_project_name\n```\n- Explore the FastAPI documentation.\n- For Kamaqi the default port is the 8000.\n- Open in your browser http://localhost:8000/docs\n### Add apps to your project\nAdd an app \n```bash\nkamaqi add app users\n```\nAdd multiple apps\n```bash\nkamaqi add apps users products sales ... etc\n```\n### Create files for your apps\n```bash\nKamaqi upgrade apps \n```\n- Refresh files in your editor.\n- Refresh the FastAPI documentation.\n### Review your project settings\n```bash\nkamaqi show config\n```\n### Review your project apps\n```bash\nkamaqi show apps\n```\n### Database migrations\nFor update your database tables.\n```bash\nkamaqi upgrade tables -m"A description about your changes"\n```\n### To connect to MySQL or PostgreSQL database use.\n\n- For projects with Docker, review the **docker-compose.yaml**\nand use the database environment variables\nor use the following parameters.\n```bash\nDATABASE_USER = your_project_name_user\nDATABASE_PASSWORD = your_project_name_password\nDATABASE_NAME = your_project_name_db\nDATABASE_PORT = MySQL 3306  and PostgreSQL 5432\n```\n- For normal projects use your settings and in the .env and edit the connection parameters.\n\n- For SQLite databases use a editor extension or a other \nsoftware.\n\n## Project Status\n- The project is currently under development and may contain errors.\n\n- You can contribute to this project, reporting bugs, writing documentation, writing tests, with pull requests... etc.\n\nFor more information, visit [GitHub repository](https://github.com/Mitchell-Mirano/kamaqi)\n\n\n\n\n\n',
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
