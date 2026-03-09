import requests
from bs4 import BeautifulSoup
import csv
import time

url = "https://en.wikipedia.org/wiki/Web_scraping"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

html = response.text
soup = BeautifulSoup(html, "html.parser")

links = []

for link in soup.find_all("a"):
    href = link.get("href")

    if href and href.startswith("/wiki/") and ":" not in href:
        full = "https://en.wikipedia.org" + href
        links.append(full)


#remover duplicados
links = list(set(links))
print(len(links))

title = soup.find("h1").text

paragraphs = soup.find_all("p")
text = " ".join(p.text for p in paragraphs)

print(title)
print(text[:500])

images = []

for img in soup.find_all("img"):
    src = img.get("src")

    if src:
        if src.startswith("//"):
            src = "https:" + src

        images.append(src)

print(images[:10])

data = {
    "url": url,
    "title": title,
    "text": text,
    "links": links,
    "images": images
}

import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {"User-Agent": "Mozilla/5.0"}

start_url = "https://en.wikipedia.org/wiki/Web_scraping"

visited = set()
queue = [start_url]

with open("wikipedia_dataset.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)
    writer.writerow(["url", "title", "text", "links", "images"])

    while queue and len(visited) < 1000:

        url = queue.pop(0)

        if url in visited:
            continue

        print("Visiting:", url)

        visited.add(url)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # título
        title = soup.find("h1").text if soup.find("h1") else ""

        # texto
        paragraphs = soup.find_all("p")
        text = " ".join(p.text for p in paragraphs)

        # links
        links = []
        for a in soup.find_all("a"):
            href = a.get("href")

            if href and href.startswith("/wiki/") and ":" not in href:
                full = "https://en.wikipedia.org" + href
                links.append(full)

                if full not in visited:
                    queue.append(full)

        # imagens
        images = []
        for img in soup.find_all("img"):
            src = img.get("src")

            if src:
                if src.startswith("//"):
                    src = "https:" + src

                images.append(src)

        # guardar no CSV
        writer.writerow([
            url,
            title,
            text[:5000],   # limitar tamanho
            ";".join(set(links)),
            ";".join(set(images))
        ])

        time.sleep(1)