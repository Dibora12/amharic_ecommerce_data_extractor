# Amharic E-commerce NER & Vendor Scorecard 🇪🇹

Extracting Structured Product Intelligence from Telegram E-commerce Channels  
**Named Entity Recognition (NER) + Vendor Analytics + Micro-Lending Scorecard**

---

## Project Overview

This project builds an NLP pipeline to extract and analyze e-commerce information from **Amharic-language Telegram posts**. The system performs:

 📌 **Named Entity Recognition (NER)** to identify key entities:
  - 🛍️ `PRODUCT` – items being sold
  - 💰 `PRICE` – numerical price values (e.g., "6500 ብር")
  - 📍 `LOCATION` – delivery/meeting/store areas
  - 📞 `CONTACT` – phone numbers

- **FinTech Vendor Scorecard** to assess vendor activity, engagement, and pricing and identify top-performing microbusinesses eligible for **micro-lending** based on engagement and product insights.


## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
````

### 2. Run the Preprocessing & Labeling Pipeline

```bash
python scripts/run_preprocessing.py
python scripts/run_ner_labeling.py
```

These scripts clean and tokenize Telegram messages and output weakly labeled data in **CoNLL format** (`labeled_data.conll`).


## Pipeline Components

### Data Preprocessing

* Scraped Telegram posts using Telethon
* Cleaned noise, removed emojis, normalized text

### Rule-based Weak Labeling

Custom heuristics for each entity:

| Entity   | Strategy                                  |
| -------- | ----------------------------------------- |
| PRODUCT  | Keyword anchor matching (e.g., ማሽን, ጫማ)   |
| PRICE    | Regex on digits + ብር / ዋጋ                 |
| LOCATION | Clue phrases (e.g., ቦታ, አድራሻ ሞል)           |
| CONTACT  | Regex (e.g., 09xx,07xx,251 numbers) |

* BIO format applied to support model training (`B-`, `I-`, `O`)

### NER Model Training

* Used 🤗 HuggingFace transformers
* Fine-tuned multilingual models:

  * `rasyosef/bert-tiny-amharic`
  * `Davlan/distilbert-base-multilingual-cased-ner-hrl`
  * `mbeukman/xlm-roberta-base-finetuned-ner-swahili`
* Trained on `labeled_data.conll`

### Model Comparison

| Model Name                                          | Type                              | Weighted F1 | `PRODUCT` F1 | Notes                      |
| --------------------------------------------------- | --------------------------------- | ----------- | ------------ | -------------------------- |
| `rasyosef/bert-tiny-amharic`                        | Tiny BERT (Amharic)               | **0.95**    | 0.64         | Fast, efficient            |
| `Davlan/distilbert-base-multilingual-cased-ner-hrl` | DistilBERT (multilingual)         | **0.95**    | 0.74         | Strong PRODUCT performance |
| `mbeukman/xlm-roberta-base-finetuned-ner-swahili`   | XLM-RoBERTa (multilingual, large) | **0.95**    | **0.78**     | Best PRODUCT recall        |

[✓] **Selected**: `rasyosef/bert-tiny-amharic` – lightweight & excellent CONTACT/LOCATION accuracy

### Model Interpretability

* Used attention visualization + SHAP/LIME to explain decisions
* Identified model weaknesses (e.g., ambiguous PRODUCTs)



## FinTech Vendor Scorecard

Combined **NER outputs + Telegram metadata** to generate vendor-level microbusiness profiles.

### Key Metrics:

| Metric              | Description                                     |
| ------------------- | ----------------------------------------------- |
| **Posts/Week**      | Consistency of business activity                |
| **Avg Views/Post**  | Audience engagement & potential market size     |
| **Avg Price (ETB)** | Product pricing profile                         |
| **Top Post**        | Highest view count + associated product & price |
| **Lending Score**   | Custom score: `0.5 * Views + 0.5 * Posts/Week`  |

### Scorecard Summary:

| Vendor         | Avg Views | Posts/Week | Avg Price (ETB) | Lending Score |
| -------------- | --------- | ---------- | --------------- | ------------- |
| `@ethio_brand_collection`   | 36,957    | 7.89       | 2,274           | **18,482.86** |
| `@ZemenExpress`   | 13,114    | 23.34      | 1,812           | 6,568.82      |
| `@Shageronlinestore` | 13,028    | 27.67      | 2,102           | 6,528.15      |
| `@nevacomputer`  | 5,359     | 7.49       | 34,055          | 2,683.56      |
| `@meneshayeofficial`  | 2,748     | 6.35       | 4,813           | 1,377.37      |



## Outputs

* `data/raw/telegram_data.csv` – raw scraped Telegram posts
* `data/processed/telegram_data_cleaned.csv` – cleaned messages
* `data/outputs/labeled_data.conll` – weakly labeled NER dataset
* `models/` – fine-tuned models (Google Drive)
* `reports/final_report.pdf` – full PDF report with visuals
* `notebooks/vendor_scorecard_visuals.ipynb` – summary dashboard notebook



## Next Steps

* Deploy inference API or Streamlit app
* Use feedback from lenders to refine score logic
* Explore expansion to other local languages & platforms (e.g., Facebook)


## Acknowledgments

* Amharic NLP community for open-source models (rasyosef, Davlan, mbeukman)
* Telethon & HuggingFace for enabling Telegram + NER pipelines


