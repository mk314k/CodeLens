from setuptools import setup, find_packages

setup(
    name='CodeLens',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'parse = codelens.parser:build_fs',
        ],
    },
)