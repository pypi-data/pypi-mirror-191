from setuptools import setup, find_packages
import codecs
import os
import configparser

VERSION = '0.2.2'
DESCRIPTION = 'reading a csv file from a website'

def create_config():
    config = configparser.ConfigParser()

    config["DEFAULT"] = {
        "output_dir":"/Users/jedmundson",
        "filenamme" : "raw.csv",
        "clean_data" : "_clean_data",
        "data_profiling" : "_data_profiling",
        "data_consistency" : "_data_consistency",
    }

    with open("configure.ini","w") as f:
        config.write(f)

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

create_config()