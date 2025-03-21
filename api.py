from flask import Flask, jsonify
from flask_cors import CORS
from news_scraper import fetch_news
from sentiment_analysis import apply_sentiment_analysis, determine_market_bias
from utils.article_summarizer import fetch_article_content, summarize_article

app = Flask(__name__)
# CORS(app, origins=[
#     "http://localhost:5173",
#     "https://sentiment-indicator-production.up.railway.app"
# ])
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route("/market-sentiment", methods=["GET"])
def market_sentiment():
    """Endpoint to return the overall market sentiment score."""
    try:
        news_data = fetch_news()
        if not news_data:
            raise ValueError("No news data returned")

        sentiment_score = apply_sentiment_analysis(news_data)
        market_bias = determine_market_bias(sentiment_score)

        return jsonify({
            "market_sentiment_score": sentiment_score,
            "market_bias": market_bias
        })

    except Exception as e:
        print(f"[ERROR] /market-sentiment failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/headlines", methods=["GET"])
def headlines():
    """Endpoint to return financial news headlines and their links."""
    news_data = fetch_news()
    headlines_data = [{"source": news["source"],
                       "headline": news["headline"],
                       "link": news["link"]} for news in news_data]

    return jsonify(headlines_data)


@app.route("/summaries", methods=["GET"])
def summaries():
    """Endpoint to return article summaries."""
    try:
        news_data = fetch_news()
        summarized_data = []

        for news in news_data:
            article_text = fetch_article_content(news["link"])
            if not article_text.strip():
                continue

            summary = summarize_article(article_text) or "No summary available."

            summarized_data.append({
                "source": news["source"],
                "headline": news["headline"],
                "summary": summary,
                "link": news["link"]
            })

        return jsonify(summarized_data)
    except Exception as e:
        print(f"[ERROR] /summaries failed: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
