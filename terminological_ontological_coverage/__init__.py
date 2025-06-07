"""
Terminological Ontological Coverage (TOCo)
A package for keyword and ontology comparison.

Author: Anna Sofia Lippolis
"""

__version__ = "1.0.1"
__author__ = "Anna Sofia Lippolis"

# Import the main functions that users might want to use directly
try:
    from .keyword_comparison import (
        extract_text_from_pdf,
        load_ontology,
        generate_keywords_rake,
        generate_keywords_rake_nltk,
        generate_keywords_keybert,
        compare_ontologies_and_methods,
        main
    )
except ImportError:
    # If there are import issues, at least provide the metadata
    pass

__all__ = [
    'extract_text_from_pdf',
    'load_ontology', 
    'generate_keywords_rake',
    'generate_keywords_rake_nltk',
    'generate_keywords_keybert',
    'compare_ontologies_and_methods',
    'main'
]
