import requests
import re
from math import ceil
import pycountry

from chess_openings import find_opening_from_pgn

CUSTOM_COUNTRY_CODES = {
    "GER": "Germany",
    "RUE": "Russia",
    "AUH": "Austria-Hungary",
    "MNC": "Monaco",
    "URS": "Soviet Union",
    "YUG": "Yugoslavia",
    "TCH": "Czechoslovakia",
    "GDR": "East Germany",
    "FRG": "West Germany",
    "CSR": "Czechoslovakia",
    "ENG": "England",
    "SCO": "Scotland",
    "USA": "United States",
    "HUN": "Hungary",
    "ROM": "Romania",
    "CUB": "Cuba",
    "ESP": "Spain",
    "DEN": "Denmark",
    "NED": "Netherlands",
    # Add more as needed
}
UNMAPPED_CODES = set()

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
            fields["Opening"] = find_opening_from_pgn(pgn)

        else:
            pattern = tags.get(field)
            match = re.search(pattern, pgn) if pattern else None
            fields[field] = match.group(1)

    return fields

def get_country_name_from_code(code):
    code = code.upper()
    # First, check custom mapping
    if code in CUSTOM_COUNTRY_CODES:
        return CUSTOM_COUNTRY_CODES[code]

    # Fall back to pycountry
    try:
        country = pycountry.countries.get(alpha_3=code)
        if country:
            return country.name
        else:
            UNMAPPED_CODES.add(code)
            return code
    except:
        UNMAPPED_CODES.add(code)
        return code

def normalize_location(site_tag):
    parts = site_tag.strip().split()
    if len(parts) >=2:
        code = parts[-1]
        city = " ".join(parts[:-1])
        return f"{city}, {get_country_name_from_code(code)}"
    else:
        return site_tag

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


