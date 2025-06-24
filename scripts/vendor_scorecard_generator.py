import pandas as pd
from collections import defaultdict
from datetime import datetime
import numpy as np
import re


def extract_price(text):
    """
    Extract numeric price values from text using regex.
    Assumes Ethiopian birr amounts (e.g., '380 ብር', '380 birr', etc.)
    Also excludes common non-price numbers like sizes or phone numbers.
    """
    if not isinstance(text, str):
        return None


    price_pattern = r"\b(\d{2,6})\s*(ብር|birr)\b"
    matches = re.findall(price_pattern, text.replace(",", "")) 

    
    if matches:
        return float(matches[0][0])
    
    return None

def posts_per_week(dates):
    """
    Calculate average number of posts per week.
    """
    if len(dates) < 2:
        return len(dates)
    dates = sorted(pd.to_datetime(dates))
    duration_days = (dates[-1] - dates[0]).days + 1
    weeks = duration_days / 7
    return round(len(dates) / weeks, 2)


def compute_vendor_metrics(df):
    """
    Main function to compute metrics per vendor.
    """
    vendors = []
    for vendor, group in df.groupby('Channel Username'):
        # Posting frequency
        post_freq = posts_per_week(group['Date'])

        # Views
        avg_views = group['Views'].mean()
        top_post_row = group.loc[group['Views'].idxmax()]
        top_post = top_post_row['Message']
        top_views = top_post_row['Views']

        # Price extraction
        group['Extracted Price'] = group['Message'].apply(extract_price)
        avg_price = group['Extracted Price'].dropna().mean()

        # Lending Score (weights can be tuned)
        score = 0.5 * avg_views + 0.5 * post_freq

        vendors.append({
            'Vendor': vendor,
            'Avg Views/Post': round(avg_views, 2),
            'Posts/Week': round(post_freq, 2),
            'Avg Price (ETB)': round(avg_price, 2) if not np.isnan(avg_price) else None,
            'Top Post': top_post[:100] + '...' if len(top_post) > 100 else top_post,
            'Top Post Views': int(top_views),
            'Lending Score': round(score, 2)
        })

    return pd.DataFrame(vendors)


def main():
    input_csv = './data/processed/telegram_data_cleaned_with_views.csv'
    output_csv = './data/outputs/vendor_scorecard.csv'

    print("[✓] Loading data...")
    df = pd.read_csv(input_csv, parse_dates=['Date'])

    if 'Views' not in df.columns:
        raise ValueError("Expected 'Views' column in input CSV.")

    print("[✓] Computing vendor metrics...")
    scorecard_df = compute_vendor_metrics(df)

    print("[✓] Saving output to:", output_csv)
    scorecard_df.to_csv(output_csv, index=False)

    print("\n📊 Vendor Scorecard Summary:")
    print(scorecard_df[['Vendor', 'Avg Views/Post', 'Posts/Week', 'Avg Price (ETB)', 'Lending Score']].sort_values(by='Lending Score', ascending=False))


if __name__ == "__main__":
    main()