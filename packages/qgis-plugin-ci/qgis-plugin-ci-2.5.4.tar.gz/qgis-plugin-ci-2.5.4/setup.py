#! python3  # noqa: E265

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pathlib
import sys

# 3rd party
from setuptools import setup

# package (to get version)
from qgispluginci import __about__

# ############################################################################
# ########## Globals #############
# ################################

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

with open(HERE / "requirements/base.txt") as f:
    requirements = [
        line
        for line in f.read().splitlines()
        if not line.startswith(("#", "-")) and len(line)
    ]
with open(HERE / "requirements/development.txt") as f:
    dev_requirements = [
        line
        for line in f.read().splitlines()
        if not line.startswith(("#", "-")) and len(line)
    ]

python_min_version = (3, 7)

# This string might be updated on CI on runtime with a proper semantic version name with X.Y.Z
VERSION = "2.5.4"

if "." not in VERSION:
    # If VERSION is still not a proper semantic versioning with X.Y.Z
    # let's hardcode 0.0.0
    VERSION = "0.0.0"

# ############################################################################
# ########## Setup #############
# ##############################


if sys.version_info < python_min_version:
    sys.exit(
        "qgis-plugin-ci requires at least Python version {vmaj}.{vmin}.\n"
        "You are currently running this installation with\n\n{curver}".format(
            vmaj=python_min_version[0], vmin=python_min_version[1], curver=sys.version
        )
    )

setup(
    name="qgis-plugin-ci",
    author=__about__.__author__,
    author_email=__about__.__email__,
    description=__about__.__summary__,
    packages=["qgispluginci", "scripts"],
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["qgis-plugin-ci = scripts.qgis_plugin_ci:main"]},
    package_data={"qgispluginci": ["plugins.xml.template"]},
    version=VERSION,
    url=__about__.__uri__,
    project_urls={
        "Docs": "https://opengisch.github.io/qgis-plugin-ci/",
        "Bug Reports": "{}issues/".format(__about__.__uri__),
        "Source": __about__.__uri__,
    },
    download_url="https://github.com/opengisch/qgis-plugin-ci/archive/{}.tar.gz".format(
        VERSION
    ),
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    python_requires=">={vmaj}.{vmin}".format(
        vmaj=python_min_version[0], vmin=python_min_version[1]
    ),
    # metadata
    keywords=["QGIS", "CI", "changelog", "plugin"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: GIS",
    ],
)
