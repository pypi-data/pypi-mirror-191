"""DoHome API setup script"""
import setuptools

with open(".version", "r", encoding="utf-8") as fh:
    VERSION = ''.join(fh.read().split())

with open("README.md", "r", encoding="utf-8") as fh:
    README = fh.read()

setuptools.setup(
    name="dohome_api",
    version=VERSION,
    author="Mikhael Khrustik",
    description="Library for controlling smart bulbs that are controlled by the DoIT protocol",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=[
        'dohome_api',
        'dohome_api.light',
        'dohome_api.transport',
        'dohome_api.gateway',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        'aiodatagram==0.0.1',
        'arrrgs==0.0.4'
    ],
    scripts=[
        'scripts/dohome_rgb'
    ],
    python_requires='>=3.7',
    package_dir={'':'.'},
)
