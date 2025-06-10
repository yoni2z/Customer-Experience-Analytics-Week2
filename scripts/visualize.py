import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def create_visualizations(df):
    # Plot 1: Sentiment Distribution by Bank
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='bank_name', hue='sentiment_label')
    plt.title("Sentiment Distribution by Bank")
    plt.savefig("reports/sentiment_distribution.png")
    plt.close()

    # Plot 2: Rating Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='rating', hue='bank_name', multiple='stack')
    plt.title("Rating Distribution by Bank")
    plt.savefig("reports/rating_distribution.png")
    plt.close()

    # Plot 3: Word Cloud for Keywords
    for bank in df['bank_name'].unique():
        bank_reviews = df[df['bank_name'] == bank]
        keywords = ' '.join([kw for keywords in bank_reviews['keywords'] for kw in keywords])
        wordcloud = WordCloud(width=800, height=400).generate(keywords)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Keyword Cloud for {bank}")
        plt.savefig(f"reports/wordcloud_{bank.replace(' ', '_')}.png")
        plt.close()

    # Plot 4: Sentiment Trend over Time
    plt.figure(figsize=(10, 6))
    for bank in df['bank_name'].unique():
        bank_df = df[df['bank_name'] == bank].sort_values('date')
        plt.plot(bank_df['date'], bank_df['sentiment_score'], label=bank, marker='o')
    plt.title("Sentiment Trend over Time by Bank")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("reports/sentiment_trend.png")
    plt.close()

    # Plot 5: Theme Frequency Comparison
    theme_counts = df.explode('themes').groupby(['bank_name', 'themes']).size().unstack(fill_value=0)
    theme_counts = theme_counts.loc[:, ~theme_counts.columns.str.contains('Other')]  # Exclude "Other" theme
    theme_counts.plot(kind='bar', figsize=(10, 6), width=0.8)
    plt.title("Theme Frequency Comparison by Bank")
    plt.xlabel("Bank Name")
    plt.ylabel("Frequency")
    plt.legend(title="Themes")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("reports/theme_frequency.png")
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv("data/reviews_with_themes.csv")
    create_visualizations(df)