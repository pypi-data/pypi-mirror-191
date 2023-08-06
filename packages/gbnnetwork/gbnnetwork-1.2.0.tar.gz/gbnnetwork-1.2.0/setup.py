from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2.0'
DESCRIPTION = 'Implementation of Bayesian network.'
LONG_DESCRIPTION = 'A package that allows to build simple Bayes networks and infere probabilities.'

# Setting up
setup(
    name="gbnnetwork",
    version=VERSION,
    author="Guillermo",
    author_email="san191517@uvg.edu.gt",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[''],
    keywords=['python', 'probability', 'bayes'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)