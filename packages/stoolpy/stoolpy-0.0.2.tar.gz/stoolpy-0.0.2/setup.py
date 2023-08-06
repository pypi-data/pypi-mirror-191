from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.2'
DESCRIPTION = 'A Scientific Computing Toolbox package'
LONG_DESCRIPTION = 'A package that allows to compute, model and analyse scientific tasks with the use of numerical methods and visualizers.'

# Setting up
setup(
    name="stoolpy",
    version=VERSION,
    author="Qcuincy (Quincy Sproul)",
    author_email="<quincy.sproul@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'scipy'],
    keywords=['python', 'numerical', 'science', 'scientific', 'modelling', 'data', 'visualizer'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)