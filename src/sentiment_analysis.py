import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
from src.utils.article_summarizer import fetch_article_content, summarize_article
import nltk

# Ensure the VADER lexicon is available
nltk.download("vader_lexicon")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

MARKET_OPEN = datetime.time(9, 30)
MARKET_CLOSE = datetime.time(16, 0)
BREAKING_NEWS_KEYWORDS = ["breaking", "urgent", "just in", "alert"]
DECAY_RATE = 0.0005  # Adjust for slower or faster decay


def apply_sentiment_analysis(news_data):
    """Analyze sentiment of summarized articles and apply weighting based on time decay and news type."""
    sentiment_scores = []

    for news in news_data:
        # Fetch and summarize article content
        article_text = fetch_article_content(news["link"])
        # Skip the article if no content was fetched
        if not article_text.strip():
            print(f"Skipping article from {news['source']} (empty content): {news['link']}")
            continue
        summary = summarize_article(article_text) or news["headline"]

        # Run sentiment analysis on the summary
        sentiment = sia.polarity_scores(summary)
        compound_score = sentiment["compound"]
        weight = 1.0  # Default weight

        # Check if the headline is breaking news
        if any(keyword.lower() in news["headline"].lower() for keyword in BREAKING_NEWS_KEYWORDS):
            weight *= 1.5  # Breaking news gets extra weight

        # Apply weight based on market hours
        now = datetime.datetime.now().time()
        if MARKET_OPEN <= now <= MARKET_CLOSE:
            weight *= 1.5
        else:
            weight *= 1.2

        # Apply time decay (older news loses impact)
        elapsed_time = (datetime.datetime.now() - news["timestamp"]).total_seconds() / 3600  # Convert to hours
        decay_factor = max(0.5, 1 - DECAY_RATE * elapsed_time)  # Ensure weight does’t drop below 50%
        weighted_score = compound_score * weight * decay_factor

        sentiment_scores.append(weighted_score)

    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0


def determine_market_bias(sentiment_score):
    """Convert sentiment score into a market bias reading."""
    if sentiment_score > 0.3:
        return "Bullish"
    elif sentiment_score < -0.3:
        return "Bearish"
    else:
        return "Neutral"
