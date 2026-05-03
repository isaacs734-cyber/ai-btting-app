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

    resultados = []

    for item in data.get("response", {}).get("suggestions", [])[:10]:
        resultados.append({
            "nombre": item.get("name"),
            "equipo": item.get("teamName"),
            "tipo": item.get("type")
        })

    return resultados

@app.get("/value-picks")
def value_picks(search: str = "mbappe"):
    jugadores = players(search)

    picks = []

    for jugador in jugadores:
        probabilidad = round(random.uniform(0.48, 0.76), 2)
cuota_real = round(random.uniform(1.55, 2.45), 2)
value_score = round(probabilidad * cuota_real, 2)

if value_score >= 1.18:
    confianza = "ALTA"
    stake = "2%"
elif value_score >= 1.08:
    confianza = "MEDIA"
    stake = "1%"
else:
    confianza = "BAJA"
    stake = "NO BET"

    if value_score < 1.08:
    continue
            picks.append({
    "jugador": jugador["nombre"],
    "equipo": jugador["equipo"],
    "mercado": "Anota o asistencia",

    "probabilidad_modelo": probabilidad,
    "cuota_real": cuota_real,
    "value_score": value_score,

    "confianza": confianza,
    "stake_recomendado": stake,

    "nota": "Modelo dinámico inicial"
})
        })

    return picks