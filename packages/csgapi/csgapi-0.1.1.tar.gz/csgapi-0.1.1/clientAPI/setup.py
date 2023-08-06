# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="csgapi",
    version="0.1.1",
    description="API for interacting with the Computer Systems Genome database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://csgenome.org/",
    author="Ani Ramadoss",
    author_email="aniramadoss2002@vt.edu",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["clientAPI", "clientAPI.objects"],
    py_modules=["clientAPI.base", "clientAPI.client", "clientAPI.mixin", "clientAPI.utils"],
    include_package_data=True,
    install_requires=["flask", "requests"]
)
