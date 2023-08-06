from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Python package for areas'
LONG_DESCRIPTION = '''Python package to find the areas of 2D shapes
Shapes Included:
Square, Rectangle, Circle, Rhombus, Triangle, Parellelogram, Ellipse, Trapezoid'''

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
        install_requires=[], # add any additional packages that 
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
