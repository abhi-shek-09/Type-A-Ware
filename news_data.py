import requests
import json
import codecs
# from app import TypeSpeedGUI
def remove_unicode_escapes(text):
    if text is not None:
        text = codecs.escape_decode(text.encode('utf-8'))[0].decode('utf-8')
    return text

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

api_key = config['api_key']
country = "us"
category = "business"
url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": country,
    "category": category,
    "apiKey": api_key
}

response = requests.get(url, params=params)
if response.status_code == 200:
    content = response.json()
    articles = content['articles']
    descriptions = []
    index = 0
    for article in articles:
        descriptions.append(article['description'])
        index += 1
    
    cleaned_descriptions = [description for description in descriptions if description is not None and description != "null"]
    cleaned_descriptions = [description for description in cleaned_descriptions if "<a href" not in description]
    cleaned_descriptions = [remove_unicode_escapes(description) for description in cleaned_descriptions]

    final_descriptions = "|".join(cleaned_descriptions)
    with open('news_data.txt', 'w') as file:
        file.write(final_descriptions)

    # TypeSpeedGUI()

else:
    print(f"Error: {response.status_code}")
    print(response.text)

