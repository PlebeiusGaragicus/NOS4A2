from setuptools import setup, find_packages

# from nosferatu_cli.version import VERSION
VERSION = '0.1.1' # TODO - why the fuck doesn't this work?  It works for my nospy... FUUUUUUUUU

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
        # 'nostr',

        'python-dotenv',
        'websocket-client',
        # 'requests',
        'embit',
        'bitcoin',
        'bech32',
        'bip32',
        'bip39',
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