from google_play_scraper import Sort, reviews
import csv
from datetime import datetime
import logging
import os

# Setup logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_reviews(app_id, bank_name, count=400):
    logging.info(f"🔄 Fetching reviews for {bank_name}...")
    try:
        results, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count,
            filter_score_with=None
        )
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/{bank_name.replace(" ", "_")}_reviews_{timestamp}.csv'
        os.makedirs('data', exist_ok=True)
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['review_id', 'review_text', 'rating', 'date', 'bank_name', 'source'])
            writer.writeheader()
            for entry in results:
                writer.writerow({
                    'review_id': entry['reviewId'],
                    'review_text': entry['content'],
                    'rating': entry['score'],
                    'date': entry['at'].strftime('%Y-%m-%d'),
                    'bank_name': bank_name,
                    'source': 'Google Play'
                })
        logging.info(f"✅ Saved {len(results)} reviews to {filename}")
        return filename
    except Exception as e:
        logging.error(f"Error scraping {bank_name}: {e}")
        return None

if __name__ == "__main__":
    banks = [
        ("com.combanketh.mobilebanking", "Commercial Bank of Ethiopia"),
        ("com.boa.boaMobileBanking", "Bank of Abyssinia"),
        ("com.dashen.dashensuperapp", "Dashen Bank")
    ]
    for app_id, bank_name in banks:
        scrape_reviews(app_id, bank_name, count=500)  # Aim for 500 to ensure 400+ after cleaning