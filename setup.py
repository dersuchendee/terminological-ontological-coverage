from setuptools import setup, find_packages
import pathlib

# Load the README file.
current_directory = pathlib.Path(__file__).parent
long_description = (current_directory / "README.md").read_text()

setup(
    name="terminological_ontological_coverage",
    version="1.0.1",
    packages=find_packages(),
    package_data={                                           
        'terminological_ontological_coverage': ['*.txt'],  
    },                                                       
    include_package_data=True,                              
    install_requires=[
        "PyMuPDF",   # This installs the `fitz` package
        "rdflib",
        "rake-nltk",
        "keybert",
        "pandas",
        "argparse",
        "transformers"
    ],
    entry_points={
        'console_scripts': [
            'keyword-comparison=terminological_ontological_coverage.keyword_comparison:main',
        ]
    },
    author="Anna Sofia Lippolis",
    description="A package for keyword and ontology comparison.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="keywords ontology comparison",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
