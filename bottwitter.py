import tweepy
from bs4 import BeautifulSoup
import requests

# Set up Twitter API keys and access tokens
CONSUMER_KEY = 'YOUR KEY'
CONSUMER_SECRET = 'YOUR KEY'
ACCESS_TOKEN = 'YOUR KEY'
ACCESS_TOKEN_SECRET = 'YOUR KEY'
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Scrape MSNBC for the top article
msnbc_url = 'https://www.msnbc.com/'
try:
    response = requests.get(msnbc_url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
except requests.exceptions.RequestException as e:
    print(f"Error making the request to MSNBC: {e}")
    # Handle the error (e.g., log it, exit the script)

soup = BeautifulSoup(response.text, 'html.parser')
top_article = soup.find('h2', class_='smorgasbord-meta-content__headline smorgasbord-meta-content__headline--L')  # Adjust the class based on MSNBC's HTML structure

# Compose the tweet
if top_article:
    tweet_text = f"📰 {top_article.text}\nRead more: {msnbc_url}"

    try:
        client.create_tweet(text=tweet_text)
        print("Tweet posted successfully!")
    except tweepy.TweepError as e:
        print(f"Error posting tweet: {e}")
        if hasattr(e, 'api_code') and e.api_code == 187:
            print("Duplicate tweet. Skipping...")
else:
    print("Top article not found.")