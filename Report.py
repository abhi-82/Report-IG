import requests
from datetime import datetime, timedelta

# Instagram API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
access_token = 'your_access_token'

# Function to get Instagram user insights
def get_user_insights(username):
    endpoint = f'https://graph.instagram.com/v12.0/{username}?fields=business_discovery&access_token={access_token}'
    response = requests.get(endpoint)
    data = response.json()
    return data.get('business_discovery', {})

# Function to get Instagram post insights
def get_post_insights(media_id):
    endpoint = f'https://graph.instagram.com/v12.0/{media_id}?fields=insights.metric(impressions,reach,engagement)&access_token={access_token}'
    response = requests.get(endpoint)
    data = response.json()
    return data.get('insights', {})

# Function to generate a report
def generate_report(username, days=7):
    user_data = get_user_insights(username)
    if not user_data:
        return "Error fetching user data."

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    report = f"Instagram Report for {username}\n"
    report += f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n\n"

    for media in user_data.get('media', {}).get('data', []):
        media_id = media.get('id')
        post_insights = get_post_insights(media_id)

        if post_insights:
            impressions = post_insights[0].get('values')[0].get('value')
            reach = post_insights[1].get('values')[0].get('value')
            engagement = post_insights[2].get('values')[0].get('value')

            report += f"Post {media_id}\n"
            report += f"Impressions: {impressions}\n"
            report += f"Reach: {reach}\n"
            report += f"Engagement: {engagement}\n\n"

    return report

# Example usage
username = 'target_username'
report = generate_report(username)
print(report)
