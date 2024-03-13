import datetime
import os

import numpy as np
import pandas as pd

from WorkersAnalyzer.Core import PDFIterator, turno, Directory
from WorkersAnalyzer.PisaExtractor import PisaExtractor




class UserExtractor:
    def __init__(self, Extractors):

        self.data, self.name  = UserExtractor.extract_from_extractors(Extractors)

    def elaborate(extractor):
        Elaboration = (extractor.data["entrata"].apply(lambda row: row["Data"])).apply(
            lambda Data: (Data.year, turno(Data.time())))
        Elaboration = pd.DataFrame(list(Elaboration), columns=["Anno", "Turno"])

        return Elaboration.groupby("Anno" )


    @staticmethod
    def from_block(block):
        return UserExtractor(  [ PisaExtractor(page) for page in block  ] )

    @staticmethod
    def from_files(files):
        pages = [page for file in files for page in PDFIterator(file)]
        return UserExtractor(   PisaExtractor(page) for page in pages   )


    @staticmethod
    def extract_from_extractors( Extractors: list[PisaExtractor] ):

        names = {e.name for e in Extractors}
        if len(names)> 1:
            raise Exception("Nomi diversi all'interno delle pagine...")

        df = pd.concat( e.with_datetime() for e in Extractors ).dropna()



        df.drop(df[df["Tipo"] == "M"].index)

        df["Boolean-Type"] = df["Tipo"] == "E"

        df.sort_values(by='Data', ascending=True, inplace=True)

        iter = df.iterrows()
        Entrate = []
        Uscite = []
        for i, row in iter:
            if not row["Boolean-Type"]:
                continue

            for i, newRow in iter:

                if not newRow["Boolean-Type"]:
                    Entrate.append(row )
                    Uscite.append(newRow)
                    break
                else:
                    row = newRow

        Entrate = pd.DataFrame(Entrate).reset_index(drop=True)
        Uscite = pd.DataFrame(Uscite).reset_index(drop=True)

        filtered = Entrate[ (  Uscite["Data"] - Entrate["Data"]  ) > datetime.timedelta(hours = 6) ]


        return  filtered, list(names)[0]



if __name__ == '__main__':
     from Test import test_on_files

     Out_dir = Directory("../Filtered/")

     for file_pages, name in test_on_files():
         try:

            extractor = UserExtractor.from_block(file_pages)
            Anni = extractor.elaborate()
            Anni.apply(
                lambda Anno: Anno["Turno"].value_counts().to_csv(Out_dir.path(name).to(f'{Anno.name}.csv'))
            )
         except Exception as e:
             print(e)


        

        


