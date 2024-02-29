import pandas as pd

from .OCRExtractor import OCRExtractor


class PisaExtractor(OCRExtractor):
    w_days = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
    columns = ['Giorno', 'Timbrature', 'Assenze', 'Anomalie/P.O.', 'Timbr.', 'Dovuto', 'Totale', 'Saldo', 'Turno', 'Ore Repe', 'Repe Eff']

    def handle_data_row(self, row):

        words = row.split()
        if len(words) >= 9:
            return

        possible_orario =  words[0][:6]
        return OCRExtractor.isEntry (  possible_orario   )




    def extract_from_text_corpus(self, corpus):
        start = corpus.find("\nE")  # start of the entries rows
        rows = corpus[start + 1:].split("\n")
        name = ''.join(char for char in corpus.split("\n")[0] if char.isalpha()  or char == ' ').replace("Matricola", "").strip()
        orario = [

            self.handle_data_row(row) for row in rows

        ]

        df = pd.DataFrame({'orario': orario})

        return df, name