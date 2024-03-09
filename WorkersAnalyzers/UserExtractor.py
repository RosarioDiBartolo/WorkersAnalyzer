import datetime

import pandas as pd



class UserExtractor:
    def __init__(self, pages):
        self.data = UserExtractor.extract_from_pages(pages)


    @staticmethod
    def extract_from_pages(extractedData):
        df = pd.concat(  extractedData )
        df.drop(df[df["Tipo"] == "Mensa"].index)
        df["Boolean-Type"] = df["Tipo"] == "E"

        iter = df.iterrows()

        couples = []
        for idx, row in df.iterrows():
            if not row["Boolean-Type"]:
                continue

            for idx, newRow in iter:

                if not newRow["Boolean-Type"]:
                    couples.append((row["Data"], newRow["Data"]))
                    break
                else:
                    row = newRow

        couples = pd.DataFrame(couples, columns=["entrata", "uscita"])

        filtered = couples[( couples["uscita"]  - couples["entrata"] ) > datetime.timedelta(hours = 6)]
        return filtered["entrata"]