# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mysoc_dataset']

package_data = \
{'': ['*']}

install_requires = \
['rich-click>=1.5.2,<2.0.0', 'rich>=12.5.1,<13.0.0']

extras_require = \
{':python_version < "3.8"': ['pandas==1.3.5'],
 ':python_version >= "3.8"': ['pandas>=1.3.5']}

entry_points = \
{'console_scripts': ['mysoc-dataset = mysoc_dataset.__main__:main']}

setup_kwargs = {
    'name': 'mysoc-dataset',
    'version': '0.3.0',
    'description': 'Tool to download mySociety datasets',
    'long_description': '# mysoc-dataset\n\nA python package and CLI to download mySociety datasets.\n\nThe best example of one of these datasets is: https://mysociety.github.io/uk_local_authority_names_and_codes/\n\nThese datasets are versioned [frictionless datapackages](https://frictionlessdata.io/). A repository may contain multiple data packages, each data package may contain multiple versions. A version of a datapackage will contain multiple resources (.csvs) and some composite files made up of resources (.xlsx or .sqlite). \n\n\n## Installation\n\nIt can be installed with:\n\n```\npython -m pip install mysoc-dataset\n```\n\nor if using poetry:\n\n```\npoetry add mysoc-dataset\n```\n\n## Usage\n\n### As a package\n\nThe package has two basic functions (with helpful error messages) to access the url or a dataframe\nof the resource.\n\n```python\nfrom mysoc_dataset import get_dataset_url, get_dataset_df\n\nurl = get_dataset_url(\n    repo_name="uk_local_authority_names_and_codes",\n    package_name="uk_la_future",\n    version_name="latest",\n    file_name="uk_local_authorities_future.csv",\n)\n\n# get a pandas dataframe\ndf = get_dataset_df(\n    repo_name="uk_local_authority_names_and_codes",\n    package_name="uk_la_future",\n    version_name="latest",\n    file_name="uk_local_authorities_future.csv",\n)\n\n\n```\n\n### As a CLI\n\nThe CLI can be used to explore avaliable data using the `list` command, get the [frictionless datapackage](https://frictionlessdata.io/) that describes the repo using `detail` fetch the url with the `url` command or download the file using `download`.\n\nThis can be used to source files or pipe the URLs into other functions without writing python scripts. \n\nThe CLI can either be run as `python -m mysoc_dataset` or `mysoc-dataset`. \n\nFor instance, the following will print the `datapackage.json` that describes the underlying contents. \n\n`mysoc-dataset detail --repo uk_local_authority_names_and_codes --version latest --package uk_la_future`\n\nAnd the following will get the URL of the resource, pegged to the `1` major version:\n\n`mysoc-dataset url --repo uk_local_authority_names_and_codes --version 1 --package uk_la_future --file uk_local_authorities_future.csv`\n\nIf the dataset has had a major change, a warning will indicate this is no longer the latest version - while not introducing breaking changes to headers without the script being changed.\n\nUse `mysoc-dataset --help` for more instructions. \n\nIf using the CLI for a dataset, please fill out a survey of what you are using it for to help us explain the value of the data to funders. You can get a URL to the survey page using the \'survey\' command. \n\n`mysoc-dataset survey --repo uk_local_authority_names_and_codes --version latest --package uk_la_future --file uk_local_authorities_future.csv`\n\n# Maintenance\n\nIf the repo has a valid PYPI_TOKEN secret, and if the poetry version is bumped and all tests pass - the GitHub Action will automatically publish on push to the main branch.',
    'author': 'Alex Parsons',
    'author_email': 'alex.parsons@mysociety.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mysociety/mysoc-dataset',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
