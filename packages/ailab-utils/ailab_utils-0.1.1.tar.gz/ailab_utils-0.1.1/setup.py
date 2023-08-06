from ailab_utils import __version__

from collections import OrderedDict

import os
import setuptools

ENV_VERSION = os.getenv("VERSION")

version = __version__ if ENV_VERSION is None else ENV_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ailab_utils",
    version=f"{version}",
    author="GPAM",
    author_email="gpam@gmail.com",
    description="AiLab utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://gitlab.com/gpam/services/ailab-utils",
    packages=setuptools.find_packages(include=["ailab_utils", "ailab_utils.*"]),
    python_requires=">=3.6.0",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://gitlab.com/gpam/services/ailab-utils"),
            ("Code", "https://gitlab.com/gpam/services/ailab-utils"),
            (
                "Issue tracker",
                "https://gitlab.com/gpam/services/ailab-utils/-/issues",
            ),
            ("Changelog", "https://gitlab.com/gpam/services/ailab-utils/-/releases"),
            (
                "Contribution guide",
                "https://gitlab.com/gpam/services/ailab-utils/-/blob/main/CONTRIBUTING.md",
            ),
        )
    ),
    install_requires=[],
    tests_require=[
        "pytest",
        "flake8",
        "pytest-cov",
        "pytest-mock",
        "isort",
        "black",
    ],
    setup_requires=["setuptools>=38.6.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
    ],
)
