import requests
import pandas as pd
import os

APP_ID = os.getenv("ADZUNA_APP_ID", "66ff9d19")
APP_KEY = os.getenv("ADZUNA_APP_KEY", "212d688401bea5cd4a9484cce9ebe4a3")

CITIES = {
    "Berlin": "de",
    "Munich": "de",
    "Amsterdam": "nl",
    "Vienna": "at",
    "Zurich": "ch"
}

STATIC_DATA = {
    "Berlin":    {"Cost of Living Index": 58.2, "Safety Index": 55.1, "Internet Speed (Mbps)": 107},
    "Munich":    {"Cost of Living Index": 68.4, "Safety Index": 62.3, "Internet Speed (Mbps)": 132},
    "Amsterdam": {"Cost of Living Index": 73.1, "Safety Index": 59.8, "Internet Speed (Mbps)": 204},
    "Vienna":    {"Cost of Living Index": 65.3, "Safety Index": 67.4, "Internet Speed (Mbps)": 178},
    "Zurich":    {"Cost of Living Index": 93.6, "Safety Index": 74.2, "Internet Speed (Mbps)": 231},
}

def fetch_job_count(city, country_code):
    try:
        url = (
            f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
            f"?app_id={APP_ID}&app_key={APP_KEY}"
            f"&what=software+engineer&where={city}"
            f"&results_per_page=1&content-type=application/json"
        )
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get("count", 0)
    except:
        return 0

def fetch_all_cities():
    results = []
    for city, country_code in CITIES.items():
        print(f"Fetching data for {city}...")
        job_count = fetch_job_count(city, country_code)
        static = STATIC_DATA[city]
        results.append({
            "City": city,
            "Job Count": job_count,
            "Cost of Living Index": static["Cost of Living Index"],
            "Safety Index": static["Safety Index"],
            "Internet Speed (Mbps)": static["Internet Speed (Mbps)"]
        })
    return pd.DataFrame(results)
