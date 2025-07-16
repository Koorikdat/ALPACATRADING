import json
import ssl
import re
from urllib.request import urlopen, Request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()
# Bypass SSL certificate verification (temporary bandaid solution, need to revisit this)
ssl._create_default_https_context = ssl._create_unverified_context



# Find Tickers in text, both cashtags ($AAPL) and bare tickers (AAPL)
def extract_tickers(text):
    cashtags = re.findall(r"\$[A-Z]{1,5}", text)
    bare = re.findall(r"\b[A-Z]{2,5}\b", text)
    all_tickers = set(t.replace("$", "") for t in cashtags + bare)
    blacklist = {"YOLO", "TOS", "USD", "WSB", "DD", "CEO", "IMO", "GPT", 'FOMO', 'KMS', 'FML', 'WTF', 'IRA', 'ROI', 'AI', }  # Common false positives
    return [t for t in all_tickers if t not in blacklist]



# Get sentiment using VADER
def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound > 0.05:
        sentiment = "positive"
    elif compound < -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return sentiment, compound

# Fetch top posts from a subreddit
def get_top_posts(subreddit, limit=15, time_range="day"):
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t={time_range}&limit={limit}"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urlopen(req) as response:
        data = json.loads(response.read())

    posts = []
    for post in data['data']['children']:
        p = post['data']
        title = p['title']
        permalink = p['permalink']
        upvotes = p.get('ups', 0)
        tickers = extract_tickers(title)

        # I want to get the 'important' tickers and put them in a list so that i can count occurrences later and see which are the most mentioned

        sentiment, score = get_sentiment(title)

        posts.append({
            'title': title,
            'url': f"https://www.reddit.com{permalink}",
            'upvotes': upvotes,
            'tickers': tickers,
            'sentiment': sentiment,
            'compound_score': score,
            'subreddit': subreddit
        })
    return posts

subreddits = ["wallstreetbets", "stocks", "investing"]
for sub in subreddits:
    print(f"\nTop posts from r/{sub}:\n{'-'*50}")
    top_posts = get_top_posts(sub)
    for i, post in enumerate(top_posts, start=1):
        print(f"{i}. {post['title']}")
        print(f"   URL: {post['url']}")
        print(f"   Tickers: {post['tickers']}")
        print(f"   Sentiment: {post['sentiment']} (score: {post['compound_score']})")
        print(f"   Upvotes: {post['upvotes']}\n")
