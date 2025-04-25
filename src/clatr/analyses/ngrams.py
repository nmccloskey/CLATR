import pandas as pd
import numpy as np
import os
from collections import Counter
from math import log2
from typing import List, Tuple, Dict

def compute_ngrams(PM, sequence: List[str], row_base: Dict, section: str, prefix: str, gran: str) -> Dict[str, List[Dict]]:
    """
    Computes n-grams and associated statistics for a given sequence.

    Args:
        sequence (List[str]): Input sequence (graphemes, phonemes, etc.).
        row_base (Dict): Metadata row (doc_id, sent_id, etc.).
        section (str): Section type (e.g., 'grapheme', 'phoneme').
        prefix (str): Prefix for output table.
        gran (str): Granularity ('doc' or 'sent').

    Returns:
        Dict[str, List[Dict]]: 
            ngram_data: Each key is table name, values are rows for insertion.
    """
    ngram_data = {}
    summary_rows = []
    current_ngram_id = PM.ngram_id_doc if gran == "doc" else PM.ngram_id_sent

    for n in range(1, PM.ngrams + 1):
        ngram_list = [tuple(sequence[i:i+n]) for i in range(len(sequence)-n+1)]
        if not ngram_list:
            continue  # Skip if no n-grams for this n

        ngram_counts = Counter(ngram_list)
        total_ngrams = sum(ngram_counts.values())
        unique_ngrams = len(ngram_counts)
        
        # Compute entropy
        probs = [count/total_ngrams for count in ngram_counts.values()]
        entropy = -sum(p * log2(p) for p in probs) if total_ngrams > 0 else 0
        
        # Compute coverage_top5
        top5_counts = sum([count for _, count in ngram_counts.most_common(5)])
        coverage_top5 = top5_counts / total_ngrams if total_ngrams > 0 else 0
        
        # Compute diversity (unique / total)
        diversity = unique_ngrams / total_ngrams if total_ngrams > 0 else 0

        # Add to summary
        summary_row_data = row_base.copy()
        summary_row_data.update({
            "n": n,
            "unique_ngrams": unique_ngrams,
            "diversity": diversity,
            "entropy": entropy,
            "coverage_top5": coverage_top5
        })
        summary_rows.append(summary_row_data)

        # Build ngram_data for insertion
        table_name = f"{prefix}_n{n}grams"
        records = []
        for rank, (ngram, count) in enumerate(ngram_counts.most_common(), start=1):
            row_data = row_base.copy()
            row_data.update({
                "ngram_id": current_ngram_id,
                "n": n,
                "ngram": "_".join(ngram),
                "count": count,
                "proportion": count / total_ngrams,
                "rank": rank
            })
            records.append(row_data)
            current_ngram_id += 1
        
        ngram_data[table_name] = records

    # Save summary to Excel (append)
    file_path = os.path.join(PM.om.output_dir, section, gran, f"{prefix}_ngrams_{gran}.xlsx")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    summary_df = pd.DataFrame(summary_rows)
    try:
        # Try appending to existing file
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            summary_df.to_excel(writer, sheet_name="summary", index=False, header=False, startrow=writer.sheets["summary"].max_row)
    except FileNotFoundError:
        # If file doesn't exist, create new
        summary_df.to_excel(file_path, sheet_name="summary", index=False)

    return ngram_data
