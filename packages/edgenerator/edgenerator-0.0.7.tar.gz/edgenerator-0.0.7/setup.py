from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Package for generating energy diagrams from excel files'
LONG_DESCRIPTION = 'This package is used to generate energy diagrams from excel files. The main function to be used is [MAIN FUNCTION NAME] ' \
                   'and the arguments are the directory for the energy diagram file and the path to the excel file'

# Setting up
setup(
    name="edgenerator",
    version=VERSION,
    author="SiebeLeDe ",
    author_email="<siebe.lekannegezegddeprez@student.uva.nl>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy>=1.2', 'matplotlib>=3.6', 'openpyxl>=3.0'],
    keywords=['python', 'energy diagram', 'energy diagram generator'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
#        "Operating System :: Unix",
#       "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)