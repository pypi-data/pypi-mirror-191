import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup( 
    name="SacCkPt",
    version="0.0.3",
    author="Dikshita",
    author_email="dikshita.poojari@neosoftmail.com",
    description="A Python package to save and load checkpoint data.",
    long_description="This python package provides a checkpoint class which allow you to save and load the state of your streaming data as a checkpoint.",
    long_description_content_type="text/markdown",    
    packages=['SacCkPt'],
    install_requires=["python-dotenv==0.21.1"]
    )

