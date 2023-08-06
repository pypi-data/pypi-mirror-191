import pathlib
from setuptools import setup, find_packages


setup(
        name='zpy-database',
        version='0.1.1',
        author='Guillermo de la Iglesia',
        author_email='mail@zguillez.io',
        description='Pyton database wrapper',
        long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
        long_description_content_type='text/markdown',
        url='https://github.com/zguillez/zpy-database',
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'pymysql',
        ],
)
