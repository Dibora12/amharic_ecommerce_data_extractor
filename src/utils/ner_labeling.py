import re
import ast
from typing import List, Tuple
import pandas as pd
import os

price_pattern = re.compile(
    r"""
    (?P<price>
        (?:(?:ዋጋ[:：]?\s*)?)
        (\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)
        \s*(?:ብር|birr|ETB)?
    )
    |
    (?P<price2>
        (?:ብር|birr|ETB)\s*
        (\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

contact_pattern = re.compile(
    r'(?:\+251|0)(?:7\d{8}|9\d{8})'
)

location_keywords = ['ቦታ', 'አድራሻ', 'ሞል', 'ቢሮ', 'ህንፃ', 'ሱቅ', 
                     'ፎቅ', 'ፊት', 'ለቡ', 'መዳህኒዓለም', 'መገናኛ', 'ቦሌ']

location_pattern = re.compile(
    r"\b(" + "|".join(location_keywords) + r")(\s+\S+){0,2}", re.IGNORECASE
)

product_keywords = [
    # Amharic
    "ጁስ", "የጁስ", "ማሽን", "የፀጉር", "የማፅዳት", "ብርጭቆ", "መታጠቢያ", "ቢላዋ", "መኪና", "ሳህን", "ኮዳ",
    "ሳጥን", "የቤት እቃ", "የልብስ", "መዳፊያ", "ሱቅ", "መጠጫ", "የልጅ", "ሳሙና", "ኮምፒውተር",
    "ቴሌቪዥን", "ቡና ማቀዝቀዣ", "ቆሻሻ ባስኬት", "ሞባይል", "ጫማ", "ምጣድ", "ምድጃ",

    # English & Mixed
    "juicer", "set", "shoes", "dispenser", "portable", "furniture", "grooming",
    "ergonomic", "multi", "3in1", "knife", "washing", "mop", "slicer", "gloves",
    "humidifier", "phone", "smartphone", "pan", "machine", "tv", "microwave",
    "refrigerator", "sofa", "mattress", "speaker", "powerbank", "blender",
    "hairdryer", "cooker"
]
product_keywords = [kw.lower() for kw in product_keywords]

product_pattern = re.compile(
    r"\b(" + "|".join(map(re.escape, product_keywords)) + r")(s|es)?\b",
    re.IGNORECASE
)

# Entity definitions
ENTITY_PATTERNS = {
    "CONTACT": contact_pattern,
    "PRICE": price_pattern,
    "LOCATION": location_pattern,
    "PRODUCT": product_pattern
}
ENTITY_PRIORITY = {
    "CONTACT": 1,
    "PRICE": 2,
    "LOCATION": 3,
    "PRODUCT": 4
}

def find_entities(text: str) -> List[Tuple[int, int, str]]:
    spans = []

    for label, pattern in ENTITY_PATTERNS.items():
        for match in pattern.finditer(text):
            spans.append((match.start(), match.end(), label))


    spans = sorted(spans, key=lambda x: (x[0], ENTITY_PRIORITY[x[2]]))

    final = []
    last_end = -1
    for start, end, label in spans:
        if start >= last_end:
            final.append((start, end, label))
            last_end = end
    return final


def tokenize_and_align_labels(text: str, tokens: List[str], entities: List[Tuple[int, int, str]]) -> List[Tuple[str, str]]:
    labels = ["O"] * len(tokens)
    token_spans = []
    current_char = 0
    text_lower = text.lower()

    for token in tokens:
        clean_token = token.strip("።፣፡.,;:!?")
        token_start = text_lower.find(clean_token.lower(), current_char)
        if token_start == -1:
            token_start = current_char
        token_end = token_start + len(clean_token)
        token_spans.append((token_start, token_end))
        current_char = token_end

    for ent_start, ent_end, ent_label in entities:
        for i, (tok_start, tok_end) in enumerate(token_spans):
            if tok_end <= ent_start:
                continue
            if tok_start >= ent_end:
                break
            prefix = "B-" if tok_start == ent_start else "I-"
            labels[i] = prefix + ent_label

    return list(zip(tokens, labels))


def process_row(text: str, tokens: List[str]) -> List[Tuple[str, str]]:
    entities = find_entities(text)
    return tokenize_and_align_labels(text, tokens, entities)


def dataframe_to_conll(df: pd.DataFrame, token_column: str = "tokens", text_column: str = "cleaned_message") -> List[str]:
    conll_lines = []
    for _, row in df.iterrows():
        try:
            tokens = row[token_column]
            if isinstance(tokens, str):
                tokens = ast.literal_eval(tokens)
            text = row[text_column]

            if not isinstance(tokens, list) or not isinstance(text, str):
                continue

            labeled = process_row(text, tokens)
            for token, tag in labeled:
                conll_lines.append(f"{token} {tag}")
            conll_lines.append("")  # Sentence separator
        except Exception as e:
            print(f"[!] Skipped row due to error: {e}")
    return conll_lines


def save_conll_file(conll_lines: List[str], output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for line in conll_lines:
            f.write(line + "\n")