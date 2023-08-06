from setuptools import setup, find_packages

setup(
    name='neer',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='UNLICENSED',
    description='Python package to hold a centralized set of PostgreSQL table references.',
    long_description='Python package to hold a centralized set of PostgreSQL table references.',
    url='https://github.com/NEERINC/pyoneer',
    install_requires=['sqlalchemy', 'loguru', 'dotenv']
)
