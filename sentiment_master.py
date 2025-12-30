import pandas as pd
from textblob import TextBlob
import os

# --- FILE PATHS ---
# Ensure these paths are exact. If you move files, update them here.
FILE_PV_MAIN = r"C:\Users\nasse\OneDrive\OneUnime Files\My 4-Year Career Plan\Project\OPTI-TOURISM-2025\Day 16\Data\PV.xlsx"
FILE_PV_MAPS = r"C:\Users\nasse\OneDrive\OneUnime Files\My 4-Year Career Plan\Project\OPTI-TOURISM-2025\Day 16\Data\PV GOOGLE MAPS.xlsx"
FILE_SA = r"C:\Users\nasse\OneDrive\OneUnime Files\My 4-Year Career Plan\Project\OPTI-TOURISM-2025\Day 16\Data\Sant'Angelo, Matera - Small Luxury Hotels rating.xlsx"
FILE_PG = r"C:\Users\nasse\OneDrive\OneUnime Files\My 4-Year Career Plan\Project\OPTI-TOURISM-2025\Day 16\Data\Palazzo Gattini Luxury Hotel.csv"
FILE_AQ = r"C:\Users\nasse\OneDrive\OneUnime Files\My 4-Year Career Plan\Project\OPTI-TOURISM-2025\Day 16\Data\Aquatio Cave Luxury  Reviews ACL  Hotel.xlsx"

OUTPUT_FILE = r"C:\OPTI-TOURISM-2025\04_ANALYSIS\sentiment_master_db.csv"


def get_sentiment(text):
    """Returns Sentiment Score (-1 to 1) and Label"""
    if pd.isna(text) or str(text).strip() == "": return 0, "Neutral"
    score = TextBlob(str(text)).sentiment.polarity
    if score > 0.15:
        return score, "Positive"
    elif score < -0.05:
        return score, "Negative"
    else:
        return score, "Neutral"


def load_file(file_path):
    """Smart loader that handles both CSV and Excel"""
    if file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        return pd.read_csv(file_path)


def main():
    print("--- 🚀 STARTING SENTIMENT ENGINE (FULL MARKET) ---")
    all_data = []

    # 1. PALAZZO VICECONTE (Booking/TripAdvisor)
    try:
        df = load_file(FILE_PV_MAIN)
        # Rename based on your file structure
        df = df.rename(columns={'review_text': 'Review', 'rating': 'Rating', 'platform': 'Source'})
        df['Hotel Name'] = 'Palazzo Viceconte'
        df['Date'] = None
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        all_data.append(df[['Hotel Name', 'Source', 'Rating', 'Review', 'Date']])
        print(f"✅ Loaded {len(df)} PV (Booking/TA) reviews")
    except Exception as e:
        print(f"❌ Error PV Main: {e}")

    # 2. PALAZZO VICECONTE (Google Maps)
    try:
        df = load_file(FILE_PV_MAPS)
        df = df.rename(columns={'review_text': 'Review', 'review_rating': 'Rating', 'review_datetime_utc': 'Date'})
        df['Source'] = 'Google Maps'
        df['Hotel Name'] = 'Palazzo Viceconte'
        # Normalize Rating: Google is 1-5, we want 1-10
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce') * 2
        all_data.append(df[['Hotel Name', 'Source', 'Rating', 'Review', 'Date']])
        print(f"✅ Loaded {len(df)} PV (Google Maps) reviews")
    except Exception as e:
        print(f"❌ Error PV Maps: {e}")

    # 3. SANT'ANGELO
    try:
        df = load_file(FILE_SA)
        df['Review'] = df['likedText'].fillna('') + " | " + df['dislikedText'].fillna('')
        df = df.rename(columns={'rating': 'Rating', 'Channel': 'Source'})
        df['Hotel Name'] = "Sant'Angelo"
        df['Date'] = None
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        all_data.append(df[['Hotel Name', 'Source', 'Rating', 'Review', 'Date']])
        print(f"✅ Loaded {len(df)} Sant'Angelo reviews")
    except Exception as e:
        print(f"❌ Error Sant'Angelo: {e}")

    # 4. PALAZZO GATTINI (CSV)
    try:
        df = load_file(FILE_PG)
        df = df.rename(columns={'full_text': 'Review', 'rating_10': 'Rating', 'platform': 'Source'})
        df['Hotel Name'] = 'Palazzo Gattini'
        df['Date'] = None
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        all_data.append(df[['Hotel Name', 'Source', 'Rating', 'Review', 'Date']])
        print(f"✅ Loaded {len(df)} Gattini reviews")
    except Exception as e:
        print(f"❌ Error Gattini: {e}")

    # 5. AQUATIO CAVE
    try:
        df = load_file(FILE_AQ)
        df = df.rename(
            columns={'full_text': 'Review', 'rating_5': 'Rating', 'platform': 'Source', 'review_date': 'Date'})
        df['Hotel Name'] = 'Aquatio Cave'
        # Normalize Rating: 1-5 to 1-10
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce') * 2
        all_data.append(df[['Hotel Name', 'Source', 'Rating', 'Review', 'Date']])
        print(f"✅ Loaded {len(df)} Aquatio reviews")
    except Exception as e:
        print(f"❌ Error Aquatio: {e}")

    # --- PROCESS & EXPORT ---
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        print(f"\n🧠 Analyzing Sentiment for {len(final_df)} total reviews...")

        final_df[['Sentiment_Score', 'Sentiment_Label']] = final_df['Review'].apply(
            lambda x: pd.Series(get_sentiment(x))
        )

        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        final_df.to_csv(OUTPUT_FILE, index=False)
        print(f"🎉 DONE! Database saved to: {OUTPUT_FILE}")
        print(final_df.groupby(['Hotel Name', 'Sentiment_Label']).size().unstack(fill_value=0))
    else:
        print("No data found.")


if __name__ == "__main__":
    main()