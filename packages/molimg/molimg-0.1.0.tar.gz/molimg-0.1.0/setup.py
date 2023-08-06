# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['molimg']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0',
 'rdkit>=2022.9.4,<2023.0.0',
 'xlsxwriter>=3.0.8,<4.0.0']

setup_kwargs = {
    'name': 'molimg',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Molecular Imager\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Tests](https://github.com/jdkern11/molimg/workflows/tests/badge.svg)](https://github.com/jdkern11/molimg/actions?workflow=tests)\n[![codecov](https://codecov.io/gh/jdkern11/molimg/branch/main/graph/badge.svg?token=4MU1H8MD94)](https://codecov.io/gh/jdkern11/molimg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![version](https://img.shields.io/badge/Release-0.1.0-blue)](https://github.com/jdkern11/molimg/releases)\n\nDo you ever wish you could easily embed the images of your smiles strings into \nan excel sheet? Wish no more! molimg is here to do just that!\n\nTake the following data in a csv:\n\n![image of example data](https://raw.githubusercontent.com/jdkern11/molimg/main/images/example_csv.png)\n\nand molimg will convert it like so:\n\n![image of example data](https://raw.githubusercontent.com/jdkern11/molimg/main/images/example_csv_with_images.png)\n\n## Usage\nFirst, import the data into a pandas dataframe, then pass this dataframe, the \ncolumns that you want to convert to images, and the save name of the file to the \npackage:\n\n```Python\nimport pandas as pd\nfrom molimg import excel\n\ndf = pd.read_csv('example_data.csv')\nsmiles_columns = ['smiles1', 'smiles2']\nexcel.write(\n    df=df, \n    smiles_columns=smiles_columns, \n    filename='example_data_with_images.xlsx'\n)\n```\n\nThe order the columns appear in df.columns is how the columns will be saved in\nthe new excel sheet. The new smiles columns with images will always appear to the right\nof the data they originate from with `{original_column}_image` as the new column name.\n\nAny error that occurs when trying to convert a smiles string to an image \nwill appear as a warning log message and the image will not be produced. The excel sheet\nwill still be created with the smiles strings that work.\n",
    'author': 'jdkern11',
    'author_email': 'josephdanielkern@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jdkern11/molimg.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
