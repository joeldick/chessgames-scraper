import requests
from bs4 import BeautifulSoup
from requests.compat import urljoin

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

def extract_game_urls_from_collection(url):
    # Fetch the collection page
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    # Parse the HTML
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find all <tr class="cgame"> rows (each one contains a game)
    rows = soup.select('tr.cgame')
    game_urls = []
    for row in rows:
        a_tag = row.find("a", href=True)
        if a_tag and "gid=" in a_tag["href"]:
            full_url = requests.compat.urljoin(url, a_tag["href"])
            game_urls.append(full_url)

    return sorted(set(game_urls))

def extract_game_urls_from_html_file(filepath, base_url):
    from bs4 import BeautifulSoup

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    game_urls = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/perl/chessgame?gid=" in href:
            full_url = urljoin(base_url, a_tag["href"])
            game_urls.append(full_url)

    return sorted(set(game_urls))


'''if __name__ == "__main__":
    collection_url = "https://www.chessgames.com/perl/chesscollection?cid=1001601"
    game_urls = extract_game_urls_from_collection(collection_url)
    for game_url in game_urls:
        print(game_url)
    print(f"Total games found: {len(game_urls)}")
'''

if __name__ == "__main__":
    file_path = "chesscollection.html"
    base_url = "https://www.chessgames.com"
    urls = extract_game_urls_from_html_file(file_path, base_url)
    for url in urls:
        print(url)
    print(f"\n✅ Total games found: {len(urls)}")
