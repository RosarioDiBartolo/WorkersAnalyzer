import os.path

import pandas as pd

from WorkersAnalyzer.Test import open_raw_test
from WorkersAnalyzer.UserExtractor import UserExtractor
from WorkersAnalyzer.Core import PDFIterator
from WorkersAnalyzer.PisaExtractor import PisaExtractor



pages = [p for p in PDFIterator( "../PisaTests/Giannini Simone_AOUP_timbrature.pdf") if p ]
extractor = UserExtractor([PisaExtractor(p) for p in pages] )

values  = extractor.elaborate().apply(
            lambda Anno: Anno["Turno"].value_counts().to_dict()
        ).to_json()

print(values)