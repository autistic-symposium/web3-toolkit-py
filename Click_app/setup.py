from setuptools import setup, find_packages

setup(
    name='yourapp',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Mia von Steinkirch',
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        yourapp=yourapp.yourapp:main
    ''',
)