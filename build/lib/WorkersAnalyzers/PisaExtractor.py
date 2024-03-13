import os
import re
import pandas as pd

from WorkersAnalyzer.Core import PDFIterator, turno
from WorkersAnalyzer.ExctractingError import ExtractingError

w_days = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
datetime_format = '%Y-%m-%d  %H:%M'  # Example format: 'days hours:minutes'



class PisaExtractor:
    columns = ["Tipo", "Giorno", "Ore", "Minuti", "Settimana"]

    SingoliOrari = re.compile(r"\b\d\d:\d\d\b")
    PatternEntrateUscite = re.compile(r"(E|U)(\d\d:\d\d)")
    PatternData = re.compile(r'(Lun|Mar|Mer|Gio|Ven|Sab|Dom)\s(\d\d)')


    NamePattern = re.compile(r'[^a-zA-Z\s]')

    MONTHS_YEAR_PATTERN = re.compile(
        r'(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s(\d\d\d\d)',
        re.IGNORECASE)

    def __init__(self, page):
        self.data, self.name, self.mese, self.anno = PisaExtractor.extract_page(page)
    def with_specifics(self):
        return self.data.assign(Anno = self.anno, Mese = self.mese)
    def save(self, path):
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise Exception(f"Cant' save file here: {path}")
        else:
            os.makedirs(path)

        self.data.to_csv( os.path.join(path, f"{self.name}-{self.anno}-{self.mese}.csv") )
    def encode_date(extractor):
        datetime_string =  extractor.anno + "-" + mesi + "-" + extractor.data["Giorno"].astype(str) + " " + extractor.data["Ore"].astype(str) + ":" + extractor.data["Minuti"].astype(str)
        return pd.to_datetime(datetime_string, format=datetime_format)
    def with_datetime(self):
        return self.data.assign(Data = self.encode_date()).drop(columns=["Giorno", "Ore", "Minuti"], axis=1)
    @staticmethod
    def extract(row):

        EntrateUscite = PisaExtractor.PatternEntrateUscite.findall(row)
        match = PisaExtractor.PatternData.search(row)
        if match:
            wday, day = match.group().split()
            day = int(day)
        else:
            return []

        if  len(PisaExtractor.SingoliOrari.findall(row)) > 4:
            return [("M", day, 0, 0, wday)]

        return [(tipo, day, int(orario[0:2]), int(orario[3:]), wday) for (tipo, orario) in
                EntrateUscite] if EntrateUscite else [(None, day, 0, 0, wday)]

    @staticmethod
    def name_from_page(rows):
        return PisaExtractor.name_from_row(rows[0])

    @staticmethod
    def name_from_row(row):
        return PisaExtractor.NamePattern.sub("", row).replace("Matricola", "").strip().upper()

    @staticmethod
    def data_form_raw(page):
        result_strings = []

        for s in page[5:]:
            if s.startswith("TOTALI"):
                break  # Stop when the delimiter is encountered

            result_strings.append(s)

        return result_strings

    @staticmethod
    def search_month_year(page):
        for row in page:
            match = PisaExtractor.MONTHS_YEAR_PATTERN.search(row)
            if match:
                return match.group().split()


        raise ExtractingError(page, "Mese")

    @staticmethod
    def extract_page(page):

        name = PisaExtractor.name_from_page(page)
        mese,anno = PisaExtractor.search_month_year(page)


        interested = PisaExtractor.data_form_raw(page)

        data = pd.DataFrame([timbratura for row in interested for timbratura in PisaExtractor.extract(row) if row ],
                            columns=PisaExtractor.columns)

        return data, name, mesi.index(mese.lower()) + 1, int(anno)


def nTtest(filename):
    with open(filename , "r") as f:
        pages = f.read().split("\nPAGES\n")


    Extractor = PisaExtractor(  pages[0].splitlines() )

    print(Extractor.data)

def extract_from_file(file):
    pages = PDFIterator(file)

    data = pd.concat([PisaExtractor(page).with_datetime() for page in pages])
    data["Turni"] = data.apply(lambda r: turno(r["Data"]) if r["Tipo"] == "E" else None, axis=1)
    data.to_csv(f"{os.path.basename(file).split(".")[0]}.csv")







if __name__ == '__main__':
     extract_from_file("../PisaTests/Arrighi Michele_AOUP_timbrature.pdf")