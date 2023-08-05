from setuptools import setup, find_packages
from datetime import datetime

f = open("version.txt", "r+")
version = f.read()
print(version)
setup(
    name="std-logger",
    packages=find_packages(),
    version=version,
    description="logs tools",
    author="wei.fu",
    long_description='',
    long_description_content_type="text/markdown",
    author_email='mefuwei@163.com',
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['loguru', 'flask-log-request-id'],
)
print(version)
