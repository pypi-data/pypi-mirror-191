import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="jumonc_llview",
    version="0.2.1rc2",
    install_requires=["JuMonC>=0.10.0rc3", "pluggy"],
    entry_points={
        "jumonc": [
            "llview = jumonc_llview.jumonc_llview_plugin",
        ]
    },
    description="Allow LLVIEW to querry API-paths to be used for the job reporting",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.jsc.fz-juelich.de/coec/jumonc_llview",
    author="Christian Witzler",
    author_email="c.witzler@fz-juelich.de",
    packages=["jumonc_llview"],
    license="BSD 3-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
)
