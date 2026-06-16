from textblob import TextBlob
import time
import random

print("Mood-Based Music Recommender")
time.sleep(1)
print("Describe your feelings and I will suggest music for you.")
time.sleep(1)

positive_list = [
    "Happy Vibes Playlist",
    "Sunny Day Mix",
    "Feel Good Hits",
    "Upbeat Pop Essentials",
    "Good Mood Energy Tracks",
    "Bright Morning Tunes",
    "Positive Pop Boost"
]

negative_list = [
    "Chill & Calm Playlist",
    "Soft Piano Mix",
    "Relaxing Lo-Fi",
    "Deep Focus Ambient",
    "Slow & Peaceful Instrumentals",
    "Emotional Soft Beats",
    "Night Rain Lo-Fi"
]

neutral_list = [
    "Focus Beats",
    "Ambient Study Mix",
    "Smooth Background Tracks",
    "Calm Electronic Flow",
    "Soft Chillhop Collection",
    "Neutral Mood Mix",
    "Balanced Ambient Playlist"
]

text = input("How are you feeling today? ")

sentiment = TextBlob(text).sentiment.polarity

if sentiment > 0.2:
    category = "positive"
elif sentiment < -0.2:
    category = "negative"
else:
    category = "neutral"

print("\nAnalyzing your mood...")
time.sleep(2)

print("\nRecommended playlists:")

if category == "positive":
    for p in random.sample(positive_list, 5):
        print("-", p)
elif category == "negative":
    for p in random.sample(negative_list, 5):
        print("-", p)
else:
    for p in random.sample(neutral_list, 5):
        print("-", p)

print("\nEnjoy your music experience")
