from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

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
        probabilidad = 0.62
        cuota_minima = 1.80
        value_score = round(probabilidad * cuota_minima, 2)

        picks.append({
            "jugador": jugador.get("nombre"),
            "equipo": jugador.get("equipo"),
            "mercado": "Anota o asistencia",
            "probabilidad_modelo": probabilidad,
            "cuota_minima": cuota_minima,
            "value_score": value_score,
            "confianza": "MEDIA",
            "stake_recomendado": "1%",
            "nota": "Demo trader inicial. Falta conectar stats reales y cuotas reales."
        })

    return picks