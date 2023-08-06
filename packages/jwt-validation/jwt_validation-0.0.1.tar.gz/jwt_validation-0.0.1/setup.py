from setuptools import setup, find_packages

import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'JWT validation'
LONG_DESCRIPTION = 'Utilities used for JWT validation.'

# Setting up
setup(
    name="jwt_validation",
    version=VERSION,
    author="x227970",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyjwt == 2.6.0', 'cryptography == 39.0.0'],
    keywords=['python', 'JWT', 'validation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
