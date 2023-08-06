from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0'
DESCRIPTION = 'Package From Cras7h'

# Setting up
setup(
    name="cras7h",
    version=VERSION,
    author="Cras7h",
    author_email="<x@cras7h.de>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['vardxg'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
