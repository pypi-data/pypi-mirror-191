from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Cronuseo python SDK'
LONG_DESCRIPTION = 'Cronuseo python SDK for permission checking'

# Setting up
setup(
    name="cronuseosdk",
    version=VERSION,
    author="Cronuseo",
    author_email="<cronuseo@gmail.com>",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'auth', 'cronuseo'],
    classifiers=[
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ])