# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['RW',
 'RW.AWS',
 'RW.AWS.mixins',
 'RW.AWS.robot_tests',
 'RW.AWS.strategies',
 'RW.ArgoCD',
 'RW.Artifactory',
 'RW.CertManager',
 'RW.Chat',
 'RW.Chat.strategies',
 'RW.Datadog',
 'RW.Discord',
 'RW.GCP',
 'RW.GitHub',
 'RW.HashiCorp',
 'RW.K8s',
 'RW.Patroni',
 'RW.Postgres',
 'RW.Prometheus',
 'RW.Rest',
 'RW.RunWhen',
 'RW.SocialScrape',
 'RW.Sysdig',
 'RW.Uptime',
 'RW.Utils',
 'RW.scratch']

package_data = \
{'': ['*'],
 'RW.Artifactory': ['robot_tests/*'],
 'RW.CertManager': ['robot_tests/*'],
 'RW.Chat': ['robot_tests/*'],
 'RW.Discord': ['robot_tests/*'],
 'RW.GCP': ['robot_tests/*'],
 'RW.GitHub': ['robot_tests/*'],
 'RW.HashiCorp': ['robot_tests/*'],
 'RW.K8s': ['robot_tests/*'],
 'RW.Prometheus': ['robot_tests/*'],
 'RW.Sysdig': ['robot_tests/*'],
 'RW.Uptime': ['robot_tests/*']}

install_requires = \
['boto3>=0.0',
 'datadog-api-client==2.8.0',
 'dnspython>=0.0',
 'google-cloud-logging>=0.0',
 'google-cloud-monitoring>=0.0',
 'jmespath>=1.0.1',
 'jq>=1.3.0',
 'kubernetes>=0.0',
 'pandas>=1.5.2',
 'prometheus-client>=0.11.0',
 'protobuf>=0.0',
 'pyopenssl>=0.0',
 'python-benedict>=0.0',
 'robotframework>=4.1.2',
 'rocketchat-api>=0.0',
 'ruamel-base>=1.0.0',
 'ruamel-yaml>=0.17.20',
 'sdcclient>=0.16',
 'slack-sdk>=0.0',
 'snscrape>=0.4.3.20220106']

setup_kwargs = {
    'name': 'runwhen-keywords',
    'version': '0.0.1',
    'description': 'A set of RunWhen published keywords and python libraries',
    'long_description': 'None',
    'author': 'Kyle Forster',
    'author_email': 'kyle.forster@runwhen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
