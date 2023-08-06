"""Setup script for realpython-reader"""

import os.path
from setuptools import find_packages , setup


# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
# packages=find_packages(include=['pyapi']),
setup(
    name="algomojo",
    version="1.0",
    description="Algomojo - Arrow API Python Client V1",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://algomojo.com/docs/",
    author="Algomojo",
    author_email="support@algomojo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests"
    ],
)
