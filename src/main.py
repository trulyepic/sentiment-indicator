from news_scraper import fetch_news
from utils.article_summarizer import fetch_article_content, summarize_article
from sentiment_analysis import apply_sentiment_analysis, determine_market_bias


def main():
    print("Fetching financial news...")
    news_data = fetch_news()
    # print(news_data)

    # print("fetching article summarizer:")
    # summery = fetch_article_content("https://www.cnbc.com/2025/03/17/wholesale-egg-prices-have-plunged-retail-prices"
    #                                 "-may-follow.html")
    #
    # print(summery)
    #
    # print("gpt summary")
    # gptsummary = summarize_article(summery)
    #
    # print(gptsummary)
    print("Analyzing sentiment of summarized articles...")
    sentiment_score = apply_sentiment_analysis(news_data)

    market_bias = determine_market_bias(sentiment_score)

    print(f"Overall Market Sentiment: {market_bias} ({sentiment_score:.2f})")


if __name__ == "__main__":
    main()
