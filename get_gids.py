import re

with open("urls.txt", encoding="utf-8") as f:
    urls = f.readlines()
gids = [re.search(r"gid=(\d+)", url).group(1) for url in urls if re.search(r"gid=(\d+)", url)]

print(gids)