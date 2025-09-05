import requests, json, os
from datetime import datetime, timezone

API_KEY = os.getenv("OPENWEATHER_API_KEY", "c56866fba4ef4af770ec57a71829ed76")

cities = ["Lahore", "Islamabad", "Multan", "Depalpur", "Okara", "Basirpur"]

def fetch_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        # Check if API returned valid response
        if data.get("cod") != 200:
            print(f"⚠️ API Error for {city}: {data.get('message')}")
            return {
                "city": city,
                "temperature": 0,
                "humidity": 0,
                "description": "City not found",
                "sunrise": 0,
                "sunset": 0
            }

        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"]
        }
    except Exception as e:
        print(f"❌ Error fetching {city}: {e}")
        return {
            "city": city,
            "temperature": 0,
            "humidity": 0,
            "description": "N/A",
            "sunrise": 0,
            "sunset": 0
        }

def main():
    all_weather = [fetch_weather(c) for c in cities]
    last_update = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    data = {
        "last_update": last_update,
        "cities": all_weather
    }

    with open("weather.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Weather updated at", last_update)

if __name__ == "__main__":
    main()
