import pytest
import pandas as pd
import sys, pathlib
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR
sys.path.append(str(SRC_DIR))

from src.utils.preprocessing import clean_amharic_text, amharic_tokenize, preprocess_dataframe

# Sample data
raw_data = {
    "ID": [1],
    "Channel Title": ["Test Channel"],
    "Channel Username": ["@testchannel"],
    "Date": ["2025-06-22"],
    "Message": ["ዋጋ፦800ብር✅ አድራሻ ቁ.1 0912345678 https://t.me/example"]
}


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(raw_data)


def test_clean_amharic_text():
    text = "ዋጋ፦800ብር✅ አድራሻ0912345678 https://t.me/example"
    cleaned = clean_amharic_text(text)
    assert "800 ብር" in cleaned
    assert "0912345678" in cleaned
    assert "https://" not in cleaned
    assert "፦" not in cleaned
    assert "✅" not in cleaned


def test_amharic_tokenize():
    text = "ዋጋ 800 ብር"
    tokens = amharic_tokenize(text)
    assert isinstance(tokens, list)
    assert "800" in tokens
    assert tokens == ["ዋጋ", "800", "ብር"]


def test_preprocess_dataframe(sample_dataframe):
    processed = preprocess_dataframe(sample_dataframe)
    assert "cleaned_message" in processed.columns
    assert "tokens" in processed.columns
    assert len(processed) == 1
    assert isinstance(processed["tokens"].iloc[0], list)
    assert "800" in processed["cleaned_message"].iloc[0]
    assert "https://" not in processed["cleaned_message"].iloc[0]