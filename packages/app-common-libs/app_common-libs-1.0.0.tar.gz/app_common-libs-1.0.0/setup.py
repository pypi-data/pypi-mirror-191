import os
from setuptools import setup, find_packages

REQUIREMENTS_FILE = 'requirements.txt'
here = os.path.abspath(os.path.dirname(__file__))

rq = ['aiohttp==3.6.2',
      'async-timeout==3.0.1',
      'attrs==19.3.0',
      'aurora-data-api==0.2.0',
      'blinker==1.4',
      'certifi==2019.11.28',
      'chardet==3.0.4',
      'Click==7.0',
      'colorama==0.4.3',
      'docutils==0.16',
      'dynamorm==0.9.14',
      'idna==2.8',
      'iso8601==0.1.12',
      'itsdangerous==1.1.0',
      'jmespath==0.9.5',
      'MarkupSafe==1.1.1',
      'marshmallow==3.6.0',
      'marshmallow-jsonapi==0.22.0',
      'pyasn1==0.4.8',
      'pymysql==0.9.3',
      'python-dateutil==2.8.1',
      'PyYAML==5.3',
      'pytz==2019.3',
      'requests==2.22.0',
      'rsa==4.0',
      's3transfer==0.3.3',
      'simplejson==3.17.0',
      'SQLAlchemy==1.3.16',
      'six==1.14.0',
      'stripe==2.41.1',
      'slackclient==2.5.0',
      'urllib3==1.25.8',
      'Werkzeug==0.16.1',
      'websocket-client==0.47.0',
      'yarl==1.4.2']


def read(file_name):
    # Get the long description from the README file
    with open(os.path.join(here, file_name)) as f:
        return f.read()


def read_lines(file_name):
    return read(file_name).splitlines()


setup(
    name='app_common-libs',
    version='1.0.0',
    packages=find_packages(include=['app_common', 'app_common.*', 'requirements.txt']),
    url='',
    license='proprietary',
    author='vikas.goyal',
    author_email='vikas@mobilads.co',
    description='Mobilads common libs and functions for backend application',
    long_description='Mobilads common libs and functions for backend application',
    include_package_data=True,
    install_requires=rq
)
