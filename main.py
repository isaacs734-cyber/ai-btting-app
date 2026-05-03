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

@app.get("/top-picks")
def top_picks(min_value: float = 1.08, limit: int = 10):
    busquedas = ["a", "m", "r", "s", "haaland", "mbappe", "cristiano", "messi", "vinicius", "salah"]

    todos = []

    for nombre in busquedas:
        try:
            picks = value_picks(nombre)
            if isinstance(picks, list):
                for pick in picks:
                    if pick.get("value_score", 0) >= min_value:
                        todos.append(pick)
        except Exception:
            continue

    unicos = {}

    for pick in todos:
        jugador = pick.get("jugador")

        if not jugador:
            continue

        if jugador not in unicos or pick.get("value_score", 0) > unicos[jugador].get("value_score", 0):
            unicos[jugador] = pick

    ordenados = sorted(
        unicos.values(),
        key=lambda x: x.get("value_score", 0),
        reverse=True
    )

    return ordenados[:limit]