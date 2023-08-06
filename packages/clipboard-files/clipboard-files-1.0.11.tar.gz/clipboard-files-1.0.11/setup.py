from setuptools import setup, find_packages

setup(
    name='clipboard-files',
    version='1.0.11',
    description='A script for copying file contents to the clipboard. cf is the command',
    author='Nadav Goldstein',
    packages=["app"],
    install_requires=[
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'cf=app.main:main',
        ],
    },
)
