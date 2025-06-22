# Ecommerce Amharic NER Project 🇪🇹🛒

Extracting Product Intelligence from Telegram-based E-Commerce Posts in Amharic

---

## Project Overview

Ecommerce is building an NLP pipeline to extract structured information from unstructured Telegram messages posted by Amharic-speaking e-commerce vendors. The goal is to identify key entities:

- 🛍️ `PRODUCT`  
- 💰 `PRICE`  
- 📍 `LOCATION`  
- 📞 `CONTACT`  

The extracted information will support vendor scorecards, analytics dashboards, and intelligent recommendations.

---

## Quick Start

### Install Dependencies

    pip install -r requirements.txt

### Run Labeling Pipeline
    ```
    python scripts/run_preprocessing.py
        then
    python scripts/run_ner_labeling.py

    ```


    This loads the cleaned Telegram dataset and outputs labeled_data.conll in CoNLL format.

## Methods

* used a scalable, rule-based labeling system:

    PRODUCT - keyword anchors (e.g., juicer, ማሽን, dispenser)

    PRICE - regex for “6800 ብር”, “ዋጋ 5000”

    LOCATION - keyword-based clues like ፎቅ, ሞል, ቦታ

    CONTACT - regex for phone numbers (e.g., 0912345678)

* Labels follow the BIO scheme (B-, I-, O) for multi-token phrases.

## Outputs

    telegram_data_cleaned.csv: Cleaned and tokenized messages

    labeled_data.conll: Weakly labeled training data for NER models

## Next Steps

    Manual validation of labeling

    Fine-tuning a BERT-based Amharic NER model

    Model evaluation and interpretability

    Entity-based analytics & dashboards