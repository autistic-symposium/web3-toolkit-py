from setuptools import setup, find_packages

setup(
    name='yourapp',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Mia Stein',
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        src=src.main:main
    ''',
)