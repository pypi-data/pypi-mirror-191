from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'reading a csv file from a website'

from setuptools import setup, find_packages
import sys
import os
import configparser

def save_config(directory):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'output_dir': directory}
    with open('configure.ini', 'w') as configfile:
        config.write(configfile)

for arg in sys.argv:
    if arg.startswith('--output_dir='):
        directory = arg.split('=')[1]
        save_config(directory)

setup(
    name='eng_task',
    version=VERSION,
    description='Example package',
    author='Jack Edmundson',
    author_email='jackedmundson1997@gmail.com',
    packages=find_packages(),
    data_files=[('.', ['configure.ini'])],
    install_requires=['configparser']
)
    