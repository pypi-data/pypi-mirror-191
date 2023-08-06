from setuptools import setup, find_packages
from ossctl import __version__

setup(
    name="ossctl",
    version=__version__,
    author="wangziling100",
    author_email="wangziling100@163.com",
    description="oss command line controller",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)