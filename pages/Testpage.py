import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

st.title("📈 Historical Stock Chart")

# --- User selects ticker and time range ---
ticker = st.text_input("Enter a stock symbol", value="AAPL")
years = st.slider("How many years back?", 1, 10, 3)

# --- Calculate date range ---
end_date = date.today()
start_date = end_date.replace(year=end_date.year - years)

# --- Download data ---
data = yf.download(ticker, start=start_date, end=end_date, interval="1d")

# --- Plot if data exists ---
if not data.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close Price", line=dict(color='blue')))
    fig.update_layout(title=f"{ticker.upper()} - Last {years} Years",
                      xaxis_title="Date", yaxis_title="Price (USD)",
                      template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No data found for this ticker.")
