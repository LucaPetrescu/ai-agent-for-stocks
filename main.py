from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

URL = url = "https://api.marketaux.com/v1/news/all"
headers = {
    "Content-Type": "application/json"
}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/news")
def get_news():
    response = requests.get(URL)
    data = response.json()
    return {"data": data}