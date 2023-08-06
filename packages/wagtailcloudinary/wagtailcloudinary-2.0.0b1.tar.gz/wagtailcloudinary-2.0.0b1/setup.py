#!/usr/bin/env python
from setuptools import setup, find_packages, Distribution
import codecs
import os.path

# Make sure versiontag exists before going any further
Distribution().fetch_build_eggs("versiontag>=1.2.0")

from versiontag import get_version, cache_git_tag  # NOQA


packages = find_packages("src")

install_requires = [
    "cloudinary>=1.28.1,<1.29.0",
    "python-dateutil>=2.7",
    "wagtail>=3.0,<4.2",
]
extras_require = {
    "development": ["flake8>=3.3.0", "tox>=2.7.0", "ipdb"],
}


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding="utf-8").read()


cache_git_tag()

setup(
    name="wagtailcloudinary",
    version=get_version(pypi=True),
    package_dir={"": "src"},
    packages=packages,
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    license="BSD Licence",
    description="Cloudinary support for Wagtail CMS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/thelabnyc/wagtailcloudinary",
    author="Davor Teskera",
    author_email="dteskera@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Wagtail",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
