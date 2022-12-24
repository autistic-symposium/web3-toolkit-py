from setuptools import setup, find_packages

setup(
    name='testing_app_name',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    author='steinkirch',
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        testing_app_name=src.main:main
    ''',
)