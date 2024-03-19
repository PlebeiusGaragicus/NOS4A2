from setuptools import setup, find_packages

from nosferatu_cli.version import VERSION

setup(
    name='nosferatu_cli',
    version=VERSION,
    description='A command-line utility for automated nostr AI bots',
    author='Pleberius Garagicus',
    author_email='plebeiusgaragicus@gmail.com',
    url='https://github.com/PlebeiusGaragicus/NOS4A2',
    packages=find_packages(),
    install_requires=[
        # List your app's dependencies here
        'python-dotenv',
        'bitcoin',
        'bech32',
        # 'nostr',
        'embit',
        'bip32',
        'bip39'
        # brew install autoconf automake libtool pkg-config
    ],
    classifiers=[
        # Choose classifiers from https://pypi.org/classifiers/
        # TODO:
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'nosferatu_cli=nosferatu_cli:main',
        ],
    },
)