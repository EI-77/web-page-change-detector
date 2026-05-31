import os
import csv
import json
import hashlib
import requests

from bs4 import BeautifulSoup
from datetime import datetime


URLS = [
    "https://example.com",
]

DATA_DIR = "data"
HASH_FILE = os.path.join(DATA_DIR, "hashes.json")
LOG_FILE = os.path.join(DATA_DIR, "change_log.csv")


def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def make_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}

    with open(HASH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_hashes(hashes):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes, f, ensure_ascii=False, indent=4)


def write_log(url, status, checked_at):
    os.makedirs(DATA_DIR, exist_ok=True)

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["url", "status", "checked_at"])

        writer.writerow([url, status, checked_at])


def check_page(url, hashes):
    html = fetch_page(url)
    text = extract_text(html)
    current_hash = make_hash(text)

    previous_hash = hashes.get(url)

    if previous_hash is None:
        status = "first_check"
    elif previous_hash != current_hash:
        status = "changed"
    else:
        status = "no_change"

    hashes[url] = current_hash

    checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_log(url, status, checked_at)

    print(f"{url}: {status}")


def main():
    hashes = load_hashes()

    for url in URLS:
        try:
            check_page(url, hashes)
        except Exception as e:
            checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write_log(url, "error", checked_at)
            print(f"{url}: error")
            print(e)

    save_hashes(hashes)


if __name__ == "__main__":
    main()
    