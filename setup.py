from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'FLOW Calculator'
LONG_DESCRIPTION = 'Calculator and web app for Fanno, Rayleigh, and isentropic flow, shocks'

# Setting up
setup(
    # the name must match the folder name 'FLOW'
    name="FLOW",
    version=VERSION,
    author="Nick Mondora",
    author_email="nmondora@purdue.edu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['CoolProp', 'numpy', 'Pint', 'scipy', 'pandas'],

    keywords=['python', 'fluid flow', 'shocks'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)