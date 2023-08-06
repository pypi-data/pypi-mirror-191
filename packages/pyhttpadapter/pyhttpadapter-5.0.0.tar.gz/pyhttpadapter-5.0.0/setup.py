import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhttpadapter",
    version="5.0.0",
    author="supriya",
    author_email="supriya.kadam@neosoftmail.com",
    description="A HTTP Adapter to call any rest or 3rd party api.",
    long_description="Python module to call any 3rd party apis \
    compatible to perform any http request like GET,POST,PUT,PATCH,DELETE.",
    long_description_content_type="text/markdown",
    packages=["pyhttpadapter"],
    install_requires=[
        "attrs==22.2.0",
        "certifi==2022.12.7",
        "charset-normalizer==3.0.1",
        "exceptiongroup==1.1.0",
        "idna==3.4",
        "iniconfig==2.0.0",
        "packaging==23.0",
        "pluggy==1.0.0",
        "PyYAML==6.0",
        "requests==2.28.2",
    ],
)
