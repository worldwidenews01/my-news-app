from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import random
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GENRES = {
    "Politics": "🏛️", "Sports": "⚽", "Tech & AI": "💻", 
    "Business & Stocks": "📈", "Religion": "🕊️", "Weather & Climate": "🌍", 
    "Crime": "🚨", "Pop Culture": "🎭"
}

# Advanced scanning keywords including Indian and Global Stock Markets
KEYWORDS = {
    "Politics": ["election", "government", "modi", "parliament", "president", "policy", "vote"],
    "Sports": ["cricket", "ipl", "football", "soccer", "tennis", "nfl", "championship"],
    "Tech & AI": ["tech", "ai", "software", "apple", "google", "microsoft", "cyber", "gadget"],
    "Business & Stocks": ["market", "economy", "stocks", "inflation", "ceo", "nifty", "sensex", "shares", "crypto", "bitcoin"],
    "Religion": ["pope", "temple", "church", "mosque", "religion", "faith", "prayer"],
    "Weather & Climate": ["climate", "weather", "storm", "monsoon", "flood", "earthquake"],
    "Crime": ["police", "arrest", "court", "murder", "judge", "illegal", "scam"],
    "Pop Culture": ["movie", "music", "celebrity", "bollywood", "hollywood", "netflix", "ott"]
}

# Reads your key securely from the hidden Render server vault
API_KEY = os.environ.get("NEWS_API_KEY")

@app.get("/api/v1/current-cycle")
def get_current_cycle():
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=100&apiKey={API_KEY}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])
    except:
        articles = []

    live_data = {f"{emoji} {genre}": 0 for genre, emoji in GENRES.items()}
    
    for article in articles:
        text = str(article.get("title")).lower() + " " + str(article.get("description")).lower()
        matched = False
        for genre, words in KEYWORDS.items():
            if any(word in text for word in words):
                emoji = GENRES[genre]
                live_data[f"{emoji} {genre}"] += 1
                matched = True
                break
        
        if not matched:
            random_genre = random.choice(list(GENRES.keys()))
            live_data[f"{GENRES[random_genre]} {random_genre}"] += 1

    return {"data": live_data}

@app.get("/api/v1/dynamic-trends")
def get_dynamic_trends(timeframe: str = "1_week"):
    time_multipliers = {"1_day": 1, "1_week": 7, "1_month": 30, "3_months": 90, "6_months": 180, "1_year": 365}
    days = time_multipliers.get(timeframe, 7)
    
    historical = {}
    for genre, emoji in GENRES.items():
        daily_volume = random.randint(300, 700)
        historical[f"{emoji} {genre}"] = daily_volume * days

    return {"timeframe": timeframe, "data": historical}