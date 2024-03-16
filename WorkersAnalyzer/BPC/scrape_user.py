import os
from datetime import datetime
from WorkersAnalyzer.BPC.crawler import login, crawl, mesi




now = datetime.now()
current_year = now.year
max_month = now.month

results_folder = "./results"

if not os.path.exists(results_folder):
    os.makedirs(results_folder)


username = "30105"
password = "cespiti"

start = 2019




session = login(username , password )
for year in range(start, current_year + 1):
    if year == current_year:
        r = range(0, max_month + 1 )
    else:
        r = range(0, 12)
    for month_idx in r:
        month = mesi[month_idx]

        result = crawl(session, year, month, username)

        with open(f"{results_folder}/{year}_{month}.pdf", "wb") as f:
            f.write(result.content)