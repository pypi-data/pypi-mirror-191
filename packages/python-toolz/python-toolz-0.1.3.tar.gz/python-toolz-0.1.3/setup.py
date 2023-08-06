import pathlib
from setuptools import setup, find_packages


setup(
        name='python-toolz',
        version='0.1.3',
        author='Guillermo de la Iglesia',
        author_email='mail@zguillez.io',
        description='Pyton helpers',
        long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
        long_description_content_type='text/markdown',
        url='https://github.com/zguillez/python-toolz',
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'numpy',
            'pandas',
        ],
)
