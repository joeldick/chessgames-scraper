import re
import csv
import time
from cgcom_scraper import *

if __name__ == "__main__":
    with open("input/urls.txt", encoding="utf-8") as f:
        urls = f.readlines()
    gids = [re.search(r"gid=(\d+)", url).group(1) for url in urls if re.search(r"gid=(\d+)", url)]

    output_file = "output/scraped_chessgames_metadata.csv"
    pgn_file = "output/scraped_chessgames_pgns.pgn"
    failed_gids = []
    failed_file = "output/failed_gids.txt"
    success_count, failed_count = 0, 0

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "White", "Black", "Location", "Year", "Event", "Result", "Moves", "Opening", "Link"
        ])
        writer.writeheader()

        for gid in gids:
            try:
                pgn = get_pgn(str(gid))
                metadata = metadata_from_pgn(pgn)
                metadata["Link"] = f"https://www.chessgames.com/perl/chessgame?gid={gid}"
                print(metadata)
                writer.writerow(metadata)
                with open(pgn_file, mode="a", encoding="utf-8") as pf:
                    pf.write(clean_pgn(pgn) + "\n\n")
                print(f"Saved game {gid}")
                success_count += 1
            except Exception as e:
                print(f"Error processing gid {gid}: {e}")
                failed_gids.append(f"https://www.chessgames.com/perl/chessgame?gid={gid}")
                failed_count += 1
            time.sleep(1.0)

    if failed_gids:
        with open(failed_file, mode="w", encoding="utf-8") as f:
            f.write(",".join(failed_gids))

    print(f"Count: {success_count}. Failed: {failed_count}")