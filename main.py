from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/picks")
def picks():
    return [
        {"match": "Demo vs Demo", "prob": 0.7, "cuota": 1.8}
    ]