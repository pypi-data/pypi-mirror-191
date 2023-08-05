import re
from pathlib import Path

import pkg_resources as pkg
from setuptools import find_packages, setup

# Settings
FILE = Path(__file__).resolve()
ROOT = FILE.parent  # root directory
README = (ROOT / "README.md").read_text(encoding="utf-8")
REQUIREMENTS = [f'{x.name}{x.specifier}' for x in pkg.parse_requirements((ROOT / 'requirements.txt').read_text())]


def get_version():
    file = ROOT / 'genjutsu/__init__.py'
    return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', file.read_text(), re.M)[1]


setup(
    name="genjutsu",  # name of pypi package
    version=get_version(),  # version of pypi package
    python_requires=">=3.7.0",
    license='GPL-3.0',
    description='Itachi Uchiha Genjustu',
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),  # required
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        "Intended Audience :: Developers", "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)", "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7", "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", "Programming Language :: Python :: 3.10",
        "Topic :: Software Development", "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition", "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS", "Operating System :: Microsoft :: Windows"],
    keywords="machine-learning, deep-learning, vision, ML, DL, AI")
