import requests
from bs4 import BeautifulSoup
import csv
import time
import logging

# configuração do logging
logging.basicConfig(
    filename="crawler.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

headers = {"User-Agent": "Mozilla/5.0"}

start_url = "https://en.wikipedia.org/wiki/Web_scraping"

visited = set()
queue = [start_url]

with open("wikipedia_dataset.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)
    writer.writerow(["url", "title", "text", "links", "images"])

    while queue and len(visited) < 752:

        url = queue.pop(0)

        if url in visited:
            continue

        print("Visiting:", url)

        visited.add(url)

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro HTTP em {url}: {e}")
            print("Erro ao aceder:", url)
            continue

        try:
            # título
            title_tag = soup.find("h1")
            title = title_tag.text.strip() if title_tag else "N/A"

            # texto
            paragraphs = soup.find_all("p")
            text = " ".join(p.text for p in paragraphs) if paragraphs else ""

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
                text[:5000],
                ";".join(set(links)),
                ";".join(set(images))
            ])
        #erro ao processar o HTML, como falta de tags ou estrutura inesperada
        except Exception as e:
            logging.error(f"Erro ao processar HTML em {url}: {e}")
            print("Erro ao extrair dados:", url)

        time.sleep(1)