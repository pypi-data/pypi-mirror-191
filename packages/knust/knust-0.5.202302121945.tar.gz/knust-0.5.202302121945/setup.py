from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="knust",
    version=os.environ.get('PACKAGE_VERSION') or '0.3.dev0',
    author="Mirko Boehm",
    author_email="mirko@kde.org",
    description="Knust is a Python module to manage Raspberry Pi based thermostats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mirkoboehm/brot",
    packages=['knust_service'],
    include_package_data=True,
    package_data={
        "": ["*.yaml"],
    },
    install_requires=[
        'Click',
        'pyyaml',
        'humanize',
        'pydbus',
        'pygi',
        'humanize',
        'rpi-thingamajigs>=0.5'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
    ],
    entry_points='''
        [console_scripts]
        brot=brot.cli_brot:brot
        knust_service=knust_service.cli_knust_service:knust_service
    ''',
    python_requires='>=3.6',
)
