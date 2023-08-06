# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gener8app']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['gener8app = gener8app.main:app']}

setup_kwargs = {
    'name': 'gener8app',
    'version': '0.0.0',
    'description': 'A CLI to generate bare-bone FastAPI project',
    'long_description': '# GENER8APP\n\n### About GENER8APP\n\nGener8app is a CLI tool for generating bare-bone FastAPI project.\nWhen you run `gener8app new [project_name]`, it generates the following project structure:\n\n    .\n    ├── app/\n    │   ├── __init__.py\n    │   ├── config/\n    │   │   ├── __init__.py\n    │   │   └── config.py\n    │   ├── database/\n    │   │   ├── __init__.py\n    │   │   └── database.py\n    │   ├── models/\n    │   │   ├── __init__.py\n    │   │   └── models.py\n    │   ├── routers/\n    │   │   ├── __init__.py\n    │   │   └── routes.py\n    │   ├── schemas/\n    │   │   ├── __init__.py\n    │   │   └── schemas.py\n    │   └── services/\n    │   │   ├── __init__.py\n    │   │   └── services.py\n    │   └── statics/\n    │   └── templates/\n    │   └── tests/\n    │   │   ├── __init__.py\n    │   │   └── tests.py\n    │   └── utils/\n    │       ├── __init__.py\n    │       └── utils.py\n    ├── Dockerfile\n    ├── docker-compose.yaml\n    ├── [project_name]_ven\n    ├── .env\n    ├── .gitignore\n    ├── requirements.txt\n    └── README.md\n\n### COMMAND\n\n`gener8app new [project_name]`\n\nThis command initialized an empty git repository, create a virtual environment using the python builtin `venv` by appending `_evv` to the project name, i.e `[project_name]_env`.\n\n##### Activate the virtual environment before installing dependencies.\n\n[view project on github](https://github.com/kenmoh/cli)\n',
    'author': 'kenmoh',
    'author_email': 'kenneth.aremoh@gmail.com',
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
