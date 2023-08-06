# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['broker', 'broker.aws', 'device']

package_data = \
{'': ['*'],
 'broker': ['web/static/scripts/*', 'web/static/styles/*', 'web/templates/*']}

install_requires = \
['authlib>=1.2.0,<2.0.0',
 'boto3>=1.26.54,<2.0.0',
 'flask>=2.2.2,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'requests',
 'rich>=13.2.0,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['aws-oidc = device.cli:app']}

setup_kwargs = {
    'name': 'aws-oidc-broker',
    'version': '0.1.0',
    'description': '',
    'long_description': '# AWS OpenID Credential Broker\n\nOpenID Based Identity Credential Broker for AWS (Built as an alternative to AWS SSO to support OpenID Federation)\n\n![demo image](.github/images/panel.png)\n\n\n## Broker authentication flow \n\n```mermaid\nsequenceDiagram;\n\nparticipant User;\nparticipant Broker;\nparticipant IDP;\nparticipant AWS;\n\nUser -->> Broker: Login via IDP\nBroker -->> IDP: Forward Auth Request\nIDP -->> Broker: IDP Login Successful\nUser -->> Broker: Open AWS Console\nBroker -->> AWS: Request Session\nAWS -->> Broker: Login Successfull\nBroker -->> Browser: Open AWS Console\n```\n\n## Getting Started\n\nQuick Start with docker compose\n\n```bash\ndocker-compose up -d\n```\n\n### Prerequisites\n\n- python3\n- virtualenv\n- docker\n- docker-compose\n\n\n### Installing\n\nA step by step series of examples that tell you how to get a development env running\n\nClone the Project \n\n```bash\ngit clone https://github.com/Rishang/aws-oidc-broker.git\n```\n\nInitialzing virtualenv\n\n```bash\ncd aws-oidc-broker\npython -m venv venv\nsource ./venv/bin/activate\n```\n\nInstalling Dependencies\n\n```bash\npip install -r requirements.txt\n```\n\nConfigure .env file or perform export of those variables\n\n```bash\ncp .env.example .env\n```\n\nConfigure environment variables as required.\n\n## Environment Variables for KEYCLOAK integration\n\n| VARIABLE NAME | Example VALUE | DESCRIPTION | REQUIRED |\n| --- | --- | --- | --- |\n| `KEYCLOAK_CLIENT_ID` | `aws-oidc`| Client ID | yes |\n| `KEYCLOAK_WELLKNOWN` | `https://example.dev/realms/test/.well-known/openid-configuration` | Keycloak well-known openid URL | yes |\n| `APP_SECRET` | `!apppasswd` | optional env variable to set encrytion secret | no |\n| `TITLE` | `Example Broker` | Title to display on Broker UI | no |\n\n## Deployment\n\nAdd additional notes about how to deploy this on a live system\n\n## Built With\n\n- [Flask](https://flask.palletsprojects.com/) - The web framework used\n\n- [VueJs](https://vuejs.org/) - The web framework for building web user interfaces.\n',
    'author': 'Rishang',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
