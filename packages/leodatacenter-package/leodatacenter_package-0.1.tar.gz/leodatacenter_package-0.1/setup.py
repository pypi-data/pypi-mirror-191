from setuptools import setup

setup(
    name='leodatacenter_package',
    version='0.1',
    description='A package for managing the datacenter',
    author_email='N.Dulal@leonardogermany.com',
    author='LEONARDO Germany GmbH',
    install_requires=[
        'influxdb-client',
    ],
)
