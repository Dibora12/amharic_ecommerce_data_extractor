import sys, pathlib
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR
sys.path.append(str(SRC_DIR))

from src.utils.preprocessing import load_raw_telegram_data, preprocess_dataframe, save_cleaned_data

INPUT_PATH = "./data/raw/telegram_data.csv"
OUTPUT_PATH = "./data/processed/telegram_data_cleaned.csv"

def main():
    df = load_raw_telegram_data(INPUT_PATH)
    cleaned_df = preprocess_dataframe(df)
    save_cleaned_data(cleaned_df, OUTPUT_PATH)
    print(f"[✓] Cleaned data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()