import oracledb
import pandas as pd
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def setup_database():
    try:
        connection = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn="localhost:1521/XE"
        )
        cursor = connection.cursor()

        # Create Banks table
        cursor.execute("""
            CREATE TABLE Banks (
                bank_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                bank_name VARCHAR2(100) UNIQUE
            )
        """)

        # Create Reviews table
        cursor.execute("""
            CREATE TABLE Reviews (
                review_id VARCHAR2(100) PRIMARY KEY,
                review_text VARCHAR2(4000),
                rating NUMBER,
                review_date DATE,
                bank_id NUMBER,
                source VARCHAR2(50),
                sentiment_label VARCHAR2(50),
                sentiment_score NUMBER,
                themes VARCHAR2(200),
                FOREIGN KEY (bank_id) REFERENCES Banks(bank_id)
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
        logging.info("Database schema created")
    except Exception as e:
        logging.error(f"Error setting up database: {e}")

def insert_data(df):
    try:
        connection = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn="localhost:1521/XE"
        )
        cursor = connection.cursor()

        # Insert unique banks
        banks = df['bank_name'].unique()
        for bank in banks:
            cursor.execute("INSERT INTO Banks (bank_name) VALUES (:1)", (bank,))

        # Insert reviews
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO Reviews (review_id, review_text, rating, review_date, bank_id, source, sentiment_label, sentiment_score, themes)
                VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), (SELECT bank_id FROM Banks WHERE bank_name = :5), :6, :7, :8, :9)
            """, (
                row['review_id'], row['review_text'], row['rating'], row['date'],
                row['bank_name'], row['source'], row['sentiment_label'], row['sentiment_score'], ','.join(row['themes'])
            ))

        connection.commit()
        cursor.close()
        connection.close()
        logging.info("Data inserted into Oracle database")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")

if __name__ == "__main__":
    setup_database()
    df = pd.read_csv("data/reviews_with_themes.csv")
    insert_data(df)