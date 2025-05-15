import scraper_sentiment

# Test the scrape_headlines function
headlines = scraper_sentiment.scrape_headlines(query="technology", page_size=3)
print("Headlines retrieved:", len(headlines))
for headline in headlines:
    print(f"- {headline}")