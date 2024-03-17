from WorkersAnalyzer.PisaExtractor import PisaExtractor
from WorkersAnalyzer.EasyTest.Test import pages
pages = pages[0:1]

#pages = PDFIterator(["./WorkersAnalyzers/PisaTests/Galli Chiara_AOUP_timbrature.pdf"])
encoded = PisaExtractor(pages[0]).encode()

print(encoded)
"""
extractedData = [PisaExtractor(page).data for page in pages]
Extractor = UserExtractor( extractedData  )

def turno(entrata):
    if datetime.time(hour=6) < entrata < datetime.time(hour=14):
        return "Mattina"
    elif datetime.time(hour=14) < entrata < datetime.time(hour=20):
        return "Pomeriggio"
    else:
        return "Notte"

turni = Extractor.data.apply(lambda date: turno(date.time()) )
values: pd.Series = turni.value_counts()


values.to_csv(f"./Results/values.csv")
Extractor.data.to_csv("./Results/filtered.csv")"""