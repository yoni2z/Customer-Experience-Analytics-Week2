from transformers import pipeline
import pandas as pd

def analyze_sentiment(df):
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    reviews = df['review_text'].tolist()
    sentiments = classifier(reviews, truncation=True, max_length=512)
    df['sentiment_label'] = [result['label'] for result in sentiments]
    df['sentiment_score'] = [result['score'] for result in sentiments]
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_reviews.csv")
    df = analyze_sentiment(df)
    df.to_csv("data/reviews_with_sentiment.csv", index=False)
    print("Sentiment analysis completed")