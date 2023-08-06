from setuptools import setup, find_packages

VERSION = '1.2.3'
DESCRIPTION = ''
with open('README.md') as readme:
    LONG_DESCRIPTION = readme.read()

# Setting up
setup(
    name='node-core',
    version=VERSION,
    author='Kilthunox',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)



