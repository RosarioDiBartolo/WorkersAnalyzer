import pandas as pd
from WorkersAnalyzer.Extractors.DataFrameHandler import DataFrameWrapper
from WorkersAnalyzer.Extractors.DataExtracted import DataExtracted

datetime_format = '%Y-%m-%d  %H:%M'  # Example format: 'days hours:minutes'

import pandas as pd



PageColumns =  ["Tipo", "Giorno", "Ore", "Minuti", "Settimana"]
class PageData(DataFrameWrapper( PageColumns )):


    def __init__(self, anno, mese, nome, data):
        self.anno = anno
        self.mese = mese
        self.nome = nome

        #Checs if columns requirements are met
        super().__init__( pd.DataFrame(data, columns=PageColumns))

    def encode_date(self):
        datetime_string = str(self.anno) + "-" + str(self.mese) + "-" + self.raw["Giorno"].astype(
            str) + " " + self.raw["Ore"].astype(str) + ":" + self.raw["Minuti"].astype(str)
        return pd.to_datetime(datetime_string, format=datetime_format)

    def with_datetime(self):
        return DataExtracted( self.raw.assign(Data = self.encode_date()).drop( columns=["Giorno", "Ore", "Minuti"], axis=1) )