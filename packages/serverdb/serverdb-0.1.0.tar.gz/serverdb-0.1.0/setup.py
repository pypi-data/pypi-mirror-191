from io import open
from setuptools import setup


version = "0.1.0"
desc = "serverdb"


setup(
    name="serverdb",
    version=version,
    author="ZziriosS",
    description=(u"asd"),
    long_description=desc,
    url="https://github.com/ZziriosS/serverdb",
    download_url=f"https://github.com/ZziriosS/serverdb/archive/v{version}",
    packages=["serverdb"],
    install_requires=["orjson", "requests"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ]
)