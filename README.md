# Chessgames.com Scraper

This project scrapes metadata and PGN data from [Chessgames.com](https://www.chessgames.com/) for a list of game URLs. It outputs:

- A CSV file containing metadata for each game (players, result, location, opening, etc.)
- A `.pgn` file with all game data, formatted cleanly for use in PGN viewers or databases
- A list of failed game IDs, if any

---

## 📁 Project Structure

| File / Folder       | Purpose                                                                         |
| ------------------- | ------------------------------------------------------------------------------- |
| `main.py`           | Entrypoint script that runs the scraper logic from `cgcom_scraper.py`           |
| `cgcom_scraper.py`  | Main script that fetches PGNs and extracts metadata from Chessgames.com         |
| `chess_openings.py` | Utility for identifying the opening name from a PGN using FEN-based matching    |
| `eco-codes/`        | Folder containing a CSV file of chess openings with SAN move sequences and FENs |
| `add_fen.py`        | One-time utility script to add FENs to the opening database from move sequences |
| `urls.txt`          | Input file listing Chessgames.com game URLs (one per line)                      |
| `input/`            | Directory for input file (see below)                                            |
| `output/`           | Directory for output files (see below)                                          |

---

## 📤 Input Files

Output is written to the `output/` directory.

| File       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `urls.txt` | List of urls from chessgames.com of the games to scrape |

---

## 📤 Output Files

Output is written to the `output/` directory.

| File                              | Description                             |
| --------------------------------- | --------------------------------------- |
| `scraped_chessgames_metadata.csv` | CSV of metadata for each scraped game   |
| `scraped_chessgames_pgns.pgn`     | Combined PGNs with clean formatting     |
| `failed_gids.txt`                 | List of game IDs that failed to process |

---

## 🚀 Usage

1. Clone the repository:

```bash
git clone https://github.com/joeldick/chessgames-scraper.git
cd chessgames-scraper
```

2. Install dependencies:

> No external libraries are required beyond Python standard library (Python 3.7+)

3. Add game URLs to `input\urls.txt`, one per line. Example:

```
https://www.chessgames.com/perl/chessgame?gid=1060718
https://www.chessgames.com/perl/chessgame?gid=1451573
```

4. Run the scraper:

```bash
python main.py
```

---

## 🧠 Opening Detection Logic

Opening names are assigned based on FEN positions matched from a cleaned opening database (`eco-codes/opening_names.csv`). The logic walks through each move in a game, checking whether the current board state matches any known FENs in the database.

---
