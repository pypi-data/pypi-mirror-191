from setuptools import setup

with open("README.md", "r", encoding="UTF-8") as readme:
    long_description = readme.read()

setup(
    name="PythonPoet",
    version="0.1.4",
    author="Pelfox",
    author_email="me@pelfox.dev",
    description="API for generating Python source code from runtime.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pelfox/PythonPoet",
    project_urls={
        "Bug Tracker": "https://github.com/Pelfox/PythonPoet/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    include_package_data=True,
)
