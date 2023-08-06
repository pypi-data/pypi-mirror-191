from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rpi-thingamajigs",
    version=os.environ.get('PACKAGE_VERSION') or '0.3.dev0',
    author="Mirko Boehm",
    author_email="mirko@kde.org",
    description="Raspberry Pi Thingamajigs is a collection of Raspberry Pi related utilities like LCDD or character display interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mirkoboehm/rpi-thingamajigs",
    packages=[
        'rpithingamajigs',
        'rpithingamajigs/platform',
        'rpithingamajigs/logging',
        'rpithingamajigs/lcdd',
        'rpithingamajigs/lcdd/client', 
        'rpithingamajigs/lcdd/service',
        'rpithingamajigs/chardisplay_sysinfo',
        'rpithingamajigs/temperature_sensor'
    ],
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
        'psutil'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
    ],
    entry_points='''
        [console_scripts]
        lcdc=rpithingamajigs.lcdd.client.cli_lcdd_client:lcdd_client
        lcdd=rpithingamajigs.lcdd.service.cli_lcdd_service:lcdd
        chardisplay_sysinfo=rpithingamajigs.chardisplay_sysinfo.cli_chardisplay_sysinfo:chardisplay_sysinfo
    ''',
    python_requires='>=3.6',
)
