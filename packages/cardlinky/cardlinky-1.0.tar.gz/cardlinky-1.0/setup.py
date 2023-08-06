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
    'version': '1.0',
    'description': 'A Python wrapper for the CARDLINK api',
    'long_description': '# cardlinky\n<img src="https://img.shields.io/github/license/LUK050/cardlinky?style=flat-square"> <img src="https://img.shields.io/bitbucket/issues/LuK050/cardlinky?style=flat-square">\n\n📘 [Official documentation](https://cardlink.link/reference/api)\n\n## Usage\nFirst of all, you need to create a store in the system https://cardlink.link/. After confirmation, you will be able to get a token and a shop ID to work with the API.\n\n### Creating a bill and getting a payment link:\n```py\nfrom cardlinky import Cardlinky\n\n\ndef print_bill_url(token: str, shop_id: str, amount: float) -> None:\n    # Creating an instance of the class\n    cardlinky = Cardlinky(token)\n\n    # Create a bill and save it\n    bill = cardlinky.create_bill(amount=amount, shop_id=shop_id)\n\n    # Getting a payment link and printing\n    print(bill.link_url)\n\n\nprint_bill_url("YOUR-TOKEN", "YOUR-SHOP-ID", 100.0)\n# https://cardlink.link/link/GkLWvKx3\n```\n\n### Getting a bill status:\n```py\nfrom cardlinky import Cardlinky\n\n\ndef print_bill_status(token: str, id: str) -> None:\n    # Creating an instance of the class\n    cardlinky = Cardlinky(token)\n\n    # Create a bill and save it\n    bill_status = cardlinky.get_bill_status(id=id)\n\n    # Getting a status and printing\n    print(bill_status.status)\n\n\nprint_bill_status("YOUR-TOKEN", "BILL-ID")\n# NEW\n```\n',
    'author': 'LuK050',
    'author_email': 'volychevk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LuK050/cardlinky',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
