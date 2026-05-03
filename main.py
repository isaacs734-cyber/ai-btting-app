from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = os.getenv("a62dd4ce99msha865405af45e6ffp1ccb6bjsnee9703603f17")

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/debug")
def debug():
    url = "https://free-api-live-football-data.p.rapidapi.com/football-players-search?search=m"

   headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"

    }

    response = requests.get(url, headers=headers)
    return response.json()