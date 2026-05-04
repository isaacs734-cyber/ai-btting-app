from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/players")
def players(search: str = "mbappe"):
    api_key = (os.getenv("API_KEY") or os.getenv("RAPIDAPI_KEY") or "").strip()

    url = f"https://free-api-live-football-data.p.rapidapi.com/football-players-search?search={search}"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()

    print (data)

    resultados = []

    for item in data.get("response", {}).get("suggestions", [])[:10]:
        resultados.append({
            "nombre": item.get("name"),
            "equipo": item.get("teamName"),
            "tipo": item.get("type")
        })

    return resultados

@app.get("/top-picks")
def top_picks(min_value: float = 1.08, limit: int = 10):
    busquedas = ["mbappe", "cristiano", "messi", "haaland", "vinicius", "salah", "kane", "bellingham"]

    todos = []

    for nombre in busquedas:
        jugadores = players(nombre)

        for jugador in jugadores:
            probabilidad = round(random.uniform(0.48, 0.76), 2)
            cuota_real = round(random.uniform(1.55, 2.45), 2)
            value_score = round(probabilidad * cuota_real, 2)

            if value_score < min_value:
                continue

            if value_score >= 1.18:
                confianza = "ALTA"
                stake = "2%"
            elif value_score >= 1.08:
                confianza = "MEDIA"
                stake = "1%"
            else:
                confianza = "BAJA"
                stake = "NO BET"

            todos.append({
                "jugador": jugador["nombre"],
                "equipo": jugador["equipo"],
                "mercado": "Anota o asistencia",
                "probabilidad_modelo": probabilidad,
                "cuota_real": cuota_real,
                "value_score": value_score,
                "confianza": confianza,
                "stake_recomendado": stake,
                "nota": "Top pick automático"
            })

    todos = sorted(todos, key=lambda x: x["value_score"], reverse=True)

    return todos[:limit]

@app.get("/real-picks")
def real_picks():
    url = "https://odds-feed.p.rapidapi.com/markets"

    querystring = {
        "placing": "PREMATCH",
        "market_name": "1X2",
        "page": "0"
    }

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "odds-feed.p.rapidapi.com"
    }

    res = requests.get(url, headers=headers, params=querystring)
    data = res.json()

    picks = []

    # 🔥 IMPORTANTE: estructura puede variar, esto lo ajustamos después
    for event in data.get("events", []):
        for market in event.get("markets", []):
            for outcome in market.get("outcomes", []):

                cuota = float(outcome.get("odds", 0))

                if cuota <= 1:
                    continue

                # modelo fake por ahora
                probabilidad = round(1 / cuota * 1.1, 2)
                value = round(probabilidad * cuota, 2)

                if value < 1.08:
                    continue

                if value >= 1.18:
                    confianza = "ALTA"
                    stake = "2%"
                else:
                    confianza = "MEDIA"
                    stake = "1%"

                picks.append({
                    "partido": event.get("name"),
                    "seleccion": outcome.get("name"),
                    "cuota_real": cuota,
                    "probabilidad_modelo": probabilidad,
                    "value_score": value,
                    "confianza": confianza,
                    "stake_recomendado": stake
                })

    return picks