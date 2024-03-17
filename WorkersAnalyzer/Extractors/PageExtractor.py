import abc
import re
from WorkersAnalyzer.ExctractingError import ExtractingError
from WorkersAnalyzer.Extractors.PageData import PageData


class PageExtractor  :
    mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre",
            "novembre", "dicembre"]

    MONTHS_YEAR_PATTERN = re.compile(
        r'(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s(\d\d\d\d)',
        re.IGNORECASE)
    def __init__(self, page):

        self.page = page

        self.mese, self.anno = self.search_month_year( )

        self.name = self.extract_name()

    def read(self):
        data = PageData(data=self.extract(), nome=self.extract_name(), mese=self.mese, anno=self.anno)
        return data
    @abc.abstractmethod
    def extract (self ):
        pass
    @abc.abstractmethod
    def extract_name(self ):
        pass

    def search_month_year( self):
        for row in self.page:
            match = PageExtractor.MONTHS_YEAR_PATTERN.search(row)
            if match:
                mese, anno = match.group().split()
                return PageExtractor.mesi.index(mese.lower()) + 1, int(anno)

        raise ExtractingError(self.page, "Mese")