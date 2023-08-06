# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cardlinky',
 'cardlinky.types',
 'cardlinky.types.enums',
 'cardlinky.types.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'cardlinky',
    'version': '1.6.1',
    'description': 'Wrapper for the Cardlink API in Python',
    'long_description': '# cardlinky\n<a href="https://pypi.org/project/cardlinky/"><img src="https://img.shields.io/pypi/v/cardlinky?style=flat-square"></a> <a href="https://pypi.org/project/cardlinky/"><img src="https://img.shields.io/pypi/dm/cardlinky?color=blue&style=flat-square"></a> <img src="https://img.shields.io/pypi/pyversions/cardlinky?style=flat-square"> \n\n[📘 Official documentation](https://cardlink.link/reference/api)\n\n## Usage\nFirstly, you need to create an account and а shop in https://cardlink.link/. After confirmation, you will be able to get a token and a shop ID to work with the API.\n\n### Creating a bill and getting a payment link:\n```py\nfrom cardlinky import Cardlinky\n\n\ndef print_bill_url(token: str, shop_id: str, amount: float) -> None:\n    # Creating an instance of the class\n    cardlinky = Cardlinky(token)\n\n    # Create a bill and save it\n    bill = cardlinky.create_bill(amount=amount, shop_id=shop_id)\n\n    # Getting a payment link and printing\n    print(bill.link_url)\n\n\nprint_bill_url("YOUR-TOKEN", "YOUR-SHOP-ID", 100.0)\n# https://cardlink.link/link/GkLWvKx3\n```\n\n### Getting a bill status:\n```py\nfrom cardlinky import Cardlinky\n\n\ndef print_bill_status(token: str, bill_id: str) -> None:\n    # Creating an instance of the class\n    cardlinky = Cardlinky(token)\n\n    # Create a bill and save it\n    bill_status = cardlinky.get_bill_status(bill_id=bill_id)\n\n    # Getting a status and printing\n    print(bill_status.status)\n\n\nprint_bill_status("YOUR-TOKEN", "BILL-ID")\n# Status.NEW\n```\n\n## Installation\n```sh\npip install cardlinky\n```\n### Dependencies:\nPackage  | Version\n-------- | ----------\n`requests` | `>=2.28.2` \n',
    'author': 'LuK050',
    'author_email': 'volychevk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LuK050/cardlinky',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
