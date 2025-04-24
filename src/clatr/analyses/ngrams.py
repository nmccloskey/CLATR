from collections import Counter
from typing import List, Dict, Tuple
from itertools import islice
import logging
logger = logging.getLogger("CustomLogger")

def compute_ngrams(sequence: List[str], n: int) -> List[Tuple[str, ...]]:
    """
    Generate n-grams from a given sequence.
    :param sequence: List of elements (words, phonemes, POS tags, etc.)
    :param n: Size of the n-gram
    :return: List of n-grams as tuples
    """
    return [tuple(sequence[i:i + n]) for i in range(len(sequence) - n + 1)]

def ngram_statistics(sequence: List[str], n: int) -> List[Dict]:
    """
    Compute n-grams and associated statistics.
    :param sequence: List of elements (words, phonemes, POS tags, etc.)
    :param n: Size of the n-gram
    :return: List of dictionaries (record format) containing n-gram stats
    """
    ngrams = compute_ngrams(sequence, n)
    ngram_counts = Counter(ngrams)
    total_ngrams = sum(ngram_counts.values())

    # Sort by length
    # 2-gram total counts, etc.
    # Get top X most common
    
    results = {}
    for ngram, count in ngram_counts.items():
        results.update({
            "ngram": " ".join(ngram),  # Convert tuple to space-separated string
            "count": count,
            "frequency": count / total_ngrams,  # Relative frequency
            "probability": count / len(ngrams)  # Empirical probability
        })
    
    return results

# Example Usage
if __name__ == "__main__":
    sequence = ["DT", "NN", "VB", "DT", "NN", "VB", "IN", "DT", "NN"]  # Example POS tags
    n = 2
    ngram_results = ngram_statistics(sequence, n)  # Bigram analysis
    for record in ngram_results:
        print(record)
