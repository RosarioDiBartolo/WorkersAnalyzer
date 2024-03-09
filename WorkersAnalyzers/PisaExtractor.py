import re
import datetime
import pandas as pd

from WorkersAnalyzers.ExctractingError import ExtractingError

w_days = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
datetime_format = '%Y-%m-%d  %H:%M'  # Example format: 'days hours:minutes'


class PisaExtractor:
    columns = ["Tipo", "Giorno", "Ore", "Minuti", "Settimana"]

    NamePattern = re.compile(r'[^a-zA-Z\s]')

    MONTHS_YEAR_PATTERN = re.compile(
        r'(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s(\d\d\d\d)',
        re.IGNORECASE)

    def __init__(self, page):
        self.data, self.name, self.mese, self.anno = PisaExtractor.extract_page(page)

    PatternEntrateUscite = re.compile(r"(E|U)(\d\d:\d\d)")
    PatternData = re.compile(r'(Lun|Mar|Mer|Gio|Ven|Sab|Dom)\s(\d\d)')

    def encode(extractor):
        extractor.data["Mese"] = mesi.index(extractor.mese) + 1
        extractor.data["Anno"] = extractor.anno
        datetime_string = extractor.data["Anno"].astype(str) + '-' + extractor.data["Mese"].astype(str) + '-' + \
                          extractor.data['Giorno'].astype(str) + ' ' + extractor.data['Ore'].astype(str) + ':' + \
                          extractor.data['Minuti'].astype(str)
        result = pd.to_datetime(datetime_string, format=datetime_format)
        return result

    @staticmethod
    def extract(row):

        EntrateUscite = PisaExtractor.PatternEntrateUscite.findall(row)
        wday, day = PisaExtractor.PatternData.search(row).group().split()
        day = int(day)

        if len(row.split()) > 9:
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
            match = PisaExtractor.MONTHS_YEAR_PATTERN.findall(row)
            if match:
                return match[0][0], match[0][1]

    @staticmethod
    def extract_page(page):

        name = PisaExtractor.name_from_page(page)
        match = PisaExtractor.search_month_year(page)

        if match:
            mese, anno = match
        else:
            raise ExtractingError(page, "Mese")

        interested = PisaExtractor.data_form_raw(page)

        data = pd.DataFrame([timbratura for row in interested for timbratura in PisaExtractor.extract(row)],
                            columns=PisaExtractor.columns)

        return data, name, mese.lower(), anno