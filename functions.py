# -*- coding: utf-8 -*-

import urllib.parse, urllib.request, urllib.error, json
from bs4 import BeautifulSoup
from openai import OpenAI
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import keys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

client = OpenAI(api_key=keys.OPENAI_API_KEY)
authenticator = IAMAuthenticator(keys.IBM_API_KEY)
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

topicsearch_baseurl = 'https://health.gov/myhealthfinder/api/v3/topicsearch.json'
itemlist_baseurl = 'https://health.gov/myhealthfinder/api/v3/itemlist.json'
text_to_speech_baseurl = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com'


# performs a topic search using MyHealthFinderAPI using user-specified categories, keywords, and language
def search_for_articles(category, language='en', keywords=None):
    if keywords is None:
        parameters = {'lang': language, 'categoryId': category}
    else:
        parameters = {'lang': language, 'categoryId': category, 'keyword': keywords}
    api_request = topicsearch_baseurl + '?' + urllib.parse.urlencode(parameters)
    api_response = urllib.request.urlopen(api_request)
    articles_data = json.loads(api_response.read())
    return articles_data


# Return a dictonary that pairs category name (in a specified language) with categoryIDs. Splits Mental Health and
# Relationships into two different categories (i.e., depression and anxiety) to simplify topic search.
def get_category_database(language='en'):
    api_request = f'{itemlist_baseurl}?lang={language}&type=category'
    api_response = urllib.request.urlopen(api_request)
    category_list = json.loads(api_response.read())
    category_database = {}
    for item in category_list['Result']['Items']['Item']:
        category_title = item['Title']
        category_id = int(item['Id'])
        if category_title == 'Mental Health and Relationships':
            category_database['Depression'] = category_id
            category_database['Anxiety'] = category_id
        elif category_title == 'Salud mental y relaciones con otras personas':
            category_database['Depresión'] = category_id
            category_database['Ansiedad'] = category_id
        else:
            category_database[category_title] = category_id
    return category_database


# Given the output from a MyHealthFinderAPI topic search, this function will return the summarized content and resource
# links for all articles in the topic search
def extract_content_and_resources(articles_data):
    all_articles = articles_data['Result']['Resources']['Resource']
    store_related_links = {}
    store_all_content = ''

    for article in all_articles:
        content = clean_article_content(article)
        store_all_content += f'{content}\n\n'
        all_related_links = article['RelatedItems']['RelatedItem']
        for related_link in all_related_links:
            store_related_links[related_link['Title']] = related_link['Url']

    print('Checkpoint reached!')
    summarized_content = create_summary(store_all_content)
    summarized_content = summarized_content.replace('\n', '<br>')

    content_and_resources = {
        'content': summarized_content,
        'related-links': store_related_links
    }

    return content_and_resources


# Removes any HTML that is present from MyHealthFinderAPI topic search so the text is easier to read
def clean_article_content(article):
    article_sections = article["Sections"]["section"]
    compiled_content = ''
    for section in article_sections:
        raw_content = section["Content"]
        soup = BeautifulSoup(raw_content, 'html.parser')
        cleaned_content = soup.get_text(separator=' ')
        cleaned_content = ' '.join(cleaned_content.split())
        compiled_content += cleaned_content
    return compiled_content


# Given the content from MyHealthFinderAPI, create a summary.
def create_summary(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": "Remove all repeated information and summarize the following text in 350 words "
                                        "or less with layman terms. If potential questions for doctors are originally"
                                        f"included, add them to the end with a lead-in (not included in limit): {text}"
             }
        ]
    )
    summary = response.choices[0].message.content
    return summary


def generate_text_to_speech(text, lang):
    text_to_speech.set_service_url(text_to_speech_baseurl)
    if lang == 'en':
        response = text_to_speech.synthesize(
            text,
            voice="en-US_OliviaV3Voice",
            accept='audio/wav'
        )
    else:
        response = text_to_speech.synthesize(
            text,
            voice="es-US_SofiaV3Voice",
            accept='audio/wav'
        )
    return response.get_result().content


# Safe version of search_for_articles
def search_for_articles_safe(category, language='en', keywords=None):
    try:
        return search_for_articles(category, language, keywords)
    except urllib.error.HTTPError as e:
        print(f"Error trying to retrieve data: {e}")
    except urllib.error.URLError as e:
        print(f"Failed to reach the server: {e}")
    return None


# Safe version of get_category_database
def get_category_database_safe(language='en'):
    try:
        return get_category_database(language)
    except urllib.error.HTTPError as e:
        print(f"Error trying to retrieve data: {e}")
    except urllib.error.URLError as e:
        print(f"Failed to reach the server: {e}")
    return None


if __name__ == '__main__':
    article = search_for_articles_safe(19, language='en')
    extract_content_and_resources(article)
