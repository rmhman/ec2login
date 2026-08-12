#!/usr/bin/env python3
"""Setup configuration for ec2login package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ec2login",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Interactive AWS EC2 instance selector with SSM Session Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ec2login",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.7",
    install_requires=[
        "boto3>=1.26.0",
    ],
    entry_points={
        "console_scripts": [
            "ec2login=ec2login.cli:main",
        ],
    },
    include_package_data=True,
)
