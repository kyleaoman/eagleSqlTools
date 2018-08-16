from setuptools import setup

setup(
    name='eagleSqlTools',
    version='2.0',
    description='Utilities for accessing EAGLE public database.',
    url='',
    author='Kyle Oman',
    author_email='koman@astro.rug.nl',
    license='GNU GPL v3',
    packages=['eagleSqlTools'],
    install_requires=["numpy"],
    include_package_data=True,
    zip_safe=False
)
