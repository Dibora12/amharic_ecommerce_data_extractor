import pandas as pd
import re
import string

def load_raw_telegram_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def clean_amharic_text(text: str) -> str:
    if pd.isnull(text):
        return ""

    text = re.sub(r"[\U00010000-\U0010FFFF]", " ", text)

    text = re.sub(r"(ዋጋ)\s*[:፦\-：]*\s*", r"\1 ", text)

    text = re.sub(r"(?<=\d)(?=\s?(ብር|birr|etb))", " ", text, flags=re.IGNORECASE)

    text = re.sub(r'(?<=[\u1200-\u137F])(?=\d)', ' ', text)
    text = re.sub(r'(?<=\d)(?=[\u1200-\u137F])', ' ', text)
    text = re.sub(r'(?<=[\u1200-\u137F])(?=[a-zA-Z])', ' ', text)
    text = re.sub(r'(?<=[a-zA-Z])(?=[\u1200-\u137F])', ' ', text)


    phone_pattern = r'(\+251[79]\d{8}|0[79]\d{8})'
    text = re.sub(fr'(?<!\s){phone_pattern}(?!\s)', r' \1 ', text)

    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'@\w+', '', text)

    text = re.sub(r'[^a-zA-Z0-9\u1200-\u137F\s፡።፣፤፥፦መሀቀለዐነአሰቀቸበኸተሰከወፈ]+', '', text)
    

    text = re.sub(r'\s+', ' ', text).strip()

    return text

def amharic_tokenize(text: str) -> list:
    return text.split()


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()


    df = df[df["Message"].notnull() & df["Message"].str.strip().ne("")]

    df["cleaned_message"] = df["Message"].apply(clean_amharic_text)

    df["tokens"] = df["cleaned_message"].apply(amharic_tokenize)

    return df[["ID", "Channel Title", "Channel Username", "Date", "cleaned_message", "tokens"]]

def save_cleaned_data(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False)

