import os
import json
import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

api = Api(app)


filename = "./website/journal.json"


def add_entry(text,name):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            journal = json.load(file)
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_entry = next((entry for entry in journal if entry['date_time'].startswith(today)), None)

        if today_entry:
            new_text = text
            today_entry['text'] = today_entry['text'] + "\n" + new_text
        else:
            today_entry = {
                'text': text,
                'date_time': str(datetime.datetime.now()),
                'emotion': "",
                'Name': name
            }
            journal.append(today_entry)
    else:
        journal = [{
            'text': text,
            'date_time': str(datetime.datetime.now()),
            'emotion': "",
            'Name': name
        }]

    nltk_sentiment = SentimentIntensityAnalyzer().polarity_scores(journal[0]['text'])
    nltk_score = nltk_sentiment['compound']

    textblob_score = TextBlob(journal[0]['text']).sentiment.polarity

    print(f"NLTK Score: {nltk_score}")
    
    journal[0]['emotion'] = "Negative"

    if nltk_score > 0 or textblob_score > 0:
        journal[0]['emotion'] = "Positive"
        

    with open(filename, "w") as file:
        json.dump(journal, file, indent=4)

    return journal[0]['emotion']

def view_sentiment_calendar():
    if os.path.exists(filename):
        with open(filename, "r") as file:
            journal = json.load(file)
        
        emotions = []
        for entry in journal:
            emotions.append(entry['emotion'])
        
        date_list = [datetime.datetime.strptime(entry['date_time'], "%Y-%m-%d %H:%M:%S.%f").date() for entry in journal]
        unique_dates = list(set(date_list))
        unique_dates.sort()
        
        calendar_data = {}
        for date in unique_dates:
            calendar_data[date.strftime("%B %d, %Y")] = [emotions[i] for i in range(len(date_list)) if date_list[i] == date]
        
        for date, emotion_list in calendar_data.items():
            date_obj = datetime.datetime.strptime(date, "%B %d, %Y")
            date_of_week = date_obj.strftime("%a")
            positive_count = emotion_list.count("Positive")
            negative_count = emotion_list.count("Negative")
            total = positive_count + negative_count
            print(f"{date} ({date_of_week}): {emotions[0]}")

        print("\n")

    else:
        print("No journal entries found.")
@app.before_request
def options_autoreply():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
        h = resp.headers
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Methods'] = "DELETE, GET, POST, PUT"
        h['Access-Control-Allow-Headers'] = headers
        return resp

@app.after_request
def set_allow_origin(resp):
    h = resp.headers
    h['Access-Control-Allow-Origin'] = '*'
    return resp

class Journal(Resource):
    def post(self):
        text = request.get_json()["text"]
        name = request.get_json()["name"]
        if text:
            emotion = add_entry(text,name)
            response = jsonify({"message": "Success", "emotion": emotion})

            return response
        else:
            return {"error": "Text field is missing."}, 400
        
class journalist(Resource):
    def get(self):
        data = "./website/journal.json"
        with open(data, "r") as file:
            journal = json.load(file)
        return journal


api.add_resource(Journal, '/journal')
api.add_resource(journalist, '/journalist')

if __name__ == '__main__':
    app.run(debug=True,port=9999)
