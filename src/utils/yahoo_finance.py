import requests
from bs4 import BeautifulSoup
import datetime


def fetch_yahoo_finance_rss(headers):
    """Fetch Yahoo Finance news using RSS instead of web scraping."""
    rss_url = "https://finance.yahoo.com/rss/topstories"

    try:
        response = requests.get(rss_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "xml")  # Parse as XML (RSS feeds use XML)

        articles = []
        for item in soup.find_all("item")[:7]:  # Get top 5 headlines
            title = item.find("title").get_text(strip=True)
            link = item.find("link").get_text(strip=True)

            articles.append({
                "source": "YahooFinance",
                "headline": title,
                "link": link,
                "timestamp": datetime.datetime.now()
            })

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Yahoo Finance RSS: {e}")
        return []
