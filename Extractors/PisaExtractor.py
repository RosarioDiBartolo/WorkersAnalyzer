import pandas as pd

from OCRExtractor import OCRExtractor


class PisaExtractor(OCRExtractor):
    w_days = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']

    def extract_from_text_corpus(self, corpus):
        start = corpus.find("\nE")  # start of the entries rows
        rows = corpus[start + 1:].split("\n")
        name = ''.join(char for char in corpus.split("\n")[0] if char.isalpha()  or char == ' ').removeprefix(' ').removesuffix(' ')
        data = [
            OCRExtractor.isEntry (  row.split()[0][:6]) for row in rows[1:]
        ]

        df = pd.DataFrame({'orario': data})

        return df, name