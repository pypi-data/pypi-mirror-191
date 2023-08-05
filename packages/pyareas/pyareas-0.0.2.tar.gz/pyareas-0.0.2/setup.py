from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Python package for Areas'
LONG_DESCRIPTION = 'Python package to help get the areas of 2D shapes'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pyareas", 
        version=VERSION,
        author="TomTheCodingGuy",
        author_email="tomb80940@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['math'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'pyareas'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
