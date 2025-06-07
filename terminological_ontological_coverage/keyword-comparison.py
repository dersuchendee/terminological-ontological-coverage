import fitz  # PyMuPDF
from rdflib import Graph, RDFS
from rake.rake import RAKE
from rake_nltk import Rake
from keybert import KeyBERT
from typing import List, Tuple, Dict, Union, Callable
import pandas as pd
import argparse


def extract_text_from_pdf(pdf_path: str) -> str:
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text


def load_ontology(filepath: str) -> Graph:
    g = Graph()
    g.parse(filepath, format="ttl")
    return g


def keyword_in_ontology(keyword: str, graph: Graph) -> int:
    keyword = keyword.lower()
    count = 0
    for label in graph.objects(None, RDFS.label):
        if keyword in str(label).lower():
            count += 1
    for comment in graph.objects(None, RDFS.comment):
        if keyword in str(comment).lower():
            count += 1
    return count


def generate_keywords_rake(text: str) -> List[Tuple[float, str]]:
    rake = RAKE()  # Uses default stop words
    text = text.replace("\n", " ")
    keywords_with_scores = rake.exec(text)
    keywords_with_scores = [(score, keyword) for keyword, score in keywords_with_scores
                            if len(keyword.split()) <= 3 and len(keyword) <= 35 and not keyword.isdigit()]
    return keywords_with_scores


def generate_keywords_rake_nltk(text: str) -> List[Tuple[float, str]]:
    r = Rake(min_length=1, max_length=2, include_repeated_phrases=False)
    r.extract_keywords_from_text(text)
    keywords_with_scores = [(score, keyword) for score, keyword in r.get_ranked_phrases_with_scores()
                            if len(keyword) >= 3 and not keyword.isdigit()]
    return keywords_with_scores


def generate_keywords_keybert(text: str) -> List[Tuple[float, str]]:
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words=None, top_n=10)
    return [(score, keyword) for keyword, score in keywords]


def generate_custom_keywords_scores(custom_keywords_scores: Dict[str, float]) -> List[Tuple[float, str]]:
    return [(score, keyword) for keyword, score in custom_keywords_scores.items()]


def weighted_keywords_in_ontology(
    keywords_with_scores: List[Tuple[float, str]], ontology: Graph
) -> Dict[str, Union[int, float, Dict[str, int]]]:
    total_relevance = sum(score for score, keyword in keywords_with_scores)
    weighted_found = 0
    keywords_found = {}

    for score, keyword in keywords_with_scores:
        count = keyword_in_ontology(keyword, ontology)
        if count > 0:
            weighted_found += score
            keywords_found[keyword] = count

    percentage_found = (weighted_found / total_relevance) * 100 if total_relevance > 0 else 0

    return {
        "weighted_percentage": percentage_found,
        "keywords_found": keywords_found,
    }


def analyze_keywords_from_text(
    text: str, ontology_path: str, keyword_func: Callable[[str], List[Tuple[float, str]]]
) -> Dict[str, Union[int, float, Dict[str, int]]]:
    keywords_with_scores = keyword_func(text)
    ontology = load_ontology(ontology_path)
    result = weighted_keywords_in_ontology(keywords_with_scores, ontology)
    return result


def analyze_custom_keywords(
    custom_keywords_scores: Dict[str, float], ontology_path: str
) -> Dict[str, Union[int, float, Dict[str, int]]]:
    keywords_with_scores = generate_custom_keywords_scores(custom_keywords_scores)
    ontology = load_ontology(ontology_path)
    result = weighted_keywords_in_ontology(keywords_with_scores, ontology)
    return result


def compare_ontologies_and_methods(
    text: str,
    ontology_paths: List[str],
    keyword_methods: List[Tuple[str, Callable[[str], List[Tuple[float, str]]]]],
    custom_keywords_scores: Dict[str, float],
    csv_file_path: str,
    match_file_path: str
) -> pd.DataFrame:
    comparison_results = []
    match_results = []

    # Evaluate RAKE, Rake-NLTK, KeyBERT, and custom keywords methods
    for ontology_path in ontology_paths:
        for method_name, keyword_func in keyword_methods:
            result = analyze_keywords_from_text(text, ontology_path, keyword_func)
            comparison_results.append({
                "Ontology": ontology_path,
                "Method": method_name,
                "Weighted Percentage": result["weighted_percentage"]
            })
            for keyword, count in result["keywords_found"].items():
                match_results.append({
                    "Ontology": ontology_path,
                    "Method": method_name,
                    "Keyword": keyword,
                    "Count": count
                })

    # Evaluate custom keywords
    for ontology_path in ontology_paths:
        result = analyze_custom_keywords(custom_keywords_scores, ontology_path)
        comparison_results.append({
            "Ontology": ontology_path,
            "Method": "Custom Keywords",
            "Weighted Percentage": result["weighted_percentage"]
        })
        for keyword, count in result["keywords_found"].items():
            match_results.append({
                "Ontology": ontology_path,
                "Method": "Custom Keywords",
                "Keyword": keyword,
                "Count": count
            })

    df_comparison = pd.DataFrame(comparison_results)
    df_comparison.to_csv(csv_file_path, index=False)

    df_matches = pd.DataFrame(match_results)
    df_matches.to_csv(match_file_path, index=False)

    best_result = df_comparison.loc[df_comparison["Weighted Percentage"].idxmax()]
    print(f"Ontology '{best_result['Ontology']}' achieved the highest score with method '{best_result['Method']}'.")

    return df_comparison


def parse_arguments():
    parser = argparse.ArgumentParser(description="Compare ontologies and keyword extraction methods.")
    parser.add_argument("text_file_path", type=str, help="Path to the input text file.")
    parser.add_argument("ontology_paths", type=str, nargs="+", help="Paths to the ontology files.")
    parser.add_argument("output_comparison_csv", type=str, help="Path to save the comparison results CSV file.")
    parser.add_argument("output_matches_csv", type=str, help="Path to save the match results CSV file.")
    parser.add_argument("--use_rake", action="store_true", help="Use RAKE for keyword extraction.")
    parser.add_argument("--use_rake_nltk", action="store_true", help="Use Rake-NLTK for keyword extraction.")
    parser.add_argument("--use_keybert", action="store_true", help="Use KeyBERT for keyword extraction.")
    parser.add_argument("--custom_keywords_file", type=str, help="Path to the custom keywords CSV file.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    with open(args.text_file_path, "r", encoding="utf-8") as file:
        text = file.read()

    keyword_methods = []
    custom_keywords_scores = {}

    if args.use_rake:
        keyword_methods.append(("RAKE", generate_keywords_rake))
    if args.use_rake_nltk:
        keyword_methods.append(("Rake-NLTK", generate_keywords_rake_nltk))
    if args.use_keybert:
        keyword_methods.append(("KeyBERT", generate_keywords_keybert))
    if args.custom_keywords_file:
        custom_keywords_df = pd.read_csv(args.custom_keywords_file)
        custom_keywords_scores = dict(zip(custom_keywords_df["Keyword"], custom_keywords_df["Score"]))

    compare_ontologies_and_methods(
        text,
        args.ontology_paths,
        keyword_methods,
        custom_keywords_scores,
        args.output_comparison_csv,
        args.output_matches_csv
    )


if __name__ == "__main__":
    main()
