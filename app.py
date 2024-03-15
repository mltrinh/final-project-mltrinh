# -*- coding: utf-8 -*-
import requests.exceptions

import functions
import time
from flask import Flask, render_template, request, url_for, session, Response
from secrets import token_hex

# Create an instance of Flask
app = Flask(__name__)
app.secret_key = token_hex(16)


# Create a view function for /
@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    included_topics_id = [16, 18, 19, 29, 20, 91, 92, 93, 94, 95, 96, 54, 29, 106, 314, 24, 26, 110]
    included_topics = {}
    if request.method == 'POST':
        lang = request.form["lang"]
        session['lang'] = lang
        category_database = functions.get_category_database_safe(lang)
        for category in category_database:
            if category_database[category] in included_topics_id:
                included_topics[category] = category_database[category]
        return render_template('questionnaire.html', lang=lang, topics=included_topics)
    elif request.method == 'GET':
        return 'Wrong HTTP method', 400


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        lang = session['lang']
        special_topics = [16, 18, 20]
        user_interested_articles = {}
        if len(request.form) > 3 or len(request.form) == 0:
            return render_template('results.html', user_articles={}, error=True)
        else:
            for topic_name, topic_id in request.form.items():
                if int(topic_id) in special_topics:
                    related_articles = functions.search_for_articles_safe(topic_id, lang, topic_name)
                    content_and_resources = functions.extract_content_and_resources(related_articles)
                else:
                    related_articles = functions.search_for_articles_safe(topic_id, lang)
                    content_and_resources = functions.extract_content_and_resources(related_articles)
                user_interested_articles[topic_name] = content_and_resources
                session[topic_name] = content_and_resources['content']
            return render_template('results.html', user_articles=user_interested_articles, error=False)
    elif request.method == 'GET':
        return 'Wrong HTTP method', 400


@app.route('/text-to-speech/<topic_name>')
def text_to_speech(topic_name):
    lang = session['lang']
    content = session[topic_name]
    content = content.replace('<br>', '')
    for retry in range(3):
        try:
            audio = functions.generate_text_to_speech(content, lang)
            break
        except requests.exceptions.ChunkedEncodingError:
            time.sleep(1)
    return Response(audio, mimetype='audio/wav')


if __name__ == '__main__':
    app.run(debug=True)
