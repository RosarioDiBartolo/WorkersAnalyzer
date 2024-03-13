import datetime
import os

import numpy as np
import pandas as pd

from WorkersAnalyzer.Core import PDFIterator, turno, Directory
from WorkersAnalyzer.PisaExtractor import PisaExtractor

class UserExtractor:
    def __init__(self, Extractors):
        self.data = UserExtractor.extract_from_extractors(Extractors)

    def turni(self):
        return self.data["entrata"].apply(lambda e: turno(e["Data"].time()))
    @staticmethod
    def extract_from_extractors( Extractors: list[PisaExtractor] ):


        df = pd.concat( e.with_datetime() for e in Extractors)


        #dropping mensa
        df.drop(df[df["Tipo"] == "M"].index)

        df["Boolean-Type"] = df["Tipo"] == "E"
        iter = df.iterrows()
        couples = []
        for i, row in iter:
            if not row["Boolean-Type"]:
                continue

            for i, newRow in iter:

                if not newRow["Boolean-Type"]:
                    couples.append(( row  ,   newRow  ) )
                    break
                else:
                    row = newRow

        couples = pd.DataFrame(couples, columns=["entrata", "uscita" ])

        filtered = couples[( couples["uscita"].apply(lambda r: r["Data"] )  - couples["entrata"].apply(lambda r: r["Data"] ) ) > datetime.timedelta(hours = 6)]

        return  filtered


if __name__ == '__main__':
     from Test import test_on_files

     Out_dir = Directory("../Filtered/")

     for file_pages, name in test_on_files():
        try:
            extractor = UserExtractor( [PisaExtractor(page) for page in file_pages ] )

            Elaboration =   (extractor.data["entrata"].apply(lambda row: row["Data"] )).apply(lambda Data: ( Data.year, turno( Data.time())) )
            Elaboration = pd.DataFrame(list(Elaboration), columns = ["Anno", "Turno"])

            Elaboration.groupby("Anno", include_groups=False).apply( lambda Anno: Anno["Turno"].value_counts().to_csv(  Out_dir.path( name ).to(f'{Anno.name}.csv') )  )
        except Exception as e:
            print(e)
        

        


