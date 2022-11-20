import pandas as pd
import os
import requests

# Random variables we need
token = os.environ.get("TWITTER_BEARER_TOKEN")
username = 'realDonaldTrump'
today = pd.Timestamp("today").strftime("%Y-%m-%d-%H")
headers = {
    'Authorization': f"Bearer {token}",
}

# Read the archive
archive_df = pd.read_csv(f'data/processed/{username}_followers_archive.csv')

# Get the latest follower count using the Twitter API
response = requests.get(f'https://api.twitter.com/2/users/by/username/{username}?user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&expansions=pinned_tweet_id', headers=headers)

# Snag the follower info from the user object and place in dataframe
latest_df = pd.DataFrame(response.json()['data']['public_metrics'], index=[0])

# Add today's date
latest_df['date'] = today

# Append latest to archive
df = pd.concat([archive_df, latest_df]).reset_index(drop=True).drop_duplicates(subset='date')

# Export
df.to_csv(f'data/processed/{username}_followers.csv', index=False)
df.to_csv(f'data/processed/{username}_followers_archive.csv', index=False)
latest_df.to_csv(f'data/processed/timeseries/{username}_followers_{today}.csv', index=False)
