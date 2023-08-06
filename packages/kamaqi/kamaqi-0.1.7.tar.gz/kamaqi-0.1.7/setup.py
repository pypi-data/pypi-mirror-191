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
    'version': '0.1.7',
    'description': 'A command line app for creating Backends with FastAPI',
    'long_description': '# Kamaqi\nA command line app for creating Backends with **FastAPI**, inspired in **Artisan** from **Laravel** and **manage.py** from **Django**.\n\n## The key features are:\n\n- Creates a normal project or a project with **Docker**.\n- Chooses a **MySQL**, **PostgreSQL** or **SQLite** database.\n- Works as with **Django** creating  apps.\n- Every application created with **Kamaqi** contains a minimum **CRUD**.\n- Integration between **SQLAlchemy** and **Alembic** for migrations.\n\n### What is an app?\nAn application is a module of your project, which manages the logic of an actor of your application, for example (users, products, shops ... etc). Generally, an app is associated with a table in the database on which you want to do CRUD operations and they are named in the plural.\n\n\nEvery app created with Kamaqi contains the following\nfiles. For example:\n\n```bash\nusers\n├── crud.py\n├── router.py\n└── schemas.py\n```\n- The **schemas.py** file contains classes of validation for input and output  data using\nPydantic. For example:\n\n```python\nfrom pydantic import BaseModel,EmailStr\n\nclass UserCreate(BaseModel):\n    name:str\n    email:EmailStr\n    password:str\n\nclass UserRead(BaseModel):\n    id:int\n    name:str\n    email:EmailStr\n```\n- The **router.py** contains an APIRouter and endpoint functions. for example:\n```python\nfrom fastapi import APIRouter,Depends,status\nfrom users.schemas import UserCreate\nfrom users.schemas import UserRead\nfrom users.crud import insert_user\n\nfrom sqlalchemy.orm import Session\nfrom database.database import get_db\n\nusers_routes= APIRouter(prefix="/api/v1/users")\n\n@users_routes.post(path="/create/",\n                 tags=["Users"],\n                 response_model=UserRead,\n                 status_code=status.HTTP_201_CREATED)\nasync def create_user(user_data:UserCreate,\n                      db:Session=Depends(get_db)):\n\n    return insert_user(db,user_data)\n```\n\n- The **crud.py** contains a CRUD functions for your modules as insert_app, update_app, select_app ... etc. For example:\n\n```python\nfrom users.schemas import UserCreate\nfrom sqlalchemy.orm import Session\nfrom database import models\n\ndef insert_user(db: Session, \n                user:UserCreate):\n\n    db_user = models.User(**user.dict())\n    db.add(db_user)\n    db.commit()\n    db.refresh(db_user)\n\n    return db_app\n```\nThis is just an example, in a real development environment, before\ninserting the user into the database should encrypt the password, check if the user is not registered...etc.\n\n### Project Structure\n\nWhen creates a new project with Kamaqi this can have the following structures.\n\n- A projects with Docker following the next structure.\n\n```bash\nproject_name\n├── db_volume\n├── docker-compose.yaml\n├── Dockerfile\n├── kamaqi.json\n├── requirements.txt\n└── src\n    ├── alembic.ini\n    ├── database\n    │\xa0\xa0 ├── database.py\n    │\xa0\xa0 ├── models.py\n    ├── main.py\n    ├── .env\n    ├── migrations\n    │\xa0\xa0 ├── env.py\n    │\xa0\xa0 ├── script.py.mako\n    │\xa0\xa0 └── versions\n    ├── users\n    │\xa0\xa0 ├── crud.py\n    │\xa0\xa0 ├── router.py\n    │\xa0\xa0 └── schemas.py\n    └── project_name\n        ├── auth.py\n        ├── exceptions.py\n        ├── router.py\n        ├── schemas.py\n        └── settings.py\n```\n- The normal projects following the nex structure.\n\n```bash \nproject_name\n├── alembic.ini\n├── database\n│\xa0\xa0 ├── database.py\n│\xa0\xa0 └── models.py\n├── env\n├── kamaqi.json\n├── main.py\n├── .env\n├── migrations\n│\xa0\xa0 ├── env.py\n│\xa0\xa0 ├── script.py.mako\n│\xa0\xa0 └── versions\n├── requirements.txt\n├── users\n│\xa0\xa0 ├── crud.py\n│\xa0\xa0 ├── router.py\n│\xa0\xa0 └── schemas.py\n└── project_name\n    ├── auth.py\n    ├── exceptions.py\n    ├── router.py\n    ├── schemas.py\n    └── settings.py\n```\n- In normal projects the env directory is the\nPython virtual environment.\n\n- The .env file contains the environment\nvariables.\n\n- The project_name is the main app in to the project.\n- **auth.py** contains functions for hashing passwords, verify passwords and create access tokens. \n- **exceptions.py** contains some exceptions.\n- **settings.py** contains classes and functions that provide environment variables like secret keys, database connection parameters...etc. These variables are taken from the .env file.\n\n\n## Installation:\n\nInstall Kamaqi in the global environment.\n```bash \npip install kamaqi\n```\nFor help on Kamaqi commands and parameters, use.\n```bash\nkamaqi --help \nkamaqi command --help\n```\n## Basic Usage:\n\n### Init your project:\n```bash\nkamaqi init project project_name\n```\nChoose the options, for setting your project. Remember for create projects\nwith docker requires **docker** and **docker-compose** installed.\n\n### Run your project\n```bash\ncd project_name\n```\n```bash\nkamaqi run project project_name\n```\n- Explore the FastAPI documentation.\n- For Kamaqi the default port is the 8000.\n- Open in your browser http://localhost:8000/docs\n### Add apps to your project\nAdd an app \n```bash\nkamaqi add app users\n```\nAdd multiple apps\n```bash\nkamaqi add apps users products sales ... etc\n```\n### Create files for your apps\n```bash\nKamaqi upgrade apps \n```\n- Refresh files in your editor.\n- Refresh the FastAPI documentation.\n### Review your project settings\n```bash\nkamaqi show config\n```\n### Review your project apps\n```bash\nkamaqi show apps\n```\n### Database migrations\nFor update your database tables.\n```bash\nkamaqi upgrade tables -m"A description about your changes"\n```\n### To connect to MySQL or PostgreSQL database use.\n\n- For projects with Docker, review the **docker-compose.yaml**\nand use the database environment variables\nor use the following parameters.\n```bash\nDATABASE_USER = your_project_name_user\nDATABASE_PASSWORD = your_project_name_password\nDATABASE_NAME = your_project_name_db\nDATABASE_PORT = MySQL 3306  and PostgreSQL 5432\n```\n- For normal projects use your settings and in the .env and edit the connection parameters.\n\n- For SQLite databases use a editor extension or a other \nsoftware.\n\n## Project Status\n- The project is currently under development and may contain errors.\n\n- You can contribute to this project, reporting bugs, writing documentation, writing tests, with pull requests... etc.\n\nFor more information, visit [GitHub repository](https://github.com/Mitchell-Mirano/kamaqi)\n\n\n\n\n\n',
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
