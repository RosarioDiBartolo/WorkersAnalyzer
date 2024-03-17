from urllib.request import DataHandler

from WorkersAnalyzer.Core import turno
import pandas as pd

from WorkersAnalyzer.Extractors.DataFrameHandler import DataFrameWrapper

DataInfo = ["Tipo", "Data"]


class DataExtracted(DataFrameWrapper(DataInfo)):

    def turni(self):
        return self.raw["Data"].apply(lambda e: turno(  e.time() )   )

