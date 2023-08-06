#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup

with open("requirements.txt") as fp:
    install_requires = fp.read()

package_name = "byb"
package_version = "0.0.1"

setup(
    name=package_name,
    version=package_version,
    description="byb",
    author="Globally Limited",
    author_email="dev@globally.ltd",
    url="https://byb.globally.ltd",
    packages=find_packages(),
    package_data={"byb": ["bots/assets/*"]},
    include_package_data=True,
    entry_points={"console_scripts": ["byb=byb.cli:main"]},
    install_requires=install_requires,
    test_suite=None,
)
