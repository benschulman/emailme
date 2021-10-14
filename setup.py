from setuptools import find_packages
from setuptools import setup

setup(
    name="emailme",
    version="0.0.1",
    description="A simple emailer",
    url="https://github.com/benschulman/emailme",
    author="Ben Schulman",
    author_email="bgschulman31@gmail.com",
    packages=find_packages(),
    package_data={"emailme": ["templates/*.html"]},
    include_package_data=True,
    install_requires=[
        "Jinja2>=3.0.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
    ],
)
