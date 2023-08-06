# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnus_extension_datastore_s3']

package_data = \
{'': ['*']}

install_requires = \
['magnus>=0.4.1,<0.5.0', 'magnus_extension_aws_config>=0.2,<0.3']

entry_points = \
{'magnus.datastore.BaseRunLogStore': ['s3 = '
                                      'magnus_extension_datastore_s3.s3:S3Store'],
 'magnus.integration.BaseIntegration': ['local-container-run_log_store-s3 = '
                                        'magnus_extension_datastore_s3.integration:LocalContainerComputeS3Store',
                                        'local-run_log_store-s3 = '
                                        'magnus_extension_datastore_s3.integration:LocalComputeS3RunLogStore']}

setup_kwargs = {
    'name': 'magnus-extension-datastore-s3',
    'version': '0.2.0',
    'description': 'Magnus extension for S3 as run log store',
    'long_description': '# S3 Run Log store\n\nThis package is an extension to [magnus](https://github.com/AstraZeneca/magnus-core).\n\n## Provides \nProvides the functionality to use S3 buckets as run log stores.\n\n## Installation instructions\n\n```pip install magnus_extension_datastore_s3```\n\n## Set up required to use the extension\n\nAccess to AWS environment either via:\n\n- AWS profile, generally stored in ~/.aws/credentials\n- AWS credentials available as environment variables\n\nIf you are using environmental variables for AWS credentials, please set:\n\n- AWS_ACCESS_KEY_ID: AWS access key\n- AWS_SECRET_ACCESS_KEY: AWS access secret\n- AWS_SESSION_TOKEN: The session token, useful to assume other roles\n\nA S3 bucket that you want to use to store the run log store.\n\nSince the run log would be modified frequently as part of the run, we recommend \n[switching off versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html) of files in\nthe S3 bucket.\n\n\n## Config parameters\n\nThe full configuration of S3 Run log store are:\n\n```yaml\nrun_log:\n  type: s3\n  config:\n    s3_bucket: # Bucket name, required\n    region: # Region if we are using\n    aws_profile: #The profile to use or default\n    use_credentials: # Defaults to False\n```\n\n### **s3_bucket**:\n\nThe s3 bucket you want to use for storing the run logs.\n\nPlease note that S3 run log store is not concurrent friendly and therefore might be inconsistent \nif you are running parallel steps.\n\nThe below parameters are inherited from AWS Configuration.\n\n### **aws_profile**:\n\nThe profile to use for acquiring boto3 sessions. \n\nDefaults to None, which is used if its role based access or in case of credentials present as environmental variables.\n\n### **region**:\n\nThe region to use for acquiring boto3 sessions.\n\nDefaults to *eu-west-1*.\n\n\n### **aws_credentials_file**:\n\nThe file containing the aws credentials.\n\nDefaults to ```~/.aws/credentials```.\n\n### **use_credentials**:\n\nSet it to ```True``` to provide AWS credentials via environmental variables.\n\nDefaults to ```False```.\n\n### ***role_arn***:\n\nThe role to assume after getting the boto3 session.\n\n**This is required if you are using ```use_credentials```.**\n',
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
