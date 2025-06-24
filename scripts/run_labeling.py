import os
import pandas as pd
import ast
from typing import List
import sys, pathlib
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR
sys.path.append(str(SRC_DIR))

from src.utils.ner_labeling import dataframe_to_conll, save_conll_file

def label_dataset_to_conll(input_csv_path: str, output_conll_path: str, token_column: str = "tokens") -> None:
    df = pd.read_csv(input_csv_path)
    first_5_channels = df['Channel Username'].drop_duplicates().head(5)
    df_filtered = df[df['Channel Username'].isin(first_5_channels)]
    conll_lines = dataframe_to_conll(df_filtered, token_column)
    save_conll_file(conll_lines, output_conll_path)
    print(f"[✓] CoNLL labeling complete. Output saved to: {output_conll_path}")


if __name__ == "__main__":
    input_csv_path = "./data/processed/telegram_data_cleaned.csv"
    output_conll_path = "./data/outputs/labeled_data.conll"
    label_dataset_to_conll(input_csv_path, output_conll_path)