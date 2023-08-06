from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="cetl",
    version='0.0.5',
    author="Clement",
    author_email="<cheukub@gmail.com>",
    description='A basic data pipeline tools for data engineer to handle the CRM or loyalty data',
    packages=find_packages(),
    install_requires=['flask', 'SQLalchemy', 'pyspark', 'pandas'],
    keywords=['python', 'data pipeline', 'pipeline'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ]
)