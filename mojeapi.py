import os
import json
from glob import glob
from typing import Union
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()
DATA_FOLDER = "data"

def get_latest_file():
    files = glob(os.path.join(DATA_FOLDER, "synop_data_*.json"))
    if not files:
        raise FileNotFoundError("No data files found.")
    
    latest_file=max(files, key=lambda x: datetime.strptime(
        os.path.basename(x).replace("synop_data_", "").replace(".json", ""), "%Y%m%d_%H%M%S"))
    return latest_file

def load_weather_data():
    try:
        latest_file = get_latest_file()
        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON data.")

@app.get("/")
def get_root():
    return {"Hello": "World"}

@app.get("/weather/")
def get_weather():
    try:
        data = load_weather_data()
        result = [record for record in data]
        if not result:
            raise HTTPException(status_code=404, detail="Station not found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/{station}")
def get_weather_by_station(station: str):
    try:
        data = load_weather_data()
        result = [record for record in data if record.get("stacja") == station]
        if not result:
            raise HTTPException(status_code=404, detail="Station not found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/wheater/stats/")
def get_weather_stats():
    stats={}
    with open("logs/app.log", "r", encoding="utf-8") as f:
        for line in f:
            if "Średnia temperature" in line:
                stats["avg_temperature"] = float(line.split(":")[-1].strip())
            elif "Maksymalna temperature" in line:
                stats["max_temperature"] = float(line.split(":")[-1].strip())
            elif "Minimalna temperature" in line:
                stats["min_temperature"] = float(line.split(":")[-1].strip())
            elif "Średnia pressure" in line:
                stats["avg_pressure"] = float(line.split(":")[-1].strip())
            elif "Maksymalna pressure" in line:
                stats["max_pressure"] = float(line.split(":")[-1].strip())
            elif "Minimalna pressure" in line:
                stats["min_pressure"] = float(line.split(":")[-1].strip())
            elif "Średnia humidity" in line:
                stats["avg_humidity"] = float(line.split(":")[-1].strip())
            elif "Maksymalna humidity" in line:
                stats["max_humidity"] = float(line.split(":")[-1].strip())
            elif "Minimalna humidity" in line:
                stats["min_humidity"] = float(line.split(":")[-1].strip())
    return stats
