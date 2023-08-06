from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hello_world_pkg_wesley_wang",
    version="0.0.2",
    author="wesleywang",
    author_email="wangwes@gmail.com",
    description="This is a temporary description for the package.",
    long_description_content_type="text/markdown",
    url="",
    install_requires=["numpy"],
    license="MIT",
    keywords=["temporary", "hello", "world"],
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent"]
    )
