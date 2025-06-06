import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def extract_themes(df):
    nlp = spacy.load("en_core_web_sm")
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1,2))
    tfidf_matrix = vectorizer.fit_transform(df['review_text'])
    feature_names = vectorizer.get_feature_names_out()

    # Extract keywords per review
    def get_top_keywords(text):
        doc = nlp(text.lower())
        tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]
        return tokens[:5]  # Top 5 tokens

    df['keywords'] = df['review_text'].apply(get_top_keywords)

    # Manual clustering into themes
    themes = {
        'Account Access Issues': ['login', 'error', 'access', 'password'],
        'Transaction Performance': ['slow', 'transfer', 'loading', 'delay'],
        'User Interface': ['ui', 'interface', 'design', 'navigation'],
        'Customer Support': ['support', 'response', 'help', 'service'],
        'Feature Requests': ['feature', 'fingerprint', 'budgeting', 'transfer']
    }

    def assign_themes(keywords):
        assigned = []
        for theme, theme_keywords in themes.items():
            if any(kw in keywords for kw in theme_keywords):
                assigned.append(theme)
        return assigned if assigned else ['Other']

    df['themes'] = df['keywords'].apply(assign_themes)
    df.to_csv("data/reviews_with_themes.csv", index=False)
    print("Thematic analysis completed")
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/reviews_with_sentiment.csv")
    df = extract_themes(df)