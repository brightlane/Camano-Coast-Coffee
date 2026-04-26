import tweepy
import requests
from datetime import date

# --- Twitter API Setup ---
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# Twitter Authentication
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
twitter_api = tweepy.API(auth)

# --- Facebook API Setup ---
facebook_page_access_token = 'your_facebook_page_access_token'
facebook_page_id = 'your_facebook_page_id'

# --- LinkedIn API Setup ---
linkedin_access_token = 'your_linkedin_access_token'
linkedin_person_urn = 'urn:li:person:your_person_urn'  # Replace with your LinkedIn Person URN

# --- Function to Generate Daily Content ---
def generate_daily_content():
    today = date.today()
    content = f"Today's featured coffee: Camano Island Coffee! Brewed fresh, organic, and shipped directly to your door. Learn more: https://www.camanislandcoffee.com/blog/{today.strftime('%Y-%m-%d')}"
    return content

# --- Function to Post to Twitter ---
def post_to_twitter(content):
    try:
        twitter_api.update_status(content)
        print(f"Posted to Twitter: {content}")
    except tweepy.TweepError as e:
        print(f"Error posting to Twitter: {e}")

# --- Function to Post to Facebook ---
def post_to_facebook(content):
    url = f'https://graph.facebook.com/{facebook_page_id}/feed'
    payload = {
        'message': content,
        'access_token': facebook_page_access_token
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Posted to Facebook: {content}")
    else:
        print(f"Error posting to Facebook: {response.json()}")

# --- Function to Post to LinkedIn ---
def post_to_linkedin(content):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {linkedin_access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }
    post_data = {
        "author": linkedin_person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "ARTICLE",
                "media": []
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 201:
        print(f"Posted to LinkedIn: {content}")
    else:
        print(f"Error posting to LinkedIn: {response.json()}")

# --- Main Function to Execute Daily Posting ---
def post_daily():
    content = generate_daily_content()
    post_to_twitter(content)
    post_to_facebook(content)
    post_to_linkedin(content)

# --- Run the Post Daily Function ---
if __name__ == "__main__":
    post_daily()
