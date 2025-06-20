import requests
import re
from math import ceil
import pycountry
import csv

from chess_openings import find_opening_from_pgn

def get_pgn(gid):
    url = f"http://www.chessgames.com/nodejs/game/viewGamePGN?text=1&gid={gid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    pgn = response.text

    return pgn

def metadata_from_pgn(pgn):
    fields = {
        "White": "",
        "Black": "",
        "Location": "",
        "Year": "",
        "Event": "",
        "Result": "",
        "Moves": "",
        "Opening": "",
    }

    tags = {
        "White": r'\[White "(.*?)"\]',
        "Black": r'\[Black "(.*?)"\]',
        "Site": r'\[Site "(.*?)"\]',
        "Date": r'\[Date "(.*?)"\]',
        "Event": r'\[Event "(.*?)"\]',
        "Round": r'\[Round "(.*?)"\]',
        "Result": r'\[Result "(.*?)"\]',
        "PlyCount": r'\[PlyCount "(.*?)"\]',
        "ECO": r'\[ECO "(.*?)"\]',
    }

    for field in fields:
        if field == "Location":
            match = re.search(tags.get("Site"), pgn)
            fields["Location"] = normalize_location(match.group(1))
        elif field == "Year":
            match = re.search(tags.get("Date"), pgn)
            year = match.group(1).split('.')[0]
            fields["Year"] = int(year)
        elif field == "Event":
            event_match = re.search(tags["Event"], pgn)
            round_match = re.search(tags["Round"], pgn)
            date_match = re.search(tags.get("Date"), pgn)
            if event_match:
                event_name = event_match.group(1)
            if round_match:
                round_num = round_match.group(1)
            if date_match:
                year = match.group(1).split('.')[0]
            if event_name and year:
                fields["Event"] = f"{event_name} {year}"
            if round_num and round_num != "?":
                fields["Event"] = fields["Event"] + f", Round {round_num}"
        elif field == "Moves":
            match = re.search(tags.get("PlyCount"), pgn)
            fields["Moves"] = ceil(int(match.group(1)) / 2)
        elif field == "Opening":
            #match = re.search(tags.get("ECO"), pgn)
            #eco_code = match.group(1)
            #fields["Opening"] = eco_to_name(eco_code)
            fields["Opening"] = find_opening_from_pgn(pgn)

        else:
            pattern = tags.get(field)
            match = re.search(pattern, pgn) if pattern else None
            fields[field] = match.group(1)

    return fields

def get_country_name_from_code(code):
    try:
        country = pycountry.countries.get(alpha_3=code.upper())
        return country.name if country else code
    except:
        return code

def normalize_location(site_tag):
    parts = site_tag.strip().split()
    if len(parts) >=2:
        code = parts[-1]
        city = " ".join(parts[:-1])
        return f"{city}, {get_country_name_from_code(code)}"
    else:
        return site_tag
    
def eco_to_name(eco_code):
    with open("eco-codes/opening_names.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["eco"].strip() == eco_code.strip():
                return row["name"].strip()
    return eco_code

def clean_pgn(pgn):
    # Strip leading/trailing spaces from each line and remove blank lines between tags
    lines = [line.strip() for line in pgn.strip().splitlines()]
    
    cleaned_lines = []
    in_tags = True
    for line in lines:
        if in_tags:
            if line.startswith('['):
                cleaned_lines.append(line)
            elif line == '':
                # ignore blank lines within tag section
                continue
            else:
                # Start of moves
                in_tags = False
                if cleaned_lines and cleaned_lines[-1] != '':
                    cleaned_lines.append('')
                cleaned_lines.append(line)
        else:
            if line != '':
                cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


