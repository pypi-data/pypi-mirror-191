import sys
import getopt

from setuptools import setup, find_packages

arguments = []
for arg in sys.argv:
    if arg.startswith("--version"):
        arguments.append(arg)

if len(arguments) > 0:
    sys.argv.remove(arguments[0])

optlist, _ = getopt.getopt(arguments, "", ["version="])

version = "0.0.0"
if len(optlist) > 0 and optlist[0][0] == "--version":
    version = optlist[0][1]

setup(
    name="levatas-alira",
    version=version,
    description="Alira",
    url="https://github.com/vinsa-ai/alira",
    author="Levatas",
    author_email="svpino@gmail.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "PyYAML>=6.0, <6.1",
        "redis>=4.4, <4.5",
        "rq>=1.12, <1.13",
        "rq-scheduler>=0.11, <0.12",
        "requests>=2.28, <2.29",
        "boto3",
        "twilio",
        "jmespath>=1.0, <1.1",
        "sqlalchemy>=1.4, <1.5",
        "pymysql>=1.0, <1.1"
    ],
)
