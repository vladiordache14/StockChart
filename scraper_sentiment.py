import requests
import datetime
from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

API_KEY = "3a25fab85d634aa9a9f64f7f15570f90"  # ← replace with your key
NEWS_API_URL = "https://newsapi.org/v2/everything"


def scrape_headlines(query="stock market", language="en", page_size=10):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    params = {
        "q": query,
        "sortBy": "popularity",
        "apiKey": API_KEY,
    }

    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)

        articles = response.json().get("articles", [])
        if not articles:
            print("⚠️ No articles found for the query:", query)
            return []

        headlines = [(article["title"], article["publishedAt"]) for article in articles if
                     article.get("title") and article.get("publishedAt")]
        return headlines

    except requests.exceptions.RequestException as e:
        print("⚠️ NewsAPI request failed:", str(e))
        return []

def get_sentiment(text_list):
    if isinstance(text_list, tuple):
        text_list = list(text_list)
    elif not isinstance(text_list, list):
        text_list = [text_list]
    results = sentiment_pipeline(text_list)
    labels = [r["label"].lower() for r in results]
    return ["positive" if "pos" in l else "negative" if "neg" in l else "neutral" for l in labels]

def analyze_market_sentiment(keyWord):
    headlines = scrape_headlines(query=keyWord)

    if not headlines:
        print("⚠️ No headlines were scraped.")
        return [], []

    texts, dates = zip(*headlines)
    sentiments = get_sentiment(texts)

    print("\nNews & Sentiment:")
    for h, s in zip(headlines, sentiments):
        print(f"[{s.upper()}] {h}")
    return sentiments, texts, dates
