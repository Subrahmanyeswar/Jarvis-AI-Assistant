# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\productivity\news.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def get_news(country_code: str = "in"):
    """
    Gets the top 5 news headlines for a specified country.
    Args:
        country_code (str): The 2-letter country code (e.g., "in" for India, "us" for USA).
    """
    print(f"🛠️ TOOL: Running get_news(country_code='{country_code}')...")
    if not API_KEY:
        return "News API key is not configured."
        
    base_url = "https://newsapi.org/v2/top-headlines"
    try:
        params = {
            'country': country_code,
            'apiKey': API_KEY,
            'pageSize': 5
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get("articles", [])
        if not articles:
            return "I couldn't find any top headlines right now."
            
        headlines = "Here are the top headlines:\n"
        for i, article in enumerate(articles, 1):
            headlines += f"{i}. {article['title']}\n"
            
        return headlines
    except requests.exceptions.RequestException as e:
        print(f"❌ News API Error: {e}")
        return "Sorry, I couldn't retrieve the news at this time."