import pandas as pd

from Core import PDFBlock
from Extractors.PisaExtractor import PisaExtractor as ExtractorType

filename = "Andreotti Valeria_AOUP_timbrature.pdf"


block = PDFBlock.from_file(filename)
extractor = ExtractorType( block.pages  )

features: list[pd.DataFrame] = extractor.features()

concatenated = pd.concat( features)
print(concatenated['turno'].value_counts())