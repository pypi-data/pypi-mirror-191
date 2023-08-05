# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cf_extension_core']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.50,<2.0.0', 'cloudformation-cli-python-lib>=2.1.14,<3.0.0']

setup_kwargs = {
    'name': 'cf-extension-core',
    'version': '0.1.dev20230210165850',
    'description': 'Provides common functionality for Custom resources in CloudFormation.',
    'long_description': '# Summary\n- Helper to enable all types of resource types for create/update/read/list operations\n- Heavily inspired to use dynamodb for resource management.  Supports all native create/read/update/list/delete operations for any resource.\n- Dynamic identifier generation to support any resource identifier use case.  Read Only resources or real resource creation.\n\n# Required extra permissions in each handlers permissions:\n- Due to us using dynamodb as a backend, we need extra permissions to store/retrieve state information from dynamo.  These permissions should be added in addition to any other required permissions by each handler.\n\n  - dynamodb:CreateTable\n  - dynamodb:PutItem\n  - dynamodb:DeleteItem\n  - dynamodb:GetItem\n  - dynamodb:UpdateItem\n  - dynamodb:UpdateTable\n  - dynamodb:DescribeTable\n  - dynamodb:Scan\n\n\n# Development\n- High level commands\n   ```\n    curl -sSL https://install.python-poetry.org | python3 -\n    export PATH="/Users/nicholascarpenter/.local/bin:$PATH"\n    poetry --version\n    poetry add boto3\n  \n    poetry add --group dev  pytest\n  \n    poetry install --no-root\n    poetry build\n    poetry config pypi-token.pypi ""\n    poetry publish\n  ```\n- Generating Stubs after all 3rd party stubs are installed\n    ```\n    find src/ -type f -name \'*.pyi\' -exec rm {} +\n    stubgen src/ -o src/  --include-private \n    ```\n  - Do not run again after manually changed.\n  - Build system updated to validate stubs via `stubtest`\n\n',
    'author': 'Nick Carpenter',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
