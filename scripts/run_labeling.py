import os
import pandas as pd
from typing import List
import sys, pathlib
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR
sys.path.append(str(SRC_DIR))

from src.utils.ner_labeling import label_tokens_bio, save_conll_file

def label_dataset_to_conll(input_csv_path: str, output_conll_path: str, token_column: str = "tokens") -> None:
    """
    Reads a CSV file, labels tokens with BIO scheme, and saves the output in CoNLL format.
    Assumes token_column contains list-like strings or lists of tokens.
    """
    df = pd.read_csv(input_csv_path)

    conll_lines: List[str] = []
    for _, row in df.iterrows():
        tokens = row[token_column]
        # Convert string representation of list to actual list
        if isinstance(tokens, str):
            tokens = eval(tokens)
        labeled = label_tokens_bio(tokens)
        for token, tag in labeled:
            conll_lines.append(f"{token} {tag}")
        conll_lines.append("")  # Empty line for sentence separation

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_conll_path), exist_ok=True)
    save_conll_file(conll_lines, output_conll_path)

if __name__ == "__main__":
    input_csv_path = "./data/processed/telegram_data_cleaned.csv"
    output_conll_path = "./data/outputs/labeled_data.conll"

    label_dataset_to_conll(input_csv_path, output_conll_path)
    print(f"[✓] CoNLL labeling complete. Output saved to: {output_conll_path}")