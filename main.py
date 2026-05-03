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
    busquedas = [
        "a", "m", "r", "s", "b", "c",
        "haaland", "mbappe", "cristiano", "messi",
        "vinicius", "salah", "kane", "bellingham"
    ]

    todos = []

    for nombre in busquedas:
        picks = value_picks(nombre)

        for pick in picks:
            if pick["value_score"] >= min_value:
                todos.append(pick)

    # quitar duplicados por jugador
    unicos = {}
    for pick in todos:
        jugador = pick["jugador"]
        if jugador not in unicos or pick["value_score"] > unicos[jugador]["value_score"]:
            unicos[jugador] = pick

    ordenados = sorted(
        unicos.values(),
        key=lambda x: x["value_score"],
        reverse=True
    )

    return ordenados[:limit]