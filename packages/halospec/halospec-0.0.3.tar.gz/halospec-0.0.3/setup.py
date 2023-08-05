import setuptools
import os
import codecs
import re

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

long_description = "Halo Spectroscopy for JWST/MIRI"
    
here = os.path.abspath(os.path.dirname(__file__))
def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# DEPENDENCIES
# 1. What are the required dependencies?
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
# 2. What dependencies required to run the unit tests? (i.e. `pytest --remote-data`)
# tests_require = ['pytest', 'pytest-cov', 'pytest-remotedata']


setuptools.setup(
    name="halospec",
    version=find_version("halospec", "__init__.py"),
    description="Halo Spectroscopy for JWST/MIRI",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    
    author="Benjamin Pope",
    author_email="b.pope@uq.edu.au",
    url="https://github.com/benjaminpope/halospec",
    
    project_urls={
        "Bug Tracker": "https://github.com/benjaminpope/halospec/issues",
    },
    
    # package_dir={"": "src"},
    packages=["halospec"],
    
    install_requires=install_requires,
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    # packages = ["src"] + setuptools.find_namespace_packages(where = "src")
)
