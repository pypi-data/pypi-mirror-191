# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quiffen', 'quiffen.core']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'quiffen',
    'version': '2.0.5',
    'description': 'Quiffen',
    'long_description': "Quiffen\n========\n\n.. content\n\nQuiffen is a Python package for parsing QIF (Quicken Interchange Format) files.\n\nThe package allows users to both read QIF files and interact with the contents, and also to create a QIF structure\nand then output to either a QIF file, a CSV of transaction data or a pandas DataFrame.\n\nQIF is an old file type, but has its merits because:\n\n- It's standardised (apart from dates, but that can be dealt with)\n\n  - Unlike CSVs, QIF files all follow the same format, so they don't require special attention when they come from\n    different sources\n\n- It's written in plain text\n\nFeatures\n--------\n\n- Import QIF files and manipulate data\n- Create QIF structures (support for Transactions, Investments, Accounts, Categories, Classes, Splits)\n- Convert Qif objects to a number of different formats and export (pandas DataFrame, CSV, QIF file)\n\nUsage\n------\n\nHere's an example parsing of a QIF file:\n\n>>> from quiffen import Qif, QifDataType\n>>> import decimal\n>>> qif = Qif.parse('test.qif', day_first=False)\n>>> qif.accounts\n{'Quiffen Default Account': Account(name='Quiffen Default Account', desc='The default account created by Quiffen when no\nother accounts were present')}\n>>> acc = qif.accounts['Quiffen Default Account']\n>>> acc.transactions\n{'Bank': TransactionList(Transaction(date=datetime.datetime(2021, 2, 14, 0 , 0), amount=decimal.Decimal(150.0), ...), ...),\n'Invst': TransactionList(...)}\n>>> tr = acc.transactions['Bank'][0]\n>>> print(tr)\nTransaction:\n    Date: 2020-02-14 00:00:00\n    Amount: 67.5\n    Payee: T-Mobile\n    Category: Cell Phone\n    Split Categories: ['Bills']\n    Splits: 2 total split(s)\n>>> qif.categories\n{'Bills': Category(name='Bills), expense=True, hierarchy='Bills'}\n>>> bills = qif.categories['Bills']\n>>> print(bills.render_tree())\nBills (root)\n└─ Cell Phone\n>>> df = qif.to_dataframe(data_type=QifDataType.TRANSACTIONS)\n>>> df.head()\n        date  amount           payee  ...                           memo cleared check_number\n0 2020-02-14    67.5        T-Mobile  ...                            NaN     NaN          NaN\n1 2020-02-14    32.0  US Post Office  ...  money back for damaged parcel     NaN          NaN\n2 2020-12-02   -10.0          Target  ...        two transactions, equal     NaN          NaN\n3 2020-11-02   -25.0         Walmart  ...          non split transaction       X        123.0\n4 2020-10-02  -100.0      Amazon.com  ...                   test order 1       *          NaN\n...\n\nAnd here's an example of creating a QIF structure and exporting to a QIF file:\n\n>>> import quiffen\n>>> from datetime import datetime\n>>> qif = quiffen.Qif()\n>>> acc = quiffen.Account(name='Personal Bank Account', desc='My personal bank account with Barclays.')\n>>> qif.add_account(acc)\n>>> groceries = quiffen.Category(name='Groceries')\n>>> essentials = quiffen.Category(name='Essentials')\n>>> groceries.add_child(essentials)\n>>> qif.add_category(groceries)\n>>> tr = quiffen.Transaction(date=datetime.now(), amount=150.0)\n>>> acc.add_transaction(tr, header=quiffen.AccountType.BANK)\n>>> qif.to_qif()  # If a path is provided, this will save the file too!\n'!Type:Cat\\nNGroceries\\nETrue\\nIFalse\\n^\\nNGroceries:Essentials\\nETrue\\nIFalse\\n^\\n!Account\\nNPersonal Bank Account\\nDMy\npersonal bank account with Barclays.\\n^\\n!Type:Bank\\nD02/07/2021\\nT150.0\\n^\\n'\n\nDocumentation\n-------------\n\nDocumentation can be found at: https://quiffen.readthedocs.io/en/latest/\n\nInstallation\n------------\n\nInstall Quiffen by running:\n\n>>> pip install quiffen\n\nDependencies\n------------\n\n- `pandas <https://pypi.org/project/pandas/>`_ (optional) for exporting to DataFrames\n\n  - The ``to_dataframe()`` method will not work without pandas installed.\n\nTo-Dos\n------\n\n- Add support for the ``MemorizedTransaction`` object present in QIF files.\n\nContribute\n----------\n\nGitHub pull requests welcome, though if you want to make a major change, please open an issue first for discussion.\n\n- Issue Tracker: https://github.com/isaacharrisholt/quiffen/issues\n- Source Code: https://github.com/isaacharrisholt/quiffen\n\nSupport\n-------\n\nIf you are having issues, please let me know.\n\nLicense\n-------\n\nThe project is licensed under the GNU GPLv3 license.\n",
    'author': 'Isaac Harris-Holt',
    'author_email': 'isaac@harris-holt.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/isaacharrisholt/quiffen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
