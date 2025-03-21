import requests
from bs4 import BeautifulSoup
import datetime
from config import NEWS_SOURCES
import os
from utils.yahoo_finance import fetch_yahoo_finance_rss
import random

# API_URL = "https://financialmodelingprep.com/api/v4/stock-news-sentiments-rss-feed?page=0"
# API_KEY = os.getenv("FMP_API_KEY")
# Define headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}


def clean_link(link, base_url):
    """Ensures only one valid URL is returned, avoiding double 'markets' in Reuters links."""
    if not link:
        return None
    link = link.strip()

    # If the link is already a full URL, return as is
    if link.startswith("http"):
        return link

    # Handle Reuters case to avoid duplicate "markets"
    if "reuters.com" in base_url and link.startswith("/markets/"):
        return "https://www.reuters.com" + link  # Ensure it starts from root

    # Fix USA Today links by removing duplicate `/money`
    if "usatoday.com" in base_url and "/money/" in link:
        base_url = base_url.replace("/money", "")
        link = link.replace("/money/story/money/", "/story/money/")

    return base_url.rstrip("/") + link  # Default case for other sources


def clean_headline(headline):
    """Removes unnecessary text like 'opens new tab'."""
    return headline.replace("opens new tab", "").strip()


# def fetch_news():
#     """Fetch stock news from the Financial Modeling Prep API."""
#     try:
#         response = requests.get(f"{API_URL}&apikey={API_KEY}")
#         response.raise_for_status()
#         news_data = response.json()
#
#         # Extract relevant fields
#         formatted_news = []
#         for article in news_data[:10]:
#             formatted_news.append({
#                 "symbol": article.get("symbol"),
#                 "publishedDate": article.get("publishedDate"),
#                 "headline": article.get("title"),
#                 "snippet": article.get("text"),
#                 "url": article.get("url"),
#                 "sentiment": article.get("sentiment"),
#                 "sentimentScore": article.get("sentimentScore"),
#                 "source": article.get("site"),
#                 "timestamp": datetime.datetime.now()
#             })
#
#         return formatted_news
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching stock news: {e}")
#         return []

def fetch_news():
    """Scrape financial headlines and article links from major sources."""
    # news_data = []
    #
    # for source, url in NEWS_SOURCES.items():
    #     try:
    #         response = requests.get(url, headers=HEADERS)
    #         response.raise_for_status()
    #         soup = BeautifulSoup(response.text, "html.parser")
    #
    #         articles = []  # Initialize articles
    #
    #         if source == "CNBC":
    #             articles = soup.find_all("a", class_="Card-title")
    #
    #         elif source == "Reuters":
    #             # Locate article containers (hero cards)
    #             article_elements = soup.find_all("div", class_="hero-card__container__1x2e7")
    #
    #             # Convert Reuters' format to match CNBC's (list of BeautifulSoup elements)
    #             articles = [article.find("a", {"data-testid": "Title"}) for article in article_elements]
    #             # Remove None values (if any)
    #             articles = [a for a in articles if a and "lseg.com" not in a["href"]]
    #
    #         elif source == "YahooFinance":
    #             yahoo_articles = fetch_yahoo_finance_rss(HEADERS)
    #             news_data.extend(yahoo_articles)  # Append Yahoo articles and skip further processing
    #             continue  # Skip the rest of the loop for YahooFinance
    #
    #         elif source == "APNews":
    #             article_elements = soup.find_all("div", class_="PagePromo")
    #             articles = [article.find("h3", class_="PagePromo-title").find("a") for article in article_elements if
    #                         article.find("h3", class_="PagePromo-title")]
    #             # Locate the news containers in AP News
    #             # article_elements = soup.find_all("div", class_="PagePromo")
    #             #
    #             # for article in article_elements[:5]:  # Limit to 5 headlines
    #             #     title_tag = article.find("h3", class_="PagePromo-title")
    #             #     link_tag = title_tag.find("a") if title_tag else None
    #             #
    #             #     if link_tag and "href" in link_tag.attrs:
    #             #         headline = clean_headline(link_tag.get_text(strip=True))
    #             #         link = clean_link(link_tag["href"], url)  # Ensure full URL
    #             #
    #             #         news_data.append({
    #             #             "source": source,
    #             #             "headline": headline,
    #             #             "link": link,
    #             #             "timestamp": datetime.datetime.now()
    #             #         })
    #
    #         elif source == "USAToday":
    #             top_headline = soup.find("a", class_="gnt_m_he")
    #             articles = [top_headline] if top_headline else []
    #
    #         elif source == "MarketWatch":
    #             article_elements = soup.find_all("h3")
    #             articles = [article.find("a") for article in article_elements if article.find("a")]
    #
    #         for article in articles[:7]:  # Limit to 5 headlines per source
    #             headline = clean_headline(article.get_text(strip=True))
    #             link = clean_link(article.get("href"), url)
    #
    #             # Ensure valid link is added for ALL sources
    #             if link:
    #                 news_data.append({
    #                     "source": source,
    #                     "headline": headline,
    #                     "link": link,
    #                     "timestamp": datetime.datetime.now()
    #                 })
    #
    #     except requests.exceptions.HTTPError as e:
    #         print(f"HTTP error while fetching {source}: {e}")
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error fetching news from {source}: {e}")
    #
    # return news_data

    return [
        {
            "source": "MockSource",
            "headline": "Stocks rally as AI hype grows",
            "link": "https://example.com/article1",
            "timestamp": datetime.datetime.now()
        },
        {
            "source": "MockSource",
            "headline": "Federal Reserve to pause rate hikes",
            "link": "https://example.com/article2",
            "timestamp": datetime.datetime.now()
        }
    ]
