import os
import sys
from setuptools import setup

INSTALL_REQUIRES = ['requests >=2.25.0']

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="slack_scraper",
    version="1.0.0",
    author="ClearFeed",
    author_email="dev@clearfeed.ai",
    description=("Python module to download threads and messages from Slack channels"),
    license="Apache License 2.0",
    keywords="clearfeed scrape slack",
    url="https://github.com/clearfeed/slack-scraper",
    packages=['slack-scraper'],
    scripts=['bin/slack-scraper.py'],
    install_requires=INSTALL_REQUIRES,
    long_description=read('README.md'),
    python_requires='>=3.6',
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ]
    )
