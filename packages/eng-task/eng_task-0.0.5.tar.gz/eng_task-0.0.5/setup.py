from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'reading a csv file from a website'



# Setting up
setup(
    name="eng_task",
    version=VERSION,
    author="Jack Edmundson",
    author_email="<jackedmundson1997@gmail.com>",
    packages=find_packages(),
    include_package_data=True,
    intall_requires=['pandas','numpy'],
    entry_points={
        'console_scripts': [
            # List your command line scripts here
        ],
    },
    classifiers=[
        # List the classifiers for your package here
    ],
    data_files=[
        ('config', ['configure.ini']),
    ],
    # Add the following argument to pass the output directory when installing your package
    extras_require={
        'output_dir': ['output_dir']
    }
    )