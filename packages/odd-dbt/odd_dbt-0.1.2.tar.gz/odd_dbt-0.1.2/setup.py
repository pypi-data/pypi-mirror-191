# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_dbt']

package_data = \
{'': ['*']}

install_requires = \
['dbt-core>=1.4.1,<2.0.0',
 'dbt-postgres>=1.4.1,<2.0.0',
 'dbt-redshift>=1.4.0,<2.0.0',
 'dbt-snowflake>=1.4.0,<2.0.0',
 'funcy>=1.17,<2.0',
 'loguru>=0.6.0,<0.7.0',
 'odd-models>=2.0.11,<3.0.0',
 'oddrn-generator==0.1.62',
 'psycopg2>=2.9.5,<3.0.0',
 'sqlalchemy>=1.4.46,<2.0.0']

setup_kwargs = {
    'name': 'odd-dbt',
    'version': '0.1.2',
    'description': 'OpenDataDiscovery Action for dbt',
    'long_description': '# OpenDataDiscovery dbt tests metadata collecting\n[![PyPI version](https://badge.fury.io/py/odd-dbt.svg)](https://badge.fury.io/py/odd-dbt)\n\nLibrary used for running dbt tests and injecting them as entities to ODD platform. \n\n## Supported data sources\n| Source    |\n|-----------| \n| Snowflake | \n| Redshift  |\n| Postgres  |\n\n## Requirements\nLibrary to inject Quality Tests entities requires presence of corresponding with them datasets entities in the platform.  \nFor example: if you want to inject data quality test of Snowflake table, you need to have entity of that table present in the platform.\n\n## Supported tests\nLibrary supports for basics tests provided by dbt. \n- `unique`: values in the column should be unique\n- `not_null`: values in the column should not contain null values\n- `accepted_values`: column should only contain values from list specified in the test config\n- `relationships`: each value in the select column of the model exists as a specified field in the reference table (also known as referential integrity)\n\n## ODDRN generation for datasets\nhost_settings of ODDRN generators required for source datasets are loaded from `.dbt/profiles.yml`.  \nProfiles inside the file looks different for each type of data source.  \n**Snowflake** host_settings value is created from field `account`. Field value should be `<account_identifier>`  \nFor example the URL for an account uses the following format: `<account_identifier>`.snowflakecomputing.com  \nExample Snowflake account identifier `hj1234.eu-central-1`.  \n**Redshift** and **Postgres** host_settings are loaded from field `host` field.  \nExample Redshift host: `redshift-cluster-example.123456789.eu-central-1.redshift.amazonaws.com`  ',
    'author': 'Mateusz Kulas',
    'author_email': 'mkulas@provectus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
