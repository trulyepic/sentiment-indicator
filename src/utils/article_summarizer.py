import openai
import os
import requests
from bs4 import BeautifulSoup
import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}


def fetch_article_content(url):
    """Fetch and return the full article text using web scraping."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all text from <p> tags (avoiding navigation menus)
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.get_text() for p in paragraphs])

        # If the article is too short, discard it
        if len(article_text) < 200:
            print(f"Warning: Article content for {url} is too short.")
            return ""

        return article_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article content from {url}: {e}")
        return ""


def summarize_article(article_text):
    """Use OpenAI's GPT model to summarize the article."""
    if not article_text:
        print("Warning: No article text to summarize.")
        return "No content available for summarization."

    prompt = f"Summarize the following financial news article in 3 concise sentences, and determine if it has " \
             f"Bullish, Bearish, or Neutral sentiment towards the stock market :\n\n{article_text}"

    try:
        client = openai.OpenAI()  # NEW: Create OpenAI client
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a article summary specialist."},
                      {"role": "user", "content": prompt}],
            # max_tokens=200
        )
        summary = response.choices[0].message.content  # NEW: Updated response structure
        return summary
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "Error generating summary."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error generating summary."

