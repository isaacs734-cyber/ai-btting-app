from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/envcheck")
def envcheck():
    api_key = (os.getenv("API_KEY") or os.getenv("RAPIDAPI_KEY") or "").strip()

    return {
        "api_key_detectada": bool(api_key),
        "variables_api": [k for k in os.environ.keys() if "API" in k or "KEY" in k]
    }

@app.get("/debug")
def debug():
    api_key = (os.getenv("API_KEY") or os.getenv("RAPIDAPI_KEY") or "").strip()

    if not api_key:
        return {"error": "API_KEY no está configurada en Railway"}

    url = "https://free-api-live-football-data.p.rapidapi.com/football-players-search?search=m"

    headers = {
        "X-RapidAPI-Key": api_key,
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
@app.get("/players")
def players(search: str = "m"):
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
    api_key = (os.getenv("API_KEY") or os.getenv("RAPIDAPI_KEY") or "").strip()

    url = f"https://free-api-live-football-data.p.rapidapi.com/football-players-search?search={search}"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()

    suggestions = data.get("response", {}).get("suggestions", [])

    picks = []

    for item in suggestions[:10]:
        probabilidad = 0.62
        cuota_minima = 1.80
        value_score = round(probabilidad * cuota_minima, 2)

        if value_score >= 1.15:
            confianza = "ALTA"
            stake = "2%"
        elif value_score >= 1.05:
            confianza = "MEDIA"
            stake = "1%"
        else:
            confianza = "BAJA"
            stake = "NO BET"

        picks.append({
            "jugador": item.get("name"),
            "equipo": item.get("teamName"),
            "mercado": "Anota o asistencia",
            "probabilidad_modelo": probabilidad,
            "cuota_minima": cuota_minima,
            "value_score": value_score,
            "confianza": confianza,
            "stake_recomendado": stake,
            "nota": "Demo trader inicial. Falta conectar stats reales y cuotas reales."
        })

    return picks