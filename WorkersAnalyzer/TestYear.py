import pandas as pd

from PisaExtractor import PisaExtractor, mesi
from WorkersAnalyzer.Core import PDFIterator, turno
from WorkersAnalyzer.DataExtracted import DataExtracted
from WorkersAnalyzer.UserExtractor import UserExtractor

Anno = 2019

Extractors = [ PisaExtractor(p)  for p in PDFIterator("../PisaTests/Andreotti Valeria_AOUP_timbrature.pdf")]

Extractor = UserExtractor(Extractors)
data = Extractor.data


interested = DataExtracted(data[data["Data"].apply(lambda d: d.year) == 2019])


