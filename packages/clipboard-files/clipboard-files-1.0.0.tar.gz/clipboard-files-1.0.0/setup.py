from setuptools import setup, find_packages

setup(
    name='clipboard-files',
    version='1.0.0',
    description='A script for copying file contents to the clipboard. cf is the command',
    author='Nadav Goldstein',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'curses',
    ],
    entry_points={
        'console_scripts': [
            'cf=app.main:main',
        ],
    },
)
