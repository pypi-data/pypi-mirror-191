# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['farcaster', 'farcaster.utils']

package_data = \
{'': ['*']}

install_requires = \
['canonicaljson>=1.6.4,<2.0.0',
 'eth-account>=0.8.0,<0.9.0',
 'pydantic>=1.9.2,<2.0.0',
 'pyhumps>=3.7.2,<4.0.0',
 'pytest-dependency>=0.5.1,<0.6.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'farcaster',
    'version': '0.6.3',
    'description': 'farcaster-py is a Python SDK for the Farcaster Protocol',
    'long_description': '# farcaster-py\n\n<div align="center">\n\n[![Build status](https://github.com/a16z/farcaster-py/workflows/build/badge.svg?branch=main&event=push)](https://github.com/a16z/farcaster-py/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/farcaster.svg)](https://pypi.org/project/farcaster/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/a16z/farcaster-py/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/a16z/farcaster-py/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/a16z/farcaster-py/releases)\n[![License](https://img.shields.io/github/license/a16z/farcaster-py)](https://github.com/a16z/farcaster-py/blob/main/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n[![chat](https://img.shields.io/badge/chat-telegram-blue)](https://t.me/+aW_ucWeBVUZiNThh)\n\nfarcaster-py is a modern Python SDK for the Farcaster protocol<br></br>\n\nFull documentation can be found [here](https://a16z.github.io/farcaster-py)\n\n</div>\n\n## Installation\n\n```bash\npip install -U farcaster\n```\n\nor install with [Poetry](https://python-poetry.org/):\n\n```bash\npoetry add farcaster\n```\n\n## Usage\n\nTo use the Farcaster API you need to have a Farcaster account. We will use the mnemonic or private key of the Farcaster custody account (not your main wallet) to connect to the API.\n\nFirst install dotenv:\n\n```bash\npip install python-dotenv # Or \'poetry add python-dotenv\'\n```\nNext, save your Farcaster mnemonic or private key to a `.env` file. Now you can initialize the client, and automatically connect to the Farcaster API!\n\n```python\nimport os\nfrom farcaster import MerkleApiClient\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\nclient = MerkleApiClient(mnemonic=os.environ.get("<MNEMONIC_ENV_VAR>"))\n\nprint(client.get_healthcheck())\n```\n\n## Examples\n\nGet a cast\n\n```python\nresponse = fcc.get_cast("0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f")\nprint(response.cast.author.username) # "dwr"\n```\n\nPublish a cast\n\n```python\nresponse = fcc.post_cast(text="Hello world!")\nprint(response.cast.hash) # "0x...."\n```\n\nGet a user by username\n\n```python\nuser = fcc.get_user_by_username("mason")\nprint(user.username) # "mason"\n```\n\nGet a user\'s followers using a fid (farcaster ID)\n\n```python\nresponse = fcc.get_followers(fid=50)\nprint(response.users) # [user1, user2, user3]\n```\n\nStream recent casts\n\n```python\nfor cast in fcc.stream_casts():\n    if cast:\n        print(cast.text) # "Hello world!"\n```\n\nGet users who recently joined Farcaster\n\n```python\nresponse = fcc.get_recent_users()\nprint(response.users) # [user1, user2, user3]\n```\n\nGet your own user object\n\n```python\nuser = fcc.get_me()\nprint(user.username) # "you"\n```\n\nRecast a cast\n\n```python\nresponse = fcc.recast("0x....")\nprint(response.cast.hash) # "0x...."\n```\n\nand many, many more things. The full specification can be found on the [Reference page](https://a16z.github.io/farcaster-py/reference).\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/a16z/farcaster-py)](https://github.com/a16z/farcaster-py/blob/main/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/a16z/farcaster-py/blob/main/LICENSE) for more details.\n\n## Disclaimer\n\n_This code is being provided as is. No guarantee, representation or warranty is being made, express or implied, as to the safety or correctness of the code. It has not been audited and as such there can be no assurance it will work as intended, and users may experience delays, failures, errors, omissions or loss of transmitted information. Nothing in this repo should be construed as investment advice or legal advice for any particular facts or circumstances and is not meant to replace competent counsel. It is strongly advised for you to contact a reputable attorney in your jurisdiction for any questions or concerns with respect thereto. a16z is not liable for any use of the foregoing, and users should proceed with caution and use at their own risk. See [our disclosures page](https://a16z.com/disclosures) for more info._\n',
    'author': 'Andreessen Horowitz',
    'author_email': 'crypto-engineering@a16z.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/a16z/farcaster-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>3.7.1,<4.0.0',
}


setup(**setup_kwargs)
