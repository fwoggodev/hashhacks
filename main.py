import os
import json
import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob


filename = "journal.json"

def add_entry():
    if os.path.exists(filename):
        with open(filename, "r") as file:
            journal = json.load(file)
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_entry = next((entry for entry in journal if entry['date_time'].startswith(today)), None)

        if today_entry:
            print(f"Old text:\n{today_entry['text']}")
            new_text = input("Enter new text to append:")
            today_entry['text'] = today_entry['text'] + "\n" + new_text
        else:
            today_entry = {
                'text': input("Enter text for the day:"),
                'date_time': str(datetime.datetime.now()),
                'emotion': "",
            }
            journal.append(today_entry)
    else:
        journal = [{
            'text': input("Enter text for the day:"),
            'date_time': str(datetime.datetime.now()),
            'emotion': "",
        }]

    nltk_sentiment = SentimentIntensityAnalyzer().polarity_scores(journal[0]['text'])
    nltk_score = nltk_sentiment['compound']

    textblob_score = TextBlob(journal[0]['text']).sentiment.polarity

    if nltk_score > 0 or textblob_score > 0:
        journal[0]['emotion'] = "Positive"
    else:
        journal[0]['emotion'] = "Negative"

    
    with open(filename, "w") as file:
        json.dump(journal, file, indent=4)
    
    print(f"Emotion: {journal[0]['emotion']}")



while True:

    choice = int(input("Enter your choice:"))

    if choice == 1:
        add_entry()
    elif choice == 2:
        break
    else:
        print("Invalid choice.")
