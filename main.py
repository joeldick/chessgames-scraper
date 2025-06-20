import re
import csv
import time
from datetime import datetime
import shutil
from cgcom_scraper import *

if __name__ == "__main__":
    with open("input/urls.txt", encoding="utf-8") as f:
        urls = f.readlines()
    gids = [re.search(r"gid=(\d+)", url).group(1) for url in urls if re.search(r"gid=(\d+)", url)]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"output/scraped_chessgames_metadata_{timestamp}.csv"
    output_pgn = f"output/scraped_chessgames_pgns_{timestamp}.pgn"
    failed_gids = []
    output_failed = f"output/failed_gids_{timestamp}.txt"
    success_count, failed_count = 0, 0

    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
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
                with open(output_pgn, mode="a", encoding="utf-8") as pf:
                    pf.write(clean_pgn(pgn) + "\n\n")
                print(f"Saved game {gid}")
                success_count += 1
            except Exception as e:
                print(f"Error processing gid {gid}: {e}")
                failed_gids.append(f"https://www.chessgames.com/perl/chessgame?gid={gid}")
                failed_count += 1
            time.sleep(1.0)

    if failed_gids:
        with open(output_failed, mode="w", encoding="utf-8") as f:
            f.write(",".join(failed_gids))

    shutil.copy(output_csv, "output/scraped_chessgames_metadata_latest.csv")
    shutil.copy(output_pgn, "output/scraped_chessgames_pgns_latest.pgn")
    shutil.copy(output_failed, "output/failed_gids_latest.txt")

    print("\n=== Output Files ===")
    print(f"Metadata CSV:        {output_csv}")
    print(f"PGN File:            {output_pgn}")
    print(f"Failed URLs:         {output_failed}")
    print("\n=== Summary ===")
    print(f"✅ Successful games: {success_count}")
    print(f"❌ Failed games:     {failed_count}")
