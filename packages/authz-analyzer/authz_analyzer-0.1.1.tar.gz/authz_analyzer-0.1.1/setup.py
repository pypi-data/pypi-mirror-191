# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authz_analyzer',
 'authz_analyzer.datastores',
 'authz_analyzer.datastores.aws',
 'authz_analyzer.datastores.aws.analyzer',
 'authz_analyzer.datastores.aws.analyzer.redshift',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.actions',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.iam',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.iam.policy',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.iam.role',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.policy_evaluation',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.principals',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.ptrp_allowed_lines',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.ptrp_models',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.resources',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.services',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.services.assume_role',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.services.federated_user',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.services.s3',
 'authz_analyzer.datastores.aws.aws_ptrp_package.aws_ptrp.utils',
 'authz_analyzer.datastores.bigquery',
 'authz_analyzer.datastores.mongodb',
 'authz_analyzer.datastores.mongodb.atlas',
 'authz_analyzer.datastores.postgres',
 'authz_analyzer.datastores.snowflake',
 'authz_analyzer.models',
 'authz_analyzer.utils',
 'authz_analyzer.writers',
 'tests',
 'tests.mocks',
 'tests.test_writers',
 'tests.tests_datastores',
 'tests.tests_datastores.aws',
 'tests.tests_datastores.aws.aws_ptrp',
 'tests.tests_datastores.aws.utils',
 'tests.tests_datastores.mongodb',
 'tests.tests_datastores.postgres',
 'tests.tests_datastores.postgres.mocks',
 'tests.tests_datastores.redshift',
 'tests.tests_datastores.snowflake']

package_data = \
{'': ['*'],
 'authz_analyzer.datastores.aws.analyzer.redshift': ['commands/*'],
 'authz_analyzer.datastores.postgres': ['commands/*'],
 'authz_analyzer.datastores.snowflake': ['commands/*'],
 'tests.tests_datastores.aws.aws_ptrp': ['resolve_permissions_test_inputs/deny_with_condition/*',
                                         'resolve_permissions_test_inputs/iam_user_to_s3_bucket/*',
                                         'resolve_permissions_test_inputs/multi_iam_users_to_multi_s3_buckets/*',
                                         'resolve_permissions_test_inputs/not_action/*',
                                         'resolve_permissions_test_inputs/s3_resource_regex/*']}

install_requires = \
['boto3>=1.26.27,<2.0.0',
 'click==8.1.3',
 'google-api-python-client>=2.66.0,<2.67.0',
 'google-cloud-bigquery>=2.1.0,<3.0',
 'google-cloud-iam>=2.10.0,<3.0.0',
 'google-cloud-resource-manager>=1.6.3,<2.0',
 'networkx>=2.8.8,<3.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'psycopg2>=2.9.5,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'pyserde>=0.9.6,<0.10.0',
 'redshift-connector>=2.0.909,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'snowflake-connector-python==3.0.0']

extras_require = \
{'test': ['pytest>=7.2.0,<8.0.0',
          'pytest-cov>=4.0.0,<5.0.0',
          'black>=22.12.0,<23.0.0',
          'isort>=5.11.3,<6.0.0',
          'twine>=4.0.2,<5.0.0']}

entry_points = \
{'console_scripts': ['authz-analyzer = authz_analyzer.cli:main']}

setup_kwargs = {
    'name': 'authz-analyzer',
    'version': '0.1.1',
    'description': 'Analyze DB authorization.',
    'long_description': 'authz-analyzer (AKA Authorization Analyzer) helps DevOps and data engineers quickly understand who has access to what data and how.\n\nDevOps and data engineers are often tasked with managing the security of the databases, data lakes or warehouses they operate. This usually involves setting permissions to enable users to query the data they need. However, as the number of users and use-cases increase, complexity explodes. It\'s no longer humanly possible to remember who had access to what, how and why, which makes meeting security and compliance requirements impossible.\n\nThe root cause of this problem is that permissions to data are usually stored in normalized form, which is great for evaluating permissions but not so great when you want to clearly understand your permissions landscape. When asked "how come Joe can query that table?", it can be a long process to get to a definitive answer and that\'s just time we don\'t have. With so many data stores, each with its own security model, it\'s not feasible to manage it all manually.\n\nIdentifying this was an issue for many of our customers, the team at [Satori](https://satoricyber.com) decided to build *Authorization Analytics*, a service that helps admins to better manage their data store permissions. We believe no one should have to sift through DB system tables to get a clear picture of who can do what with data.\n\n## Using Authorization Analytics\nAuthz Analytics is available in two ways:\n1. authz-analyzer open source CLI - scan the permissions structure of a database to get the list of all users and data assets they can access.\n2. Satori Authorization Analytics - a fully managed SaaS solution to periodically scan, store and visualize all users and data assets they can access. Learn more [here](https://satoricyber.com).\n\n## Supported Data Stores\nAuthz Analytics support the following data stores, with more on the way:\n\n* [Amazon Redshift](docs/datastores/redshift.md)\n* [Amazon S3](docs/datastores/s3.md)\n* [Google BigQuery](docs/datastores/bigquery.md)\n* [MongoDB](docs/datastores/mongodb.md)\n* [PostgreSQL](docs/datastores/postgresql.md)\n* [Snowflake](docs/datastores/snowflake.md)\n\n## Contributing\nPlease follow the [contributing guidelines](CONTRIBUTING.md).\n\n## Credits\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'SatoriCyber',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/satoricyber/authz-analyzer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
