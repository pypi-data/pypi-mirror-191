# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnus_extension_catalog_s3']

package_data = \
{'': ['*']}

install_requires = \
['magnus>=0.4.1,<0.5.0',
 'magnus_extension_aws_config>=0.2.0,<0.3.0',
 'pydantic>=1.10.4,<2.0.0']

entry_points = \
{'magnus.catalog.BaseCatalog': ['s3 = '
                                'magnus_extension_catalog_s3.s3:S3Catalog'],
 'magnus.integration.BaseIntegration': ['local-container-catalog-s3 = '
                                        'magnus_extension_catalog_s3.integration:LocalContainerComputeS3Catalog']}

setup_kwargs = {
    'name': 'magnus-extension-catalog-s3',
    'version': '0.2.0',
    'description': 'Magnus extension to provide S3 Catalog functionality',
    'long_description': '# S3 catalog provider\n\nThis package is an extension to [magnus](https://github.com/AstraZeneca/magnus-core).\n\n## Provides \nProvides functionality to use S3 buckets as catalog provider.\n\n## Installation instructions\n\n```pip install magnus_extension_catalog_s3```\n\n## Set up required to use the extension\n\nAccess to AWS environment either via:\n\n- AWS profile, generally stored in ~/.aws/credentials\n- AWS credentials available as environment variables\n\nIf you are using environmental variables for AWS credentials, please set:\n\n- AWS_ACCESS_KEY_ID: AWS access key\n- AWS_SECRET_ACCESS_KEY: AWS access secret\n- AWS_SESSION_TOKEN: The session token, useful to assume other roles\n\nA S3 bucket that you want to use to store the catalog objects.\n\n## Config parameters\n\nThe full configuration required to use S3 as catalog is:\n\n```yaml\ncatalog:\n  type: s3\n  config:\n    compute_data_folder : # defaults to data/\n    s3_bucket: # Bucket name, required\n    region: # Region if we are using\n    aws_profile: #The profile to use or default\n    use_credentials: # Defaults to False\n\n```\n\n### **compute_data_folder**:\n\nThe ```data``` folder that is used for your work. \n\nLogically cataloging works as follows:\n\n- get files from the catalog before the execution to a specific compute data folder\n- execute the command\n- put the files from the compute data folder to the catalog.\n\n\nYou can over-ride the compute data folder, defined globally, for individual steps by providing it in the step \nconfiguration.\n\nFor example:\n\n```yaml\ncatalog:\n  ...\n\ndag:\n  steps:\n    step name:\n      ...\n      catalog:\n        compute_data_folder: # optional and only apples to this step\n        get:\n          - list\n        put:\n          - list\n\n    ...\n```\n\nThe below parameters are inherited from AWS Configuration.\n\n### **aws_profile**:\n\nThe profile to use for acquiring boto3 sessions. \n\nDefaults to None, which is used if its role based access or in case of credentials present as environmental variables.\n\n### **region**:\n\nThe region to use for acquiring boto3 sessions.\n\nDefaults to *eu-west-1*.\n\n\n### **aws_credentials_file**:\n\nThe file containing the aws credentials.\n\nDefaults to ```~/.aws/credentials```.\n\n### **use_credentials**:\n\nSet it to ```True``` to provide AWS credentials via environmental variables.\n\nDefaults to ```False```.\n\n### ***role_arn***:\n\nThe role to assume after getting the boto3 session.\n\n**This is required if you are using ```use_credentials```.**\n',
    'author': 'Vijay Vammi',
    'author_email': 'vijay.vammi@astrazeneca.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AstraZeneca/magnus-extensions/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
