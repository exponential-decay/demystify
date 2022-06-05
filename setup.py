"""Setuptools for demystify"""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

version = {}
with open("src/demystify/libs/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="demystify-digipres",
    version=version.get("__version__"),
    description="Static analysis tool for file format identification reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exponential-decay/demystify",
    author="Ross Spencer",
    author_email="all.along.the.watchtower2001+github@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "Topic :: System :: Archiving",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    keywords="digital-preservation, file-analysis, string-analysis, filename-analysis",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9, <4",
    entry_points={"console_scripts": ["demystify=demystify.demystify:main"]},
    project_urls={
        "Bug Reports": "https://github.com/exponential-decay/demystify/issues",
        "Source": "https://github.com/exponential-decay/demystify",
        "Ko-Fi": "https://ko-fi.com/beet_keeper",
    },
)
