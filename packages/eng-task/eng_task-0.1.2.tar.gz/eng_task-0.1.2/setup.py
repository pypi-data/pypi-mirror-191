import argparse
import configparser
import sys
from setuptools import setup, find_packages

def save_config(directory):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'output_dir': directory}
    with open('configure.ini', 'w') as configfile:
        config.write(configfile)

if 'sdist' in sys.argv or 'bdist_wheel' in sys.argv:
    # Building a distribution package, no need to handle options
    pass
else:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=str, help='output directory')
    args = parser.parse_args()

    if args.output_dir:
        save_config(args.output_dir)

setup(
    name='eng_task',
    version='0.1.2',
    description='Example package',
    author='Jack Edmundson',
    author_email='jackedmundson1997@gmail.com',
    packages=find_packages(),
    install_requires=[
        # List all other packages your package depends on here
        'configparser',
        'pandas',
        'requests',
        'beautifulsoup4',
    ],
    data_files=[('.', ['configure.ini'])],
)

