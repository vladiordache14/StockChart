from scraper_sentiment import analyze_market_sentiment
import yfinance as yf
import pandas as pd

def get_market_trend(ticker="^GSPC", days=5):
    data = yf.download(ticker, period=f"{days}d", auto_adjust=True, progress=False)

    if data.empty or "Close" not in data.columns:
        print("⚠️ Failed to load market data.")
        return "unknown"

    closes = data["Close"]
    first_close = closes.iloc[0]
    last_close = closes.iloc[-1]

    change = (last_close - first_close) / first_close

    if hasattr(change, 'item'):  # If it's a numpy/pandas type that has item()
        change = change.item()

    if change < -0.01:
        return "down"
    elif change > 0.01:
        return "up"
    else:
        return "flat"



def generate_signal():
    market_trend = get_market_trend()
    print(f"\nMarket Trend: {market_trend.upper()}")

    sentiment = analyze_market_sentiment("Apple")

    # If no sentiment data, fallback to hold
    if not sentiment:
        return "HOLD"

    # Count sentiment labels
    positive = sum(1 for s in sentiment if s == "positive")
    negative = sum(1 for s in sentiment if s == "negative")

    # Decision logic based on market + sentiment
    if market_trend == "down" and positive > negative:
        return "STRONG BUY"
    elif market_trend == "up" and negative > positive:
        return "WAIT"
    else:
        return "HOLD"
