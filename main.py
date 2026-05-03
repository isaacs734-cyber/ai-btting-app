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
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?date=2026-05-03"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    return response.json()