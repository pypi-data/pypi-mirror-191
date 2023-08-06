from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "A simple Python class for measuring performance of processes"
LONG_DESCRIPTION = "A simple Python class for measuring performance of processes."

setup(
    name="perfov",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/cobanov/perfov/",
    author="Mert Cobanov",
    author_email="mertcobanov@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords="timer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
