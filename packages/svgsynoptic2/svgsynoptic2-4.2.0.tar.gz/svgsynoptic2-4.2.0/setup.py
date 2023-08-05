#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="svgsynoptic2",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Widget for displaying a SVG synoptic.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Johan Forsberg",
    author_email="johan.forsberg@maxiv.lu.se",
    license="GPLv3",
    python_requires=">=3.6",
    install_requires=["pytango>=9.2.1", "taurus>=4.5", "pyqtwebengine"],
    url="https://gitlab.com/MaxIV/lib-maxiv-svgsynoptic",
    packages=find_packages(),
    include_package_data=True,
    package_data={"svgsynoptic2": ["web/js/*.js", "web/js/libs/*.js", "web/css/*.css"]},
)
