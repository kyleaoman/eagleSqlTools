from setuptools import setup
import os

with open(
        os.path.join(os.path.dirname(__file__), 'eagleSqlTools', 'VERSION')
) as version_file:
    version = version_file.read().strip()

setup(
    name='eagleSqlTools',
    version=version,
    description='Utilities for accessing EAGLE public database.',
    url='',
    author='Kyle Oman',
    author_email='koman@astro.rug.nl',
    license='GNU GPL v3',
    packages=['eagleSqlTools'],
    install_requires=['numpy'],
    include_package_data=True,
    zip_safe=False
)
