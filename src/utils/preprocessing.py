import pandas as pd
import re
import string

def load_raw_telegram_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def clean_amharic_text(text: str) -> str:
    if pd.isnull(text):
        return ""

    text = text.replace("፦", " ")
    text = re.sub(r'(?<!\s)(09\d{8})(?!\s)', r' \1 ', text)
    
    text = re.sub(fr'([\u1200-\u137F])(\d)', r'\1 \2', text)
    text = re.sub(fr'(\d)([\u1200-\u137F])', r'\1 \2', text)
    text = re.sub(r'[^\w\s፡።፣፤፥፦መሀቀለዐነአሰቀቸበኸተሰከወፈ]+', '', text)

    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'@\w+', '', text)

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
