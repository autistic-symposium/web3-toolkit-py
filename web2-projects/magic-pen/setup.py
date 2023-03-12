from setuptools import setup, find_packages

setup(
    name='epen',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    author='steinkirch',
    entry_points='''
        [console_scripts]
        epen=src.main:main
    ''',
)