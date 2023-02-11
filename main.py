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

def show_choices():
    print("\n1. Add journal entry")
    print("2. View sentiment analysis in a calendar form")
    print("3. View Menu")
    print("4. Exit")

show_choices()
while True:

    choice = int(input("Enter your choice:"))

    if choice == 1:
        add_entry()
    elif choice == 2:
        view_sentiment_calendar()
    elif choice == 3:
        show_choices()
    elif choice == 4:
        break
    else:
        print("Invalid choice.")