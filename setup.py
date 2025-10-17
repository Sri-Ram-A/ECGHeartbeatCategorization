import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


requirements = [
    # use environment.yml
]


setup(
    name="ECGHeartbeatCategorization",
    version="0.0.1",
    url="https://github.com/Sri-Ram-A/ECGHeartbeatCategorization",
    author="SriRam.A",
    author_email="srirama.ai23@rvce.edu.in",
    description="This package deals with the DBMS project of 5th semester where there is MQTT based communication between multiple RaspberryPI and A central JetsonNano , where a REFLEX based UI is used in the central server and Custom tkinter based GUI in the PIs for connecting",
    long_description=read("README.rst"),
    packages=find_packages(exclude=("tests",)),
    entry_points={
        "console_scripts": [
            "ECGHeartbeatCategorization=ECGHeartbeatCategorization.cli:cli"
        ]
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
