import requests

def get_random_fact():
    r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    return r.json()["text"]

def get_category_fact(category):
    r = requests.get(f"https://uselessfacts.jsph.pl/random.json?language=en&category={category}")
    return r.json()["text"]

def get_daily_fact():
    r = requests.get("https://uselessfacts.jsph.pl/today.json?language=en")
    return r.json()["text"]

print("Random:", get_random_fact())
print("Animal:", get_category_fact("animal"))
print("Daily:", get_daily_fact())
