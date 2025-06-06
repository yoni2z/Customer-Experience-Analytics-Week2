import pandas as pd
import glob
import os

def preprocess_reviews():
    # Combine all CSVs
    all_files = glob.glob("data/*.csv")
    df_list = []
    for file in all_files:
        df = pd.read_csv(file)
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)

    # Remove duplicates based on review_id
    combined_df = combined_df.drop_duplicates(subset=['review_id'])

    # Handle missing data
    combined_df['review_text'] = combined_df['review_text'].fillna("")
    combined_df = combined_df.dropna(subset=['rating', 'date'])

    # Normalize dates
    combined_df['date'] = pd.to_datetime(combined_df['date']).dt.strftime('%Y-%m-%d')

    # Save cleaned data
    output_file = "data/cleaned_reviews.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"Saved {len(combined_df)} reviews to {output_file}")
    return combined_df

if __name__ == "__main__":
    preprocess_reviews()