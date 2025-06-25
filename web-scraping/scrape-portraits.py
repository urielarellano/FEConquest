import requests
from bs4 import BeautifulSoup
import os
import time
import json

url = "https://serenesforest.net/gallery/fire-emblem-fates/"
os.makedirs("FatesPortraits", exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch page
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

# Find all portrait links
portrait_links = soup.find_all("a", class_="ngg-fancybox")

for a in portrait_links:
    name = a.get("data-title", "Unknown").strip().replace(" ", "_")
    img_url = a.get("href")

    if not img_url or not name:
        continue

    print(f"Downloading {name}...")

    img_data = requests.get(img_url, headers=headers).content
    path = os.path.join("FatesPortraits", f"{name}.png")
    with open(path, "wb") as f:
        f.write(img_data)

    time.sleep(0.5)  # be polite to the server

print("✅ Done!")
