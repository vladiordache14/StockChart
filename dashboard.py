import streamlit as st
from signal_engine import generate_signal
from scraper_sentiment import analyze_market_sentiment
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Trading Signal", layout="centered")

st.title("📈 AI-Powered Trading Signal")

st.markdown("This app uses **news sentiment** and **market trends** to suggest a trading action.")

# --- Input field ---
query = st.text_input("Enter a company or market keyword:", value="Apple")

# --- Generate button ---
if st.button("🔍 Generate Signal"):
    signal = generate_signal()

    st.subheader("📢 Trading Signal")
    if signal.lower() in ["buy", "hold"]:
        st.success(f"Signal: {signal.upper()}")
    elif signal.lower() == "unknown":
        st.warning("Signal: UNKNOWN")
    else:
        st.info(f"Signal: {signal}")

    # Display sentiment separately
    sentiments, headlines, dates = analyze_market_sentiment(query)
    if sentiments:
        st.subheader("📰 News Sentiment")
        for sent, head in zip(sentiments, headlines):
            st.write(f"- [{sent.upper()}] {head}")
        # 📊 Sentiment Chart
        sentiment_map = {"NEGATIVE": -1, "NEUTRAL": 0, "POSITIVE": 1}
        scores = [sentiment_map.get(s.upper(), 0) for s in sentiments]

        # Build DataFrame
        df_sent = pd.DataFrame({
            "Datetime": pd.to_datetime(dates),
            "Sentiment Score": scores,
            "Headline": headlines
        })

        # Group by date and average
        df_sent["Date"] = df_sent["Datetime"].dt.date
        df_daily = df_sent.groupby("Date")["Sentiment Score"].mean().reset_index()

        # Plot
        fig = px.line(df_daily, x="Date", y="Sentiment Score", markers=True,
                      title="Average Market Sentiment Over Time")
        fig.update_yaxes(tickmode='array', tickvals=[-1, 0, 1],
                         title="Sentiment Score (-1=Neg, 0=Neutral, 1=Pos)")
        st.plotly_chart(fig)
    else:
        st.warning("No market sentiment data available.")
else:
    st.info("Click the button above to generate a trading signal.")
