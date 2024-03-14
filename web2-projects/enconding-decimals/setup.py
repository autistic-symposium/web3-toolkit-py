from setuptools import setup, find_packages

setup(
    name='efun',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Mia Stein',
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        efun=src.main:main
    ''',
)