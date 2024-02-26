import os
from datetime import datetime
from crawler import login, crawl


month_mapping = {
    "GENNAIO": 1,
    "FEBBRAIO": 2,
    "MARZO": 3,
    "APRILE": 4,
    "MAGGIO": 5,
    "GIUGNO": 6,
    "LUGLIO": 7,
    "AGOSTO": 8,
    "SETTEMBRE": 9,
    "OTTOBRE": 10,
    "NOVEMBRE": 11,
    "DICEMBRE": 12
}

mesi = list( month_mapping.keys() )

now = datetime.now()
current_year = now.year
max_month = now.month

results_folder = "./results"

if not os.path.exists(results_folder):
    os.makedirs(results_folder)


username = "5388"
password = "salvolimo"

start = 2019

"""def generate_year_month_tuples(starting_year, starting_month ):
    starting_month_idx = month_mapping[starting_month]
    for year in range(starting_year, current_year + 1):
        if year == current_year:
            r = range(0 , max_month + 1)
        elif year == starting_year:
            r = range(starting_month_idx,  12)

        else:
            r = range(0,  12)
        for month_idx in r:
            month = mesi[month_idx]

            yield (year, month)
    return result"""


session = login(username , password )
for year in range(start, current_year + 1):
    if year == current_year:
        r = range(0, max_month + 1 )
    else:
        r = range(0, 12)
    for month_idx in r:
        month = mesi[month_idx]
        print(year, month)
        result = crawl(session, year, month, username)

        with open(f"{results_folder}/{year}_{month}.pdf", "wb") as f:
            f.write(result.content)