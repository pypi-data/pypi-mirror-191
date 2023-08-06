import setuptools


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


def get_version():
    with open("supex/__init__.py", "r") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split('"')[1]
        else:
            raise TypeError("NO SUPEX_VERSION")


setuptools.setup(
    name="supex",
    version=get_version(),
    author="skt_ca_team",
    author_email="rbska56455@gmail.com",
    description="skt_ca_team library",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/advanced_analytics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "autogluon.tabular",
        "recbole",
    ],
)
