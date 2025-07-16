# I want to start by querying reddit, and look into extracting the top posts from stock market related subreddits.
# The next step will likely be to analyze these, and also look into other data sources like X or news articles.

import json
import ssl
from urllib.request import urlopen, Request

# Bypass SSL certificate verification (for macOS SSL bug)
ssl._create_default_https_context = ssl._create_unverified_context

class sentimentAnalysis: 
    def __init__(self, url): 
        self.url = url
        self.subreddit = None
        self.text = None
        self.upvotes = None
        self.title = None
        self.get_data()

    def get_data(self):
        connect = False
        while not connect:
            try:
                req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req)
                connect = True
            except Exception as e:
                print("Retrying due to error:", e)
        data_json = json.loads(response.read())

        if data_json and 'data' in data_json[0]:
            for child in data_json[0]['data'].get('children', []):
                post_data = child.get('data', {})
                self.upvotes = post_data.get('ups', 0)
                self.subreddit = post_data.get('subreddit', 'Unknown Subreddit')
                self.title = post_data.get('title', 'No Title')
                self.text = post_data.get('selftext', 'No Text')

# Example usage
# url = 'https://www.reddit.com/r/stories/comments/1ahp9d1/meditation_practise_has_made_taking_shits_1000x/.json'
# test_post = sentimentAnalysis(url)

# print("URL:", test_post.url)
# print("Subreddit:", test_post.subreddit)
# print("Title:", test_post.title)
# print("Text:", test_post.text)
# print("Upvotes:", test_post.upvotes)





# Get top 15 posts from r/wallstreetbets today
url = 'https://www.reddit.com/r/wallstreetbets/top.json?t=day&limit=15'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urlopen(req) as response:
    data = json.loads(response.read())

# Extract and print title + full Reddit URL
print("Top 15 Posts on r/wallstreetbets Today:\n")
for i, post in enumerate(data['data']['children'], start=1):
    post_data = post['data']
    title = post_data['title']
    permalink = post_data['permalink']
    full_url = f"https://www.reddit.com{permalink}"
    print(f"{i}. {title}\n   {full_url}\n")
