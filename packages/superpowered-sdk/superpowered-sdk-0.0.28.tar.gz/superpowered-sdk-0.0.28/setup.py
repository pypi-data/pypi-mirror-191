#!/usr/bin/env python
#
# Copyright (c) 2023 Superpowered AI All right reserved.
#

import os

import setuptools

long_desc = """# Superpowered AI
Create Collaborative AI Agents with memory, tools, and knowledge bases.
"""

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r", encoding="utf-8") as fh:
        return fh.read()


setuptools.setup(
    name="superpowered-sdk",
    version="0.0.28",
    description="Superpowered AI SDK",
    license="Proprietary License",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://superpowered.ai",
    project_urls={
        "Homepage": "https://superpowered.ai",
        "Documentation": "https://superpowered.ai/docs",
        "Contact": "https://superpowered.ai/contact/",
        "End-User License Agreement": "https://superpowered.ai/api-user-agreement/"
    },
    author="superpowered",
    author_email="justin@superpowered.ai",
    keywords="Superpowered AI LLM Chat Agents",
    packages=setuptools.find_packages(),
    # install_requires=read("requirements.txt"),
    include_package_data=True,
    python_requires=">=3.6",
    # entry_points={
    #     'console_scripts': ['pinecone=pinecone.cli:main'],
    # },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
