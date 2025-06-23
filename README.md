# Chessgames.com Scraper

This project scrapes metadata and PGN data from [Chessgames.com](https://www.chessgames.com/) for a list of game URLs. It outputs:

- A CSV file containing metadata for each game (players, result, location, opening, etc.)
- A `.pgn` file with all game data, formatted cleanly for use in PGN viewers or databases
- A list of failed game IDs, if any

---

## 📁 Project Structure

| File / Folder                            | Purpose                                                                         |
| ---------------------------------------- | ------------------------------------------------------------------------------- |
| `main.py`                                | Entrypoint script that runs the scraper logic from `cgcom_scraper.py`           |
| `cgcom_scraper.py`                       | Main script that fetches PGNs and extracts metadata from Chessgames.com         |
| `chess_openings.py`                      | Utility for identifying the opening name from a PGN using FEN-based matching    |
| `eco-codes/`                             | Folder containing a CSV file of chess openings with SAN move sequences and FENs |
| `add_fen.py`                             | One-time utility script to add FENs to the opening database from move sequences |
| `input/`                                 | Directory for input file (see below)                                            |
| `output/`                                | Directory for output files (see below)                                          |

---

## 📥 Input Files

Input is read from the `input/` directory.

| File       | Description                                               |
| ---------- | --------------------------------------------------------- |
| `input/urls.txt` | List of Chessgames.com game URLs to scrape (one per line) |

---

## 📤 Output Files

Output is written to the `output/` directory.

| File                              | Description                             |
| --------------------------------- | --------------------------------------- |
| `output/scraped_chessgames_metadata__<timestamp>.csv` | Timestamped CSV of metadata for each scraped game   |
| `output/scraped_chessgames_pgns__<timestamp>.pgn`     | Timestamped combined PGNs with clean formatting     |
| `output/failed_gids__<timestamp>.txt`                 | Timestamped list of game IDs that failed to process |
| `output/scraped_chessgames_metadata_latest.csv` | Most recent CSV of metadata for each scraped game   |
| `output/scraped_chessgames_pgns_latest.pgn`     | Most recent combined PGNs with clean formatting     |
| `output/failed_gids_latest.txt`                 | Most recent list of game IDs that failed to process |

---

## 🧰 Installation

1. Clone the repository:

```bash
git clone https://github.com/joeldick/chessgames-scraper.git
cd chessgames-scraper
```

2. Set up a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

This installs the following packages:
- [`pycountry`](https://pypi.org/project/pycountry/)
- [`python-chess`](https://pypi.org/project/python-chess/)


## 🚀 Usage

1. Add game URLs to `input/urls.txt`, one per line. Example:

```
https://www.chessgames.com/perl/chessgame?gid=1060718
https://www.chessgames.com/perl/chessgame?gid=1451573
```

2. Run the scraper:

```bash
python main.py
```

---

## 🧠 Opening Detection Logic

Opening names are assigned based on FEN positions matched from a cleaned opening database (`eco-codes/opening_names.csv`). The logic walks through each move in a game, checking whether the current board state matches any known FENs in the database.

---
