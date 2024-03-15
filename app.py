# -*- coding: utf-8 -*-
import requests.exceptions
import functions
import time
from flask import Flask, render_template, request, session, url_for, Response
from flask_session import Session

# Create an instance of Flask
app = Flask(__name__)

# Start Flask-Session
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


# function that renders homepage.html
@app.route('/')
def home():
    return render_template('homepage.html')


# function that renders questionnaire.html
@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    # Only include the following topics in the questionnaire (topic_id obtained from MyHealthFinder API). This helps
    # limit the topic search so that it does not return back too many articles.
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


# Function that renders results.html. If the user selected more than 3 topics or 0 topics, returns an error.
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


# Function that renders a secret url for text to speech audio. if there is a chunked encoding error, retry 5 times.
@app.route('/text-to-speech/<topic_name>')
def text_to_speech(topic_name):
    lang = session['lang']
    content = session[topic_name]
    content = content.replace('<br>', '')
    for retry in range(5):
        try:
            audio = functions.generate_text_to_speech(content, lang)
            break
        except requests.exceptions.ChunkedEncodingError:
            time.sleep(1)
            # print('Failed')
    return Response(audio, mimetype='audio/wav')


if __name__ == '__main__':
    sess = Session()
    sess.init_app(app)
    app.run(debug=True)
