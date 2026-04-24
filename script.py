import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import csv

URL = "https://rent.pe.ntu.edu.tw/"
TW = timezone(timedelta(hours=8))

def fetch():
    res = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    for item in soup.select(".CMCItem"):
        name = item.select_one(".IT").get_text(strip=True)

        if name != "健身中心":
            continue

        current = int(item.select(".ICI span")[0].get_text())

        return {
            "time": datetime.now(TW).strftime("%Y-%m-%d %H:%M:%S"),
            "current": current
        }

def save(data):
    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data["time"], data["current"]])

def main():
    data = fetch()
    if data:
        save(data)
        print("saved:", data)

if __name__ == "__main__":
    main()
