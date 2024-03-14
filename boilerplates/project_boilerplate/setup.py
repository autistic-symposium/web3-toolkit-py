from setuptools import setup, find_packages

setup(
    name="my_package",
    version='0.1',
    packages=find_packages(include=['src', \
                    'src.utils']),
    author="mia stein",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['my_package=src.main:run']
    },
)