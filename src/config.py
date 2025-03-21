import os
from dotenv import load_dotenv

# load environment variables from .env files
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

NEWS_SOURCES = {
    "MarketWatch": "https://www.marketwatch.com",
    "USAToday": "https://www.usatoday.com/money/",
    "APNews": "https://apnews.com/hub/financial-markets",
    "YahooFinance": "https://finance.yahoo.com",
    "CNBC": "https://www.cnbc.com/finance/",
    "Reuters": "https://www.reuters.com/markets/",

}
