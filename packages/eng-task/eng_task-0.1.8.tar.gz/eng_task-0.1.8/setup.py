from setuptools import setup

setup(
    name='eng_task',
    version='0.1.8',
    description='Your package description',
    author='Jack Edmundson',
    author_email='jackedmundson1997@gmail.com',
    packages=['eng_task'],
    install_requires=['pandas','numpy','requests','configparser'],
    entry_points={
        'console_scripts': [
            'your_command=end_task.your_module:main'
        ]
    },
    options={
        'config': {
            'default_config_path': '../configure.ini',
            'config_path': 'configure.ini',
        }
    }
)


