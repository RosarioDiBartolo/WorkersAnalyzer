import os.path

import pandas as pd

from WorkersAnalyzer.UserExtractor import UserExtractor
from WorkersAnalyzer.Core import PDFIterator
from WorkersAnalyzer.PisaExtractor import PisaExtractor



def Ttest():


    pages = open__raw_test("Andreotti Valeria_AOUP_timbrature")
    extractor = UserExtractor([ PisaExtractor( page ) for page in pages ] [0:1] )

    Data = pd.DataFrame(list(extractor.data["entrata"])).reset_index()
    Data["Turni"] =  extractor.turni()
    print(Data)

Ttest()