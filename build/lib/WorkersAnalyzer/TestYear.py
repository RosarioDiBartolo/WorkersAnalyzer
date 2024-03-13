import pandas as pd

from PisaExtractor import PisaExtractor, mesi
from WorkersAnalyzer.Core import PDFIterator, turno

Data = pd.concat([PisaExtractor(p).with_specifics() for p in PDFIterator("../PisaTests/Andreotti Valeria_AOUP_timbrature.pdf")])

Anno = 2019

YearData = Data[Data['Anno'].astype(int) == Anno]
Entries =  YearData[YearData["Tipo"]== "E"].copy()
Entries["Mese"] = Entries["Mese"].apply(lambda x : mesi.index(x) + 1 )
Entries["Turno"] = pd.to_datetime( Entries[["Anno", "Mese", "Giorno", "Ore", "Minuti"]].rename(columns={"Anno":"year", "Mese":"month", "Giorno":"day", "Ore":"hour", "Minuti":"minute"}) ).apply(turno)

Entries["Turno"].value_counts().to_csv("Andreotti Valeria_AOUP_timbrature.txt")

