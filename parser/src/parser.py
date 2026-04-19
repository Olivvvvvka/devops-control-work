import requests
import json
import os
from datetime import datetime
import psycopg2

def fetch_openmeteo(lat=48.7080, lon=44.5133, city="Волгоград"):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "auto"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        curr = data.get("current_weather", {})
        return {
            "source": "openmeteo",
            "city": city,
            "temp": curr.get("temperature"),
            "wind_speed": curr.get("windspeed"),
            "wind_dir": curr.get("winddirection"),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    except Exception as e:
        return {"error": str(e)}

def load_mock():
    with open("mock_gismeteo.json") as f:
        return json.load(f)

def collect_all():
    data = []
    om = fetch_openmeteo()
    if "error" not in om:
        data.append(om)
    data.append(load_mock())
    return [d for d in data if "error" not in d]

def save_to_db(data):
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="weather_db",
            user="admin",
            password="adminpass"
        )
        cur = conn.cursor()
        
        for record in data:
            cur.execute(
                "INSERT INTO weather_data (source, city, product_type, value, unit, wind_speed, wind_direction, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    record["source"],
                    record["city"],
                    "weather",
                    record["temp"],
                    "°C",
                    record["wind_speed"],
                    record["wind_dir"],
                    record["timestamp"]
                )
            )
        
        conn.commit()
        cur.close()
        conn.close()
        print("Данные успешно сохранены в БД")
    except Exception as e:
        print(f"Ошибка при сохранении данных в БД: {e}")

if __name__ == "__main__":
    results = collect_all()
    print(json.dumps(results, indent=2, ensure_ascii=False))
    save_to_db(results)
    os.makedirs("../logs", exist_ok=True)
    with open("../logs/raw_data.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
