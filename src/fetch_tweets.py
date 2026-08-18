import tweepy
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Authenticate with Twitter v2 API
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)

def fetch_tweets(query, count=10):
    """Fetch tweets using Twitter API v2."""
    try:
        # Use the Recent Search endpoint (v2)
        tweets = client.search_recent_tweets(
            query=query,
            max_results=count,
            tweet_fields=["created_at", "text", "author_id"],
            user_fields=["username"],
            expansions=["author_id"]
        )

        # Extract tweet data
        tweet_list = []
        for tweet, user in zip(tweets.data, tweets.includes["users"]):
            tweet_list.append([
                user.username,  # User's screen name
                tweet.created_at,  # Tweet creation time
                tweet.text  # Tweet text
            ])

        # Create a DataFrame
        df = pd.DataFrame(tweet_list, columns=["User", "Date", "Tweet"])
        return df

    except tweepy.Forbidden as e:
        print(f"Error: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error

# Fetch tweets about Bitcoin
tweets_df = fetch_tweets("Bitcoin", count=100)

# Save to CSV
if not tweets_df.empty:
    tweets_df.to_csv("tweets_bitcoin.csv", index=False)
    print("Tweets saved to tweets_bitcoin.csv")
else:
    print("No tweets fetched. Check your API access level.")