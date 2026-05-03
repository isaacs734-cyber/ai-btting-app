from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = os.getenv("a62dd4ce99msha865405af45e6ffp1ccb6bjsnee9703603f17") or os.getenv("a62dd4ce99msha865405af45e6ffp1ccb6bjsnee9703603f17")

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/debug")
def debug():
    if not API_KEY:
        return {"error": "API_KEY no está configurada en Railway"}

    url = "https://free-api-live-football-data.p.rapidapi.com/football-players-search?search=m"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return {
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/picks")
def picks():
    return {"message": "Backend funcionando. Usa /debug para probar la API."}