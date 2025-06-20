# Chessgames.com Scraper

This project scrapes metadata and PGN data from [Chessgames.com](https://www.chessgames.com/) for a list of game URLs. It outputs:

- A CSV file containing metadata for each game (players, result, location, opening, etc.)
- A `.pgn` file with all game data, formatted cleanly for use in PGN viewers or databases
- A list of failed game URLs, if any

## Features

- Fetches PGN data directly from Chessgames.com by game ID
- Extracts useful metadata such as:
  - Player names
  - Location and event
  - Year, round, result
  - Number of moves
  - Opening name (based on FEN position matching)
- Writes clean PGN files with one blank line between games
- Logs failed game URLs

## Usage

1. Clone the repository:

```bash
git clone https://github.com/joeldick/chessgames-scraper.git
cd chessgames-scraper
```

2. Create a Python virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `urls.txt` file and paste in full game URLs, one per line, like:

```
https://www.chessgames.com/perl/chessgame?gid=1011478
https://www.chessgames.com/perl/chessgame?gid=1251877
...
```

5. Run the scraper:

```bash
python main.py
```

6. Output files:

- `scraped_chessgames_metadata.csv`
- `scraped_chessgames_pgns.pgn`
- `failed_gids.csv` (optional, if any games failed)

## Project Structure

```
.
├── main.py
├── chess_openings.py
├── eco-codes/
│   └── opening_names.csv
├── urls.txt
├── scraped_chessgames_metadata.csv
├── scraped_chessgames_pgns.pgn
├── failed_gids.csv
├── .gitignore
└── README.md
```

## License

MIT License (or replace with your preferred license)

---

**Tip**: Use the PGN file in chess software like SCID, ChessBase, or Lichess Study Import to browse the scraped games.
