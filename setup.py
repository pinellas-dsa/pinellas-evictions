"""Setup script for evictions package."""
import os

from setuptools import find_packages
from setuptools import setup


setup(
    name="evictions",  # update this to reflect your project name
    version="1.0.0",
    description="Code for PDSA evictions scraper",
    author="James Trimarco",  # change this to your name or org
    author_email="james.trimarco@gmail.com",  # change this to your email
    install_requires=[],
    include_package_data=True,
    package_dir={"": "src"},  # this is required to access code in src/
    packages=find_packages(where="src"),  # same as above
)
