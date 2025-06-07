"""
Terminological Ontological Coverage (TOCo) Package
A package for keyword and ontology comparison.

This package provides tools for:
- Extracting keywords using RAKE, Rake-NLTK, and KeyBERT
- Comparing keyword coverage against ontologies
- Analyzing terminological and ontological relationships

Author: Anna Sofia Lippolis
"""

# Import all the main functions from keyword_comparison
from .keyword_comparison import (
    # Text processing functions
    extract_text_from_pdf,
    
    # Ontology functions
    load_ontology,
    keyword_in_ontology,
    
    # Keyword extraction functions
    generate_keywords_rake,
    generate_keywords_rake_nltk,
    generate_keywords_keybert,
    generate_custom_keywords_scores,
    
    # Analysis functions
    weighted_keywords_in_ontology,
    analyze_keywords_from_text,
    analyze_custom_keywords,
    compare_ontologies_and_methods,
    
    # Main function
    main
)

# Package metadata
__version__ = "1.0.1"
__author__ = "Anna Sofia Lippolis"
__description__ = "A package for keyword and ontology comparison"
__email__ = "your-email@domain.com"  # Update with your actual email

# Define what gets imported with "from terminological_ontological_coverage import *"
__all__ = [
    # Text processing
    'extract_text_from_pdf',
    
    # Ontology functions  
    'load_ontology',
    'keyword_in_ontology',
    
    # Keyword extraction
    'generate_keywords_rake',
    'generate_keywords_rake_nltk', 
    'generate_keywords_keybert',
    'generate_custom_keywords_scores',
    
    # Analysis functions
    'weighted_keywords_in_ontology',
    'analyze_keywords_from_text',
    'analyze_custom_keywords',
    'compare_ontologies_and_methods',
    
    # Main function
    'main'
]

# Create a convenience class that wraps the main functionality
class TOCo:
    """
    Main class for Terminological Ontological Coverage analysis.
    
    This class provides a convenient interface to the package functionality.
    """
    
    def __init__(self):
        """Initialize TOCo analyzer."""
        self.available_methods = {
            'rake': generate_keywords_rake,
            'rake_nltk': generate_keywords_rake_nltk,
            'keybert': generate_keywords_keybert
        }
    
    def extract_keywords(self, text: str, method: str = 'rake') -> list:
        """
        Extract keywords from text using specified method.
        
        Args:
            text (str): Input text
            method (str): Method to use ('rake', 'rake_nltk', 'keybert')
            
        Returns:
            list: List of (score, keyword) tuples
        """
        if method not in self.available_methods:
            raise ValueError(f"Method must be one of: {list(self.available_methods.keys())}")
        
        return self.available_methods[method](text)
    
    def analyze_ontology_coverage(self, text: str, ontology_path: str, method: str = 'rake') -> dict:
        """
        Analyze how well keywords from text are covered by an ontology.
        
        Args:
            text (str): Input text
            ontology_path (str): Path to ontology file
            method (str): Keyword extraction method
            
        Returns:
            dict: Analysis results with weighted percentage and found keywords
        """
        if method not in self.available_methods:
            raise ValueError(f"Method must be one of: {list(self.available_methods.keys())}")
        
        return analyze_keywords_from_text(text, ontology_path, self.available_methods[method])
    
    def compare_multiple_ontologies(self, text: str, ontology_paths: list, 
                                  methods: list = None, custom_keywords: dict = None,
                                  output_csv: str = 'comparison_results.csv',
                                  matches_csv: str = 'match_results.csv'):
        """
        Compare keyword coverage across multiple ontologies and methods.
        
        Args:
            text (str): Input text
            ontology_paths (list): List of ontology file paths
            methods (list): List of methods to use (default: all available)
            custom_keywords (dict): Custom keywords with scores
            output_csv (str): Path for comparison results CSV
            matches_csv (str): Path for match results CSV
            
        Returns:
            DataFrame: Comparison results
        """
        if methods is None:
            methods = [('RAKE', generate_keywords_rake),
                      ('Rake-NLTK', generate_keywords_rake_nltk),
                      ('KeyBERT', generate_keywords_keybert)]
        else:
            methods = [(method, self.available_methods[method]) for method in methods 
                      if method in self.available_methods]
        
        if custom_keywords is None:
            custom_keywords = {}
        
        return compare_ontologies_and_methods(
            text, ontology_paths, methods, custom_keywords, output_csv, matches_csv
        )

# Add the convenience class to __all__
__all__.append('TOCo')

# Print package info when imported
def _print_package_info():
    """Print package information when imported."""
    print(f"TOCo (Terminological Ontological Coverage) v{__version__}")
    print(f"Available functions: {len(__all__)} functions")
    print("Quick start: from terminological_ontological_coverage import TOCo")
    print("             analyzer = TOCo()")

# Uncomment the line below if you want info printed on import
# _print_package_info()
