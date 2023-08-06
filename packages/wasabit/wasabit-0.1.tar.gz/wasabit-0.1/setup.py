from setuptools import setup, find_packages

setup(
    name='wasabit',
    version='0.1',
    description='This package offers a solution for uploading files, creating folders, and authenticating with Wasabi',
    author='Saurabh Harak',
    author_email='saurabh_harak@isb.edu',
    packages=find_packages(),
    install_requires=[
        'boto3==1.26.65',
        'botocore==1.29.65',
        'jmespath==1.0.1',
        'python-dateutil==2.8.1',
        's3transfer==0.6.0',
        'six==1.16.0',
        'urllib3==1.26.14',
        
    ],
)
