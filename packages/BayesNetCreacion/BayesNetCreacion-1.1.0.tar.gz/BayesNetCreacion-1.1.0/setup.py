from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'Library capable of creating Bayesian Networks and making probabilistic inference over them, as well additional functions'
LONG_DESCRIPTION = 'This library has the objective of building Bayesian networks and making probabilistic inference over them. Also, adding some other additional features that could serve the developers that make use of this library. This library has zero dependencies to assure it is futureproof, easier to debug, to contribute to and use. For the most part this library works over classes like BayesNetCreacion and Node, this was chosen so that in a way it could facilitate the usage of the OOP paradigm.'

# Setting up
setup(
    name="BayesNetCreacion",
    version=VERSION,
    author="Andres de la Roca",
    author_email="<dela20332@uvg.edu.gt>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'bayes', 'bayesian network', 'zero dependencies', 'bayesian inference', 'python3', 'open source'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)