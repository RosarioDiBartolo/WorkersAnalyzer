import pandas as pd

from Core import turno

from Extractors.OCRExtractor import OCRExtractor
class PoliclinicoExtractor(OCRExtractor):

    @staticmethod
    def analyze(row):
        values = row.split()
        giorno_settimana = values[0]
        giorno = values[1]
        entry = None
        for word in values[2:]:
            Firstletter = word[0]
            if Firstletter.upper() == "E":
                entry = word[1:]
                break
        return {"w-day": giorno_settimana, "day": giorno, "entrata": entry}

    def extract_from_text_corpus(self, corpus):
        rows = corpus.split("\n")

        Data = []
        for row in rows[7:]:
            try:
                float(row) #La tabbella è delineata da una riga contenente un singolo numro in virgola mobile
                Data = pd.DataFrame(Data).dropna()
                print(Data)
                Data["orario"] = Data["entrata"].apply(lambda orario: f"{orario[:2]}:{orario[2:]}")
                Data["turno"] = Data["entrata"].apply(turno)

                return Data
            except ValueError:
                Data.append(
                    PoliclinicoExtractor.analyze(row.replace('*', ' ')  )
                ) #avvolte è aggiunto un asterisco al posto dello spazio)
