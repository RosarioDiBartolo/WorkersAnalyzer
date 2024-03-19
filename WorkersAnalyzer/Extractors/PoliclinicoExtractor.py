import re

from WorkersAnalyzer.Extractors.PageExtractor import PageExtractor, w_days


class PoliclinicoExtractor (PageExtractor):
    PatternData = re.compile(r'(lu|ma|me|gi|ve|sa|do)(\s|\*)(\d\d)')
    PatternTimbrature = re.compile(r"(E|U|u|e)(\d\d\d\d)")
    PatternName = re.compile(r"BADGE:\d+(.*)")
    WeekTable = dict(zip(["lu", "ma", "me", "gi", "ve", "sa", "do"], w_days))
    def read(self):
        data = super(PoliclinicoExtractor, self).read()
        data.raw["Settimana"] = data.raw["Settimana"].apply(lambda x :  PoliclinicoExtractor.WeekTable[x])
        return data
    def extract(self ):
        InterestedPages = self.content( )

        return [ timbratura for row in InterestedPages for timbratura in
         PoliclinicoExtractor.extract_row(row) ]


    def extract_name(self):
        return PoliclinicoExtractor.PatternName.search(self.page[2]).group(1).strip()
    def content(self):

         for row in self.page[7:]:
            try:
                float(row)
                return

            except ValueError:
                yield row.replace("*", " ")

    @staticmethod
    def extract_row(row):

        Timbrature = PoliclinicoExtractor.PatternTimbrature.findall(row)

        match = PoliclinicoExtractor.PatternData.search(row)
        if match:
            wday, day = match.group().replace("*", " ").split()
            day = int(day)
        else:
            return []

        #print("Day:", day,"Wday:",  wday,"Row:", row, "Orario:" ,Timbrature)
        return [(tipo.upper(), day, int(orario[0:2]), int(orario[2:4]), wday) for (tipo, orario) in
               Timbrature] if Timbrature else [(None, day, 0, 0, wday)]

if __name__ == '__main__':
    from WorkersAnalyzer.EasyTest.PoliclinicoUtils import SamplePages

    e = PoliclinicoExtractor(SamplePages[0])

